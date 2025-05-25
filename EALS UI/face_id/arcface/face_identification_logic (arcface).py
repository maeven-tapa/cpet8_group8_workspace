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
from pygrabber.dshow_graph import FilterGraph 
import mediapipe as mp
import glob
import insightface
from sklearn.metrics.pairwise import cosine_similarity


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
        
        # Keep the label but don't show it - will update UI during initialization without displaying text
        self.wait_label = QLabel("Reloading TensorFlow ML Model... Please wait 1 min and 30 secs or about 2 mins on initializing device")
        self.wait_label.setAlignment(Qt.AlignCenter)
        self.wait_label.setVisible(False)
        
        self.device_name_label = QLabel("Device: Not initialized")
        self.device_name_label.setAlignment(Qt.AlignCenter)

        # Add smooth bounding box tracking
        self.prev_boxes = []
        self.smooth_factor = 0.7  # Lower = smoother but more lag, higher = more responsive

        layout = QVBoxLayout()
        layout.addWidget(self.device_name_label) 
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
        self.enrolled_faces = []
        self.face_templates_dir = os.path.join(os.path.dirname(__file__), "face_templates")
        self.face_images_dir = os.path.join(os.path.dirname(__file__), "face_images")
        os.makedirs(self.face_templates_dir, exist_ok=True)
        os.makedirs(self.face_images_dir, exist_ok=True)

        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = None
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = None

        # ArcFace model with local directory
        model_dir = os.path.join(os.path.dirname(__file__), 'resources')
        os.makedirs(model_dir, exist_ok=True)
        self.arcface_model = insightface.app.FaceAnalysis(name='buffalo_sc', root=model_dir, providers=['CPUExecutionProvider'])
        self.arcface_model.prepare(ctx_id=0)

        self.enroll_active = False
        self.enroll_prompts = [
            "Neutral face",
            "Turn head left",
            "Turn head right",
            "Tilt head up",
            "Tilt head down",
            "With glasses (if you wear them)",
        ]
        self.enroll_pose_requirements = {
            0: {"description": "Neutral face", "pose": "Straight face"},
            1: {"description": "Turn head left", "pose": "Facing Left"},
            2: {"description": "Turn head right", "pose": "Facing Right"},
            3: {"description": "Tilt head up", "pose": "Facing Up"},
            4: {"description": "Tilt head down", "pose": "Facing Down"},
            5: {"description": "With glasses (if you wear them)", "pose": "Straight face"},
        }
        self.enroll_max = min(5, len(self.enroll_prompts))
        self.enroll_index = 0
        self.enroll_captured = 0
        self.enroll_timer_count = 0
        self.enroll_timer_qtimer = QTimer()
        self.enroll_timer_qtimer.timeout.connect(self.update_enroll_timer_label)
        self.person_name = ""
        self.current_pose = "Unknown"
        
    def get_camera_name(self, index=0):
        try:
            graph = FilterGraph()
            cameras = graph.get_input_devices()
            if cameras and index < len(cameras):
                return cameras[index]
        except Exception as e:
            print(f"Error getting camera name: {e}")
        return f"Camera {index}"

    def initialize_device(self):
        QApplication.processEvents()
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                QMessageBox.critical(self, "Error", "Could not open camera.")
                return
            
            device_name = self.get_camera_name(0)
            self.device_name_label.setText(f"Device: {device_name}")
                
            self.face_detection = self.face_detection or self.mp_face_detection.FaceDetection(
                min_detection_confidence=1, model_selection=1)
            
            self.face_mesh = self.face_mesh or self.mp_face_mesh.FaceMesh(
                max_num_faces=1, refine_landmarks=True,
                min_detection_confidence=0.5, min_tracking_confidence=0.5)

            self.timer.start(30)
            self.init_btn.setEnabled(False)
            self.terminate_btn.setEnabled(True)
            self.enroll_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize device: {str(e)}")
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

            if y_angle < -10:
                text = "Facing Right" 
            elif y_angle > 10:
                text = "Facing Left" 
            elif x_angle < -7:
                text = "Facing Down" 
            elif x_angle > 10:
                text = "Facing Up" 
            else:
                text = "Straight face"
                
        return face_landmarks, text

    def smooth_bounding_boxes(self, current_boxes):
        """Apply smoothing to bounding boxes to reduce jitter"""
        if not self.prev_boxes:
            self.prev_boxes = current_boxes
            return current_boxes
            
        smooth_boxes = []
        
        # Match boxes between frames and apply smoothing
        for curr_box in current_boxes:
            x, y, w, h, name = curr_box
            
            # Find best matching previous box
            best_match = None
            min_dist = float('inf')
            
            for prev_box in self.prev_boxes:
                px, py, pw, ph, pname = prev_box
                # Calculate center points
                curr_center = (x + w/2, y + h/2)
                prev_center = (px + pw/2, py + ph/2)
                
                # Square distance between centers
                dist = (curr_center[0] - prev_center[0])**2 + (curr_center[1] - prev_center[1])**2
                
                # If this is a better match and names are compatible
                if dist < min_dist and (not name or not pname or name == pname):
                    min_dist = dist
                    best_match = prev_box
            
            if best_match and min_dist < 10000: 
                px, py, pw, ph, pname = best_match
                
                sx = int(px * self.smooth_factor + x * (1-self.smooth_factor))
                sy = int(py * self.smooth_factor + y * (1-self.smooth_factor))
                sw = int(pw * self.smooth_factor + w * (1-self.smooth_factor))
                sh = int(ph * self.smooth_factor + h * (1-self.smooth_factor))
                
                sname = name if name else pname
                
                smooth_boxes.append((sx, sy, sw, sh, sname))
            else:
                smooth_boxes.append(curr_box)
        
        # Update previous boxes for next frame
        self.prev_boxes = smooth_boxes
        return smooth_boxes

    def detect_face(self, frame):
        results = []
        face_landmarks, pose_text = self.detect_face_pose(frame)
        self.current_pose = pose_text

        if self.arcface_model is None:
            return results

        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = self.arcface_model.get(rgb_frame)
            h, w = frame.shape[:2]
            for face in faces:
                x1, y1, x2, y2 = [int(v) for v in face.bbox]
                x = max(0, x1)
                y = max(0, y1)
                w_box = min(w - x, x2 - x1)
                h_box = min(h - y, y2 - y1)
                name = ""
                likeliness = 0

                # Extract current face crop for visual comparison
                face_crop = frame[y1:y2, x1:x2]
                if face_crop.size > 0:
                    face_crop_resized = cv2.resize(face_crop, (160, 160))

                # Load all embeddings and corresponding face images
                embedding_files = glob.glob(os.path.join(self.face_templates_dir, "*.npy"))
                best_score = -1
                best_name = ""
                input_embedding = face.embedding.reshape(1, -1)
                
                for emb_file in embedding_files:
                    # Load and compare embedding
                    emb = np.load(emb_file)
                    embedding_score = cosine_similarity(input_embedding, emb.reshape(1, -1))[0][0]
                    
                    # Load corresponding face image for visual comparison
                    base_name = os.path.splitext(os.path.basename(emb_file))[0]
                    image_path = os.path.join(self.face_templates_dir, f"{base_name}.jpg")
                    visual_score = 0
                    
                    if os.path.exists(image_path) and face_crop.size > 0:
                        stored_face = cv2.imread(image_path)
                        if stored_face is not None:
                            # Convert both images to grayscale for comparison
                            gray_current = cv2.cvtColor(face_crop_resized, cv2.COLOR_BGR2GRAY)
                            gray_stored = cv2.cvtColor(stored_face, cv2.COLOR_BGR2GRAY)
                            
                            # Calculate structural similarity
                            try:
                                from skimage.metrics import structural_similarity as ssim
                                visual_score = ssim(gray_current, gray_stored)
                            except ImportError:
                                # Fallback to simple correlation if skimage not available
                                result = cv2.matchTemplate(gray_current, gray_stored, cv2.TM_CCOEFF_NORMED)
                                visual_score = np.max(result)
                    
                    # Combine embedding and visual scores (weighted average)
                    combined_score = (embedding_score * 1) + (visual_score * 0.3)
                    
                    if combined_score > best_score and combined_score > 0.35:  # adjusted threshold
                        best_score = combined_score
                        file_name = os.path.splitext(os.path.basename(emb_file))[0]
                        best_name = file_name.split('_')[0]
                
                # Only assign name/likeliness if best_score >= 0.45 (adjusted for combined scoring)
                if best_name and best_score >= 0.65:
                    name = best_name
                    likeliness = int(min(1, max(0, best_score)) * 100)
                results.append((x, y, w_box, h_box, name, likeliness))
        except Exception as e:
            print(f"ArcFace detection error: {str(e)}")

        # Apply smoothing before returning results
        # Remove likeliness for smoothing, add it back after
        smooth_input = [(x, y, w, h, name) for (x, y, w, h, name, _) in results]
        smoothed = self.smooth_bounding_boxes(smooth_input)
        # Merge likeliness back
        final_results = []
        for i, (x, y, w, h, name) in enumerate(smoothed):
            likeliness = results[i][5] if i < len(results) else 0
            final_results.append((x, y, w, h, name, likeliness))
        return final_results

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        faces = self.detect_face(frame)
        for (x, y, w, h, name, likeliness) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, cv2.LINE_AA)
            # Only display name and likeliness if likeliness >= 50
            if name and likeliness >= 50:
                text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
                cv2.rectangle(frame, (x, y - text_size[1] - 10),
                              (x + text_size[0], y), (0, 200, 0), -1)
                cv2.putText(frame, name, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
                # Draw likeliness percentage below the bounding box
                cv2.putText(frame, f"Likeliness: {likeliness}%", (x, y + h + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
            # Optionally, you can skip drawing likeliness if < 50, or show "Unknown"
            # else:
            #     cv2.putText(frame, "Unknown", (x, y + h + 20),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128, 128, 128), 2, cv2.LINE_AA)

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
            faces = self.arcface_model.get(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if len(faces) == 0:
                return
            face = faces[0]
        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = self.arcface_model.get(rgb_frame)
            if len(faces) == 0:
                return
            face = faces[0]

        # Save face embedding for recognition
        embedding = face.embedding
        pose_name = self.enroll_pose_requirements[self.enroll_index]["pose"].replace(" ", "_").lower()
        
        # Save embedding
        embedding_path = os.path.join(self.face_templates_dir, f"{self.person_name}_{pose_name}.npy")
        np.save(embedding_path, embedding)
        
        # Extract and save face image in face_templates directory
        x1, y1, x2, y2 = [int(v) for v in face.bbox]
        face_crop = frame[y1:y2, x1:x2]
        
        if face_crop.size > 0:  # Ensure valid crop
            # Resize face crop to standard size for consistency
            face_crop_resized = cv2.resize(face_crop, (160, 160))
            image_path = os.path.join(self.face_templates_dir, f"{self.person_name}_{pose_name}.jpg")
            cv2.imwrite(image_path, face_crop_resized)
            
            # Also save in face_images directory for backward compatibility
            image_path_backup = os.path.join(self.face_images_dir, f"{self.person_name}_{pose_name}.jpg")
            cv2.imwrite(image_path_backup, face_crop_resized)
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
                                    f"{self.enroll_captured} face embeddings enrolled and saved for {self.person_name}.")
        else:
            QMessageBox.warning(self, "Face Enrollment", "No face embeddings enrolled.")
            
        self.enroll_active = False

    def closeEvent(self, event):
        self.terminate_device()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EALS_FACEID_LOGIC()
    window.show()
    sys.exit(app.exec())
