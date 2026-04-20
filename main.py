import cv2
import mediapipe as mp
import os

VIDEO_PATH = "vidio/kucing.mp4" #GANTI USERNAME KUCING NYA KALO UDAH ADA SAMPEL VIDIONYA TARO DI FOLDER vidio

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

video_cap = None
is_video_playing = False

def check_hand_open(hand_landmarks):

    tips = [8, 12, 16, 20]
    count = 0
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    return count >= 3 

print("Program siap. Buka tangan untuk putar video, kepal untuk tutup.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    any_hand_open = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if check_hand_open(hand_landmarks):
                any_hand_open = True

    if any_hand_open:
        if not is_video_playing:
            video_cap = cv2.VideoCapture(VIDEO_PATH)
            is_video_playing = True
            cv2.namedWindow("Video Player") 
            cv2.moveWindow("Video Player", 1000, 100) 
        
        ret, v_frame = video_cap.read()
        if ret:
            cv2.imshow("Video Player", v_frame)
        else:
            video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    else:
        if is_video_playing:
            cv2.destroyWindow("Video Player")
            video_cap.release()
            is_video_playing = False

    cv2.imshow("Hand Tracker (Camera)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if video_cap: video_cap.release()
cv2.destroyAllWindows()