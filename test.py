import cv2
import mediapipe as mp
import pyautogui

def get_finger_status(hands_module, hand_landmarks, frame_height, frame_width): #Function to check if fingers are joined or not

    index_y = (hand_landmarks[8].y)*frame_height #index 8 corresponds to tip of the index finger
    index_x = (hand_landmarks[8].x)*frame_width

    middle_y = (hand_landmarks[12].y)*frame_height #index 12 corresponds to tip of the middle finger
    middle_x = (hand_landmarks[12].x)*frame_width

    if abs(index_x-middle_x) < 50: 
        return True # less than 50 means fingers are closely joined. more than 40 means split
    else: 
        pyautogui.keyDown('space') #fire when fingers are split
        pyautogui.keyUp('space')
        return False
def finger_location(hands_module, hand_landmarks, frame_width): #get coordinates of finger

    index_x = (hand_landmarks[8].x)*frame_width
    return index_x

hands_module = mp.solutions.hands

initial_position= None 

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands = 1) # looks for hand
drawing_utils = mp.solutions.drawing_utils #Traces the hand
while True:
    _, frame=cap.read()
    frame = cv2.flip(frame, 1) #corrects mirror images
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #color conversion
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
    flag = False

    if hands:
        for hand in hands:
            
            drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS,)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = landmark.x*frame_width
                y = landmark.y*frame_height
            if get_finger_status(hands_module, landmarks, frame_height, frame_width):
                location = finger_location(hands_module,landmarks, frame_width)
                if initial_position is None:
                    initial_position = location #initialise the initial position of the fingers on screen

                # Left : initial > final
                # Right : final > initial
                
                if abs((initial_position-location))>20:
                    if initial_position>location:
                        pyautogui.keyDown('left')
                        pyautogui.keyUp('left')
                    if initial_position<location:
                        pyautogui.keyDown('right')
                        pyautogui.keyUp('right')
                
                initial_position=location #Update position
                

    cv2.imshow('Virtual Mouse', frame) #Displays the frame
    cv2.waitKey(1)