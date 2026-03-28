import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

def analyze_body_language():
    cap = cv2.VideoCapture(0)

    feedback = "Analyzing..."

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            landmarks = results.pose_landmarks.landmark

            left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
            right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y

            if abs(left - right) > 0.05:
                feedback = "⚠️ Leaning posture (low confidence)"
            else:
                feedback = "✅ Good posture (confident)"

        cv2.putText(frame, feedback, (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Body Language Analyzer", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()