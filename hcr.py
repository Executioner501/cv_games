# mediapipe for gaming
import cv2 as cv
import mediapipe as mp
import pyautogui as au
gas_on=False
brake_on=False
#forgot everythign about cv 
cap= cv.VideoCapture(0)

#defining functiosn for gas and brake
def gas():
    global gas_on
    # print("vrooom")
    au.keyDown('right')
    gas_on=True
def stop_gas():
    global gas_on
    au.keyUp('right')
    gas_on=False
def brake():
    global brake_on
    #print("stopping")
    au.keyDown('left')
    brake_on=True
def stop_brake():
    global brake_on
    au.keyUp('left')
    brake_on=False  
def neutral():
    global gas_on
    global brake_on
    if gas_on:
        stop_gas()
    if brake_on:
        stop_brake()      
#for the hands
mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils

hands=mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
#for the airspace(not in use for now)
# x1,y1=300,00
# x2,y2=600,480
#for webcam capture
while True:
    ret,frame=cap.read()
    height, width, _ = frame.shape
    # print(f"Frame size: width={width}, height={height}")
    if not ret:
        break
    
    if cv.waitKey(1)& 0xFF==ord("q"):
        break
    frame=cv.flip(frame,1)
    # cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
    rgb_frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    result=hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            #hand detection part for folding and not folding for now ignoring thumb
            index_tip=hand_landmarks.landmark[8]
            index_pip=hand_landmarks.landmark[6]
            index_mcp=hand_landmarks.landmark[5]
            index_dip=hand_landmarks.landmark[7]
            middle_tip=hand_landmarks.landmark[12]
            middle_pip=hand_landmarks.landmark[10]
            middle_mcp=hand_landmarks.landmark[9]
            middle_dip=hand_landmarks.landmark[11]
            ring_tip=hand_landmarks.landmark[16]
            ring_pip=hand_landmarks.landmark[14]
            thumb_tip=hand_landmarks.landmark[4]
            thumb_ip=hand_landmarks.landmark[3]
            if(index_tip.y<index_pip.y and middle_tip.y>middle_pip.y): #one finger up
                gas()
                stop_brake()
            
            elif (index_tip.y<index_pip.y and middle_tip.y<middle_pip.y): # 2 up
                brake()
                stop_gas()
            else:
                neutral()
            

    cv.imshow("Webcam",frame)
cap.release()
cv.destroyAllWindows() 
#end the capture here

#need to make a neutral gesture


