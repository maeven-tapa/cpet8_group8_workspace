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
import pickle


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
        os.makedirs(self.face_templates_dir, exist_ok=True)
        
        # Directory for face recognition data
        self.recognition_data_dir = os.path.join(os.path.dirname(__file__), "face_data")
        os.makedirs(self.recognition_data_dir, exist_ok=True)
        
        # Fisherface recognizer
        self.recognizer = cv2.face.FisherFaceRecognizer_create()
        self.recognizer_trained = False
        self.label_map = {}  # Maps numeric labels to person names
        self.model_path = os.path.join(self.recognition_data_dir, "fisherface_model.xml")
        self.label_map_path = os.path.join(self.recognition_data_dir, "label_map.pkl")
        
        # Try to load existing model and label map
        self.load_recognizer()

        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = None
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = None

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
        
    def load_recognizer(self):
        try:
            if os.path.exists(self.model_path):
                self.recognizer.read(self.model_path)
                with open(self.label_map_path, 'rb') as f:
                    self.label_map = pickle.load(f)
                self.recognizer_trained = True
                print("Loaded existing Fisherface model")
            else:
                print("No existing Fisherface model found")
        except Exception as e:
            print(f"Error loading recognizer: {e}")
            self.recognizer_trained = False
            
    def save_recognizer(self):
        try:
            self.recognizer.write(self.model_path)
            with open(self.label_map_path, 'wb') as f:
                pickle.dump(self.label_map, f)
            print("Saved Fisherface model")
        except Exception as e:
            print(f"Error saving recognizer: {e}")
            
    def train_recognizer(self):
        print("Training Fisherface recognizer...")
        faces = []
        labels = []
        next_label = max(self.label_map.keys()) + 1 if self.label_map else 0
        
        # Use enrolled faces to train the recognizer
        if self.person_name not in self.label_map.values():
            self.label_map[next_label] = self.person_name
            person_label = next_label
        else:
            # Find the label for existing person
            person_label = [k for k, v in self.label_map.items() if v == self.person_name][0]
            
        for face in self.enrolled_faces:
            # Convert to grayscale and resize to common size
            if face.shape[0] != 100 or face.shape[1] != 100:
                face = cv2.resize(face, (100, 100))
            gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            faces.append(gray_face)
            labels.append(person_label)
            
        # If this is the first training, we need to load existing templates
        if not self.recognizer_trained:
            # Check for existing templates and add them
            for file in os.listdir(self.face_templates_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    template_path = os.path.join(self.face_templates_dir, file)
                    face_img = cv2.imread(template_path)
                    if face_img is None:
                        continue
                    
                    # Get name from filename (format: name_pose.png)
                    name = file.split('_')[0]
                    
                    # Assign a label to this person
                    if name not in self.label_map.values():
                        self.label_map[next_label] = name
                        face_label = next_label
                        next_label += 1
                    else:
                        # Find the label for existing person
                        face_label = [k for k, v in self.label_map.items() if v == name][0]
                    
                    # Process the face image
                    if face_img.shape[0] != 100 or face_img.shape[1] != 100:
                        face_img = cv2.resize(face_img, (100, 100))
                    gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                    faces.append(gray_face)
                    labels.append(face_label)
        
        # Check if we have enough data to train
        if len(faces) < 1:
            print("Not enough face images to train the recognizer")
            return False
        
        # Check if we have at least 2 different people (Fisherface requirement)
        if len(set(labels)) < 2:
            print("Fisherface requires at least 2 different people for training")
            
            # If we have an existing trained model, keep using it
            if os.path.exists(self.model_path) and self.recognizer_trained:
                # Update the label map even if we can't retrain
                self.save_recognizer()  
                print("Using existing model and saving updated label map")
                return True
                
            # Create dummy second face class with variations of the enrolled face
            print("Creating dummy second class for initial training")
            dummy_label = next_label
            self.label_map[dummy_label] = f"{self.person_name}_reference"
            
            # Create variations from the existing faces for the second class
            for i, face in enumerate(faces[:]):  # Use a copy of faces
                # Create a horizontally flipped version
                flipped = cv2.flip(face, 1)  # 1 = horizontal flip
                faces.append(flipped)
                labels.append(dummy_label)
                
                # Create a slightly rotated version 
                if i < 2:  # Just add a couple of rotations to meet the minimum
                    M = cv2.getRotationMatrix2D((face.shape[1]//2, face.shape[0]//2), 10, 1.0)
                    rotated = cv2.warpAffine(face, M, (face.shape[1], face.shape[0]))
                    faces.append(rotated)
                    labels.append(dummy_label)
        
        # Train the recognizer
        try:
            self.recognizer.train(faces, np.array(labels))
            self.recognizer_trained = True
            self.save_recognizer()
            print(f"Trained with {len(faces)} images of {len(set(labels))} people")
            return True
        except Exception as e:
            print(f"Error training recognizer: {e}")
            
            # Fall back to LBPH if Fisherface fails
            try:
                print("Falling back to LBPH recognizer")
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
                self.recognizer.train(faces, np.array(labels))
                self.recognizer_trained = True
                self.save_recognizer()
                print(f"Trained LBPH with {len(faces)} images")
                return True
            except Exception as e2:
                print(f"Error training LBPH recognizer: {e2}")
                return False
        
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
            x, y, w, h, name, confidence = curr_box  # Updated to unpack 6 elements
            
            # Find best matching previous box
            best_match = None
            min_dist = float('inf')
            
            for prev_box in self.prev_boxes:
                px, py, pw, ph = prev_box[:4]  # Only unpack the position elements
                pname = prev_box[4] if len(prev_box) > 4 else ""
                
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
                px, py, pw, ph = best_match[:4]
                pname = best_match[4] if len(best_match) > 4 else ""
                pconf = best_match[5] if len(best_match) > 5 else 0
                
                sx = int(px * self.smooth_factor + x * (1-self.smooth_factor))
                sy = int(py * self.smooth_factor + y * (1-self.smooth_factor))
                sw = int(pw * self.smooth_factor + w * (1-self.smooth_factor))
                sh = int(ph * self.smooth_factor + h * (1-self.smooth_factor))
                
                sname = name if name else pname
                sconf = confidence  # Use current confidence
                
                smooth_boxes.append((sx, sy, sw, sh, sname, sconf))
            else:
                smooth_boxes.append(curr_box)
        
        # Update previous boxes for next frame
        self.prev_boxes = smooth_boxes
        return smooth_boxes

    def detect_face(self, frame):
        results = []
        
        face_landmarks, pose_text = self.detect_face_pose(frame)
        self.current_pose = pose_text

        if self.face_detection is None:
            return results
        
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
                    confidence = 0
                    
                    # Use Fisherface recognizer if trained
                    if self.recognizer_trained and w_box > 0 and h_box > 0:
                        try:
                            face_img = frame[y:y+h_box, x:x+w_box]
                            face_img = cv2.resize(face_img, (100, 100))
                            gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                            
                            label, confidence = self.recognizer.predict(gray_face)
                            
                            # Lower confidence value means better match in FisherFace
                            # Convert to percentage (0-100) where higher is better
                            confidence_percentage = max(0, min(100, 100 - confidence/10))
                            
                            if confidence_percentage > 20 and label in self.label_map:  # Adjust threshold as needed
                                name = self.label_map[label]
                                confidence = confidence_percentage
                        except Exception as e:
                            print(f"Error in face recognition: {e}")
                            
                    results.append((x, y, w_box, h_box, name, confidence))
        except Exception as e:
            print(f"MediaPipe detection error: {str(e)}")
        
        # Apply smoothing before returning results
        return self.smooth_bounding_boxes(results)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        faces = self.detect_face(frame)
        for face_data in faces:
            x, y, w, h = face_data[:4]
            name = face_data[4] if len(face_data) > 4 else ""
            confidence = face_data[5] if len(face_data) > 5 else 0
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, cv2.LINE_AA)
            
            # Add slightly darker background behind text for better visibility
            if name:
                text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
                cv2.rectangle(frame, (x, y - text_size[1] - 10), 
                            (x + text_size[0], y), (0, 200, 0), -1)
                cv2.putText(frame, name, (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Draw confidence percentage below the bounding box
            cv2.putText(frame, f"Confidence: {int(confidence)}%", (x, y + h + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

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
        self.enrolled_faces = []  # Reset the enrolled faces for this session
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
        
        # Train the Fisherface recognizer with new data
        if self.enroll_captured > 0:
            self.instruction_label.setText("Training face recognition model...")
            QApplication.processEvents()  # Update UI
            
            success = self.train_recognizer()
            
            if success:
                QMessageBox.information(self, "Face Enrollment", 
                                        f"{self.enroll_captured} face images enrolled and model trained for {self.person_name}.")
            else:
                QMessageBox.warning(self, "Face Enrollment", 
                                    "Face images enrolled but model training failed. Try enrolling more images.")
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
