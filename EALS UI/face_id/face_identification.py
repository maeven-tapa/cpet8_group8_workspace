import sys
import cv2
import numpy as np
import os
import chime
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox,
    QInputDialog, QLineEdit, QProgressBar
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
import mediapipe as mp

class EALS_FACEID_LOGIC(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EALS - FACE ID WRAPPER")
        self.setGeometry(100, 100, 800, 600)
        self.init_btn = QPushButton("Initialize Device")
        self.terminate_btn = QPushButton("Terminate Device")
        self.enroll_btn = QPushButton("Enroll Face")
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.instruction_label = QLabel("")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.timer_label = QLabel("")
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.wait_label = QLabel("Reloading TensorFlow ML Model... Please wait 1 min and 30 secs or about 2 mins on initializing device")
        self.wait_label.setAlignment(Qt.AlignCenter)
        self.wait_label.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.instruction_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.wait_label)
        layout.addWidget(self.init_btn)
        layout.addWidget(self.terminate_btn)
        layout.addWidget(self.enroll_btn)
        self.setLayout(layout)

        self.init_btn.clicked.connect(self.initialize_device)
        self.terminate_btn.clicked.connect(self.terminate_device)
        self.enroll_btn.clicked.connect(self.enroll_face)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.enrolled_faces = []
        self.face_templates_dir = os.path.join(os.path.dirname(__file__), "face_templates")
        os.makedirs(self.face_templates_dir, exist_ok=True)

        proto_path = cv2.data.haarcascades.replace('haarcascades', 'dnn') + 'deploy.prototxt'
        model_path = cv2.data.haarcascades.replace('haarcascades', 'dnn') + 'res10_300x300_ssd_iter_140000.caffemodel'
        self.dnn_face_net = cv2.dnn.readNetFromCaffe(proto_path, model_path) if os.path.exists(proto_path) and os.path.exists(model_path) else None

        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = None
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = None

        self.enroll_active = False
        self.enroll_prompts = [
            "Neutral face",
            "Smile",
            "Turn head left",
            "Turn head right",
            "Tilt head up",
            "Tilt head down",
            "With glasses (if you wear them)",
        ]
        self.enroll_pose_requirements = {
            0: {"description": "Neutral face", "pose": "Straight face"},
            1: {"description": "Smile", "pose": "Straight face"},
            2: {"description": "Turn head left", "pose": "Facing Left"},
            3: {"description": "Turn head right", "pose": "Facing Right"},
            4: {"description": "Tilt head up", "pose": "Facing Up"},
            5: {"description": "Tilt head down", "pose": "Facing Down"},
            6: {"description": "With glasses (if you wear them)", "pose": "Straight face"},
        }
        self.enroll_max = min(5, len(self.enroll_prompts))
        self.enroll_index = 0
        self.enroll_captured = 0
        self.enroll_timer_count = 0
        self.enroll_timer_qtimer = QTimer()
        self.enroll_timer_qtimer.timeout.connect(self.update_enroll_timer_label)
        self.person_name = ""
        self.current_pose = "Unknown"

    def initialize_device(self):
        self.wait_label.setVisible(True)
        QApplication.processEvents()
        
        try:
            test_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not test_cap.isOpened():
                QMessageBox.critical(self, "Error", "No camera found or camera index out of range.")
                self.wait_label.setVisible(False)
                return
            test_cap.release()
            
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                QMessageBox.critical(self, "Error", "Could not open camera.")
                self.wait_label.setVisible(False)
                return
                
            if self.face_detection is None:
                self.face_detection = self.mp_face_detection.FaceDetection(
                    min_detection_confidence=0.5,
                    model_selection=0  
                )
            
            if self.face_mesh is None:
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                
            self.timer.start(30)
            self.init_btn.setEnabled(False)
            self.terminate_btn.setEnabled(True)
            self.enroll_btn.setEnabled(True)
            self.wait_label.setVisible(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize device: {str(e)}")
            self.wait_label.setVisible(False)
            self.terminate_device()

    def terminate_device(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        if self.face_detection:
            self.face_detection.close()
            self.face_detection = None
        if self.face_mesh:
            self.face_mesh.close()
            self.face_mesh = None
        self.image_label.clear()
        self.init_btn.setEnabled(True)
        self.terminate_btn.setEnabled(False)
        self.enroll_btn.setEnabled(False)

    def detect_face_pose(self, frame):
        if self.face_mesh is None:
            return None, "Unknown"
            
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        
        if not results.multi_face_landmarks:
            return None, "No Face"
        
        img_h, img_w = frame.shape[:2]
        
        text = "Unknown"
        
        for face_landmarks in results.multi_face_landmarks:
            face_2d = []
            face_3d = []
            
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    x, y = int(lm.x*img_w), int(lm.y*img_h)

                    face_2d.append([x,y])
                    face_3d.append([x, y, lm.z])

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            focal_length = img_w
            center = (img_w/2, img_h/2)

            camera_matrix = np.array(
                [[focal_length, 0, center[0]],
                 [0, focal_length, center[1]],
                 [0,0,1]])
    
            dist_coeffs = np.zeros((4,1), dtype = np.float64) 
            
            (success, rotation_vector, translation_vector) = cv2.solvePnP(face_3d, face_2d, camera_matrix, dist_coeffs)
            rmat = cv2.Rodrigues(rotation_vector)[0] 

            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            x_angle = angles[0] * 360
            y_angle = angles[1] * 360

            if y_angle < -15:
                text = "Facing Right" 
            elif y_angle > 15:
                text = "Facing Left" 
            elif x_angle < -7:
                text = "Facing Down" 
            elif x_angle > 20:
                text = "Facing Up" 
            else:
                text = "Straight face"
                print(x_angle, y_angle)
                
        return face_landmarks, text

    def detect_face(self, frame):
        results = []
        
        face_landmarks, pose_text = self.detect_face_pose(frame)
        self.current_pose = pose_text

        if self.face_detection is None:
            pass
        else:
            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_results = self.face_detection.process(rgb_frame)
                
                if mp_results and mp_results.detections:
                    h, w = frame.shape[:2]
                    for detection in mp_results.detections:
                        bboxC = detection.location_data.relative_bounding_box
                        x = int(bboxC.xmin * w)
                        y = int(bboxC.ymin * h)
                        w_box = int(bboxC.width * w)
                        h_box = int(bboxC.height * h)
                        
                        x = max(0, x)
                        y = max(0, y)
                        w_box = min(w - x, w_box)
                        h_box = min(h - y, h_box)
                        
                        name = ""
                        template_files = [f for f in os.listdir(self.face_templates_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                        if template_files and w_box > 0 and h_box > 0:
                            input_face = cv2.resize(frame[y:y+h_box, x:x+w_box], (100, 100))
                            input_gray = cv2.cvtColor(input_face, cv2.COLOR_BGR2GRAY)
                            input_hist = cv2.calcHist([input_gray], [0], None, [256], [0, 256])
                            input_hist = cv2.normalize(input_hist, input_hist).flatten()
                            best_score = 0.0
                            best_name = ""
                            for template_file in template_files:
                                template_path = os.path.join(self.face_templates_dir, template_file)
                                template_img = cv2.imread(template_path)
                                if template_img is None:
                                    continue
                                template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
                                template_hist = cv2.calcHist([template_gray], [0], None, [256], [0, 256])
                                template_hist = cv2.normalize(template_hist, template_hist).flatten()
                                score = cv2.compareHist(input_hist, template_hist, cv2.HISTCMP_CORREL)
                                if score > best_score and score > 0.8:
                                    best_score = score
                                    file_name = os.path.splitext(template_file)[0]
                                    best_name = file_name.split('_')[0]
                            if best_name:
                                name = best_name
                        results.append((x, y, w_box, h_box, name))
                    
                    if results:
                        return results
            except Exception as e:
                print(f"MediaPipe detection error: {str(e)}")
        
        h, w = frame.shape[:2]
        if self.dnn_face_net:
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                         (300, 300), (104.0, 177.0, 123.0))
            self.dnn_face_net.setInput(blob)
            detections = self.dnn_face_net.forward()
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.7:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    x, y, x2, y2 = box.astype("int")
                    x, y, w_box, h_box = max(0, x), max(0, y), x2 - x, y2 - y
                    name = ""
                    template_files = [f for f in os.listdir(self.face_templates_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    if template_files:
                        input_face = cv2.resize(frame[y:y+h_box, x:x+w_box], (100, 100))
                        input_gray = cv2.cvtColor(input_face, cv2.COLOR_BGR2GRAY)
                        input_hist = cv2.calcHist([input_gray], [0], None, [256], [0, 256])
                        input_hist = cv2.normalize(input_hist, input_hist).flatten()
                        best_score = 0.0
                        best_name = ""
                        for template_file in template_files:
                            template_path = os.path.join(self.face_templates_dir, template_file)
                            template_img = cv2.imread(template_path)
                            if template_img is None:
                                continue
                            template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
                            template_hist = cv2.calcHist([template_gray], [0], None, [256], [0, 256])
                            template_hist = cv2.normalize(template_hist, template_hist).flatten()
                            score = cv2.compareHist(input_hist, template_hist, cv2.HISTCMP_CORREL)
                            if score > best_score and score > 0.9:
                                best_score = score
                                file_name = os.path.splitext(template_file)[0]
                                best_name = file_name.split('_')[0]
                        if best_name:
                            name = best_name
                    results.append((x, y, w_box, h_box, name))
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            template_files = [f for f in os.listdir(self.face_templates_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            for (x, y, w_box, h_box) in faces:
                name = ""
                if template_files:
                    input_face = cv2.resize(frame[y:y+h_box, x:x+w_box], (100, 100))
                    input_gray = cv2.cvtColor(input_face, cv2.COLOR_BGR2GRAY)
                    input_hist = cv2.calcHist([input_gray], [0], None, [256], [0, 256])
                    input_hist = cv2.normalize(input_hist, input_hist).flatten()
                    best_score = 0.0
                    best_name = ""
                    for template_file in template_files:
                        template_path = os.path.join(self.face_templates_dir, template_file)
                        template_img = cv2.imread(template_path)
                        if template_img is None:
                            continue
                        template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
                        template_hist = cv2.calcHist([template_gray], [0], None, [256], [0, 256])
                        template_hist = cv2.normalize(template_hist, template_hist).flatten()
                        score = cv2.compareHist(input_hist, template_hist, cv2.HISTCMP_CORREL)
                        if score > best_score and score > 0.9:
                            best_score = score
                            file_name = os.path.splitext(template_file)[0]
                            best_name = file_name.split('_')[0]
                    if best_name:
                        name = best_name
                results.append((x, y, w_box, h_box, name))
        return results

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        face_landmarks, pose_text = self.detect_face_pose(frame)
        
        faces = self.detect_face(frame)
        for (x, y, w, h, name) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if name:
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, pose_text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def enroll_face(self):
        if not self.cap or self.enroll_active:
            return
            
        name, ok = QInputDialog.getText(self, "Face Enrollment", 
                                        "Enter the person's name:", QLineEdit.Normal, "")
        if not ok or not name.strip():
            QMessageBox.warning(self, "Face Enrollment", "Name is required for enrollment.")
            return
            
        self.person_name = name.strip()
        self.enroll_max = len(self.enroll_prompts) 
        self.enroll_index = 0
        self.enroll_captured = 0
        self.enroll_active = True
        
        self.progress_bar.setMaximum(self.enroll_max)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        self.set_enrollment_instruction()
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.enroll_update_frame)
        
        self.enroll_timer_count = 3
        self.timer_label.setText(str(self.enroll_timer_count))
        self.enroll_timer_qtimer.start(1000)

    def set_enrollment_instruction(self):
        if self.enroll_index < len(self.enroll_pose_requirements):
            pose_info = self.enroll_pose_requirements[self.enroll_index]
            self.instruction_label.setText(f"Please show: {pose_info['description']} ({pose_info['pose']})")
        else:
            self.instruction_label.setText("Enrollment complete!")

    def enroll_update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
            
        face_landmarks, pose_text = self.detect_face_pose(frame)
        faces = self.detect_face(frame)
        
        if len(faces) > 0:
            x, y, w, h = faces[0][:4]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            if self.enroll_index < len(self.enroll_pose_requirements):
                required_pose = self.enroll_pose_requirements[self.enroll_index]["pose"]
                cv2.putText(frame, f"Current: {pose_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, f"Required: {required_pose}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if pose_text == required_pose and self.enroll_timer_count <= 0:
                    self.capture_enroll_image(frame, faces[0])
        
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h_img, w_img, ch = rgb_image.shape
        bytes_per_line = ch * w_img
        qt_image = QImage(rgb_image.data, w_img, h_img, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def update_enroll_timer_label(self):
        if not self.enroll_active:
            self.timer_label.setText("")
            self.enroll_timer_qtimer.stop()
            return
            
        if self.enroll_index < len(self.enroll_pose_requirements):
            required_pose = self.enroll_pose_requirements[self.enroll_index]["pose"]
            
            if self.current_pose == required_pose:
                if self.enroll_timer_count > 0:
                    self.timer_label.setText(str(self.enroll_timer_count))
                    self.enroll_timer_count -= 1
                else:
                    self.timer_label.setText("Capturing...")
            else:
                self.enroll_timer_count = 3
                self.timer_label.setText("Get in position")

    def capture_enroll_image(self, frame=None, face=None):
        if not self.enroll_active or self.enroll_index >= self.enroll_max:
            self.finish_enrollment()
            return
            
        if frame is None:
            ret, frame = self.cap.read()
            if not ret:
                return
            faces = self.detect_face(frame)
            if len(faces) == 0:
                return
            face = faces[0]
        
        x, y, w, h = face[:4]
        face_img = frame[y:y+h, x:x+w]
        face_resized = cv2.resize(face_img, (100, 100))
        self.enrolled_faces.append(face_resized)
        
        pose_name = self.enroll_pose_requirements[self.enroll_index]["pose"].replace(" ", "_").lower()
        save_path = os.path.join(self.face_templates_dir, f"{self.person_name}_{pose_name}.png")
        cv2.imwrite(save_path, face_resized)

        chime.theme('chime')
        chime.success()
        
        self.enroll_captured += 1
        self.enroll_index += 1
        self.progress_bar.setValue(self.enroll_index)
        
        self.enroll_timer_count = 3
        
        if self.enroll_index < self.enroll_max:
            self.set_enrollment_instruction()
        else:
            self.finish_enrollment()

    def finish_enrollment(self):
        self.instruction_label.setText("Enrollment complete!")
        self.timer_label.setText("")
        self.enroll_timer_qtimer.stop()
        self.progress_bar.setVisible(False)
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.update_frame)
        
        if self.enroll_captured > 0:
            QMessageBox.information(self, "Face Enrollment", 
                                    f"{self.enroll_captured} face images enrolled and saved for {self.person_name}.")
        else:
            QMessageBox.warning(self, "Face Enrollment", "No face images enrolled.")
            
        self.enroll_active = False

    def closeEvent(self, event):
        self.terminate_device()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EALS_FACEID_LOGIC()
    window.show()
    sys.exit(app.exec())
