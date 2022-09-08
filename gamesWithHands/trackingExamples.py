import argparse
import mediapipe as mp
import cv2
import numpy as np 

def main(mode):
	# Create camera capture
	cap = cv2.VideoCapture(0)
	screen_width, screen_height = cap.get(3), cap.get(4)

	run = True
	if mode == "hand":
		while cap.isOpened() and run:
			success, image = cap.read()
			if not success:
				continue
			result, image = processImage(hands, image)
			if result.multi_hand_landmarks:
				for hand in result.multi_hand_landmarks:
					for i, pos in enumerate(hand.landmark):
						cx, cy = int(pos.x * screen_width), int(pos.y * screen_height)
						cv2.circle(image, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
					mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			cv2.imshow(mode, image)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
	elif mode == "facedet":
		while cap.isOpened() and run:
			success, image = cap.read()
			if not success:
				continue
			result, image = processImage(face_detection, image)
			if result.detections:
				for detection in result.detections:
					mp_drawing.draw_detection(image, detection)
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			cv2.imshow(mode, image)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
	elif mode == "pose":
		while cap.isOpened() and run:
			success, image = cap.read()
			if not success:
				continue
			result, image = processImage(pose, image)
			if result.pose_landmarks:
				mp_drawing.draw_landmarks(image, result.pose_landmarks, \
					mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			cv2.imshow(mode, image)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
	elif mode == "facemesh":
		while cap.isOpened() and run:
			success, image = cap.read()
			if not success:
				continue
			result, image = processImage(face_mesh, image)
			if result.multi_face_landmarks:
				for detection in result.multi_face_landmarks:
					mp_drawing.draw_landmarks(image, landmark_list=detection, \
						connections=mp_face_mesh.FACEMESH_TESSELATION, landmark_drawing_spec=None, \
						connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
					mp_drawing.draw_landmarks(image, landmark_list=detection, \
						connections=mp_face_mesh.FACEMESH_CONTOURS, landmark_drawing_spec=None, \
						connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			cv2.imshow(mode, image)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
	elif mode == "holistic":
		while cap.isOpened() and run:
			success, image = cap.read()
			if not success:
				continue
			result, image = processImage(holistic, image)
			if result.multi_face_landmarks:
				mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, \
					landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
				mp_drawing.draw_landmarks(image, results.face_landmarks, \
					mp_holistic.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			cv2.imshow(mode, image)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break

def processImage(method, image):
	image = np.flip(image, 1)
	imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	results = method.process(image)
	return results, imageRGB

# Argparse
parser = argparse.ArgumentParser(description="Draw mediapipe landmarks")
choice_list = ["facedet", "facemesh", "hand", "pose", "holistic"]
parser.add_argument("--mode", default="face", choices=choice_list, help="Specifies what landsmarks to be drawn.")
args = parser.parse_args()

# mediapipe setup variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

hands = mp_hands.Hands()
face_detection = mp_face_detection.FaceDetection()
face_mesh = mp_face_mesh.FaceMesh()
pose = mp_pose.Pose()
holistic = mp_holistic.Holistic()

if __name__ == "__main__":
	main(args.mode)