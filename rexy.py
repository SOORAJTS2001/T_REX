import cv2 as cv
import cvzone as cvz
import PositionModule as pm
from cvzone.HandTrackingModule import HandDetector
import random,math,pyfirmata
from numpy import interp
board=pyfirmata.Arduino('/dev/ttyACM0')
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
pin9 = board.get_pin('d:9:s')#it is for base controll
pin10 = board.get_pin('d:10:s')#it is of ankle
pin11 = board.get_pin('d:11:s')#it is for wrist
pin6 = board.get_pin('d:6:s')#it is for jaw
tick = cv.imread("tick.png", cv.IMREAD_UNCHANGED)#this is the tick for the correct frame
imgtick = cv.resize(tick, (50, 50), None, 0.3, 0.3)
cross = cv.imread("crs.png", cv.IMREAD_UNCHANGED)#this is the cross for the wrong frame
imgcross = cv.resize(cross, (50, 50), None, 0.3, 0.3)
base_rot = 0#final base rot angle
elb_angle = 90#current elbow angle
ankle_angle = 0#current ankle angle
arm_length=216#length of the  my arm 
cap = cv.VideoCapture(0)#records video from the camera
detector = pm.poseDetector()
hand_detector = HandDetector(detectionCon=0.8, maxHands=1)
imagespos = random.randint(0,2)
pin9.write(0)
pin10.write(120)
pin11.write(90)
while True:
    success, img = cap.read()
    img = cv.flip(img,1)#it is to flip the image
    hands = hand_detector.findHands(img, draw=True,flipType=False)#detects the hand
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    # print(hands_open)
    if hands: #if there is a hand
        if(hands[0]):
            if hands[0][0]:
                fingstatus = hand_detector.fingersUp(hands[0][0])
                print("hands are",fingstatus)
                if ( (fingstatus[1:]== [0,0,0,0]) and hands[0][0]['type']=='Right'):
                    print("fingers closed")
                    pin6.write(0)
                if (fingstatus[1:]== [1,1,1,1]) :
                    print("fingers open")
                    pin6.write(180)
                if hands[0][0]['lmList'] and hands[0][0]['type']=='Right':
                    #print(hands[0][0]['lmList'][0][1])
                    ankle_angle=interp(hands[0][0]['lmList'][0][1],[0,480],[0,90])
                    pin11.write(ankle_angle)
                    print("angle detected:",ankle_angle) 
    if lmList:
        #img pos is the position coordinates of the image as a dictionary with key as name of the image,
        if lmList[14][1] in range(140,190) and lmList[14][2] in range(300,350):
            img = cvz.overlayPNG(img, imgtick, [400,0])
            elb_angle = int(detector.findAngle(img, 12, 14, 16, draw=False))
            if(elb_angle<90):
                print("moving up",elb_angle)
            elif(elb_angle>90):
                print("moving down",elb_angle)
            x = abs(lmList[16][1]-171)#this is the x coordinate of the refernce
            y = abs(lmList[16][2]-329)#this is the y coordinate of the reference
            x = x**2
            y = y**2
            arm_length = math.sqrt(x+y)#arm length measured by the computer
            # print(d)
            if(arm_length>216):
                langle = 180-(0.001548627925746558*(arm_length**2)+(0.09397699757869586*arm_length)-1.3640032284102335)
                print("arm to the left",langle)
                base_rot = langle
                # print("to the left")
            elif (arm_length<216):
                rangle = 0.0011659567527420355*(arm_length**2)-(1.1019051125650066*arm_length)+255.52348954088453
                print("arm to the right",rangle)
                base_rot = rangle   
        else:
            img = cvz.overlayPNG(img, imgcross, [400,0])#overlays the image
        cv.circle(img, (171, 329), 15, (255, 255, 0), cv.FILLED)
        cv.circle(img, (lmList[12][1], lmList[12][2]), 15, (0, 255, 0), cv.FILLED)
        cv.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 255, 0), cv.FILLED)
        cv.circle(img, (lmList[16][1], lmList[16][2]), 15, (0, 255, 0), cv.FILLED)
        print("base_rot",base_rot)
        pin9.write(abs(180-base_rot))#it is to send the base rot angle to the arduino
        if(elb_angle>90):elb_angle = 90
        pin10.write(abs(90-elb_angle)+120)#it is to send the elbow angle to the arduino
        #it is to send the elbow angle to the arduino
        

    # fpsReader = cvz.FPS()
    # print(hb,wb)
    # cv.namedWindow("Image", cv.WND_PROP_FULLSCREEN)
    # cv.setWindowProperty("Image", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    # _, imgResult = fpsReader.update(imgResult)
    cv.imshow("Image", img)
    cv.waitKey(1)