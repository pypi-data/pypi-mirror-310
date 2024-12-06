import cv2
import os
import logging

class FindHuman:
    def __init__(self, face_recognition=False, save_images=False, measure_distance=False, 
                 save_video=False, mask_detection=False, 
                 image_save_callback=None, distance_callback=None, 
                 distance_color=(0, 255, 0)):
        self.face_recognition = face_recognition
        self.save_images = save_images
        self.measure_distance = measure_distance
        self.save_video = save_video
        self.mask_detection = mask_detection
        self.image_save_callback = image_save_callback
        self.distance_callback = distance_callback
        self.distance_color = distance_color

        self.logger = logging.getLogger('FindHuman')
        logging.basicConfig(level=logging.INFO)

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.hog_cascade = cv2.HOGDescriptor()
        self.hog_cascade.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        if self.save_images and not os.path.exists('captured_images'):
            os.makedirs('captured_images')

        self.out = None
        if self.save_video:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter('output_video.avi', fourcc, 20.0, (640, 480))

    def save_detected_image(self, frame, x, y, w, h, label):
        if self.save_images:
            cropped_image = frame[y:y + h, x:x + w]
            file_name = f"captured_images/{label}_{x}_{y}.jpg"
            cv2.imwrite(file_name, cropped_image)
            
            if self.image_save_callback:
                self.image_save_callback(label, file_name)

    def estimate_distance(self, w, h):
        focal_length = 800
        real_width = 0.2
        distance = (focal_length * real_width) / w
        return distance

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        bodies, _ = self.hog_cascade.detectMultiScale(frame, winStride=(8, 8), padding=(8, 8), scale=1.05)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            if self.save_images:
                self.save_detected_image(frame, x, y, w, h, "Face")

            if self.measure_distance:
                distance = self.estimate_distance(w, h)
                cv2.putText(frame, f"Distance: {distance:.2f}m", (x, y + h + 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, self.distance_color, 2)
                if self.distance_callback:
                    self.distance_callback(distance)

        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Human", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            if self.save_images:
                self.save_detected_image(frame, x, y, w, h, "Human")

            if self.measure_distance:
                distance = self.estimate_distance(w, h)
                cv2.putText(frame, f"Distance: {distance:.2f}m", (x, y + h + 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, self.distance_color, 2)
                if self.distance_callback:
                    self.distance_callback(distance)

        return frame

    def run(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            frame = self.process_frame(frame)

            if self.save_video and self.out is not None:
                self.out.write(frame)

            cv2.imshow('Video - Face and Human Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        if self.out is not None:
            self.out.release()
        cv2.destroyAllWindows()
