import mediapipe as mp
import time
import cv2
import pyautogui
import threading
from tkinter import *
from PIL import Image, ImageTk

pyautogui.FAILSAFE = False;
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
 
pTime = 0
cTime = 0



window = Tk()
window.title("Force Hand Cursor (developed by Dan_Mark)")
window.iconbitmap('FHC.ico')
window['bg'] = '#cfd4e8'
window.geometry('600x480')
frame_top = Frame(window, bg = '#cfd4e8')
frame_top.place(relx=0.05,rely=0.025,relwidth=0.9,relheight=0.1)
frame = Frame(window, bg = '#c1c8e0')
frame.place(relx=0.05,rely=0.15,relwidth=0.9,relheight=0.8)
camera = Label(frame, bg = '#c1c8e0')
camera.pack()

def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def incaps(x1, y1, x2, y2):
    if x1 < x2 + 20:
        x1 = x1 + abs(x2 - x1)/10
    if x1 > x2 + 20:
        x1 = x1 - abs(x2 - x1)/10
    if y1 < y2 + 20:
        y1 = y1 + abs(y2 - y1)/10
    if y1 > y2 + 20:
        y1 = y1 - abs(y2 - y1)/10
    return [x1, y1]

x4, y4, x8, y8, x9, y9, x20, y20 = (-1,0,0,0,100,100,100,100)
main_do = True

def ThreadCursor ():
    f = True
    global x4, y4, x8, y8, x9, y9, x20, y20
    global main_do
    while main_do is True:
        if x4 != -1:
            Xcur, Ycur = pyautogui.position()
            Xcur, Ycur = incaps(Xcur,Ycur,remap(x9, 250, 400, 1900, 0),remap(y9, 200, 300, 0, 1070))
            if Xcur > 1915:
                Xcur = 1915
            if Ycur > 1070:
                Ycur = 1070
            #print(str(x4) + ' ' + str(x8) + '; ' + str(y4) + ' ' + str(y8) + '; ')
            pyautogui.moveTo(Xcur,Ycur)
            if abs(y4 - y8) < 10 & abs(x4 - x8) < 20:
                if f is True:
                    pyautogui.click(Xcur,Ycur)
                    f = False
            elif abs(y4 - y20) < 10 & abs(x4 - x20) < 10:
                if f is True:
                    pyautogui.rightClick(Xcur,Ycur)
                    f = False
            else:
                f = True

def ThreadCV():
    global x4, y4, x8, y8, x9, y9, x20, y20
    global main_do
    global camera
    while main_do is True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    #cv2.circle(img, (cx, cy), 15, (255, 198, 0), cv2.FILLED)
                    if id == 4:
                        x4 = cx
                        y4 = cy
                    if id == 8:
                        x8 = cx
                        y8 = cy
                    if id == 9:
                        x9 = cx
                        y9 = cy
                    if id == 20:
                        x20 = cx
                        y20 = cy
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                break
        else:
            x4 = -1
        #cv2.imshow("Image", img) 
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        imgar = Image.fromarray(cv2image)

        imgtk = ImageTk.PhotoImage(image=imgar)
        camera.imgtk = imgtk
        camera.configure(image=imgtk)
        cv2.waitKey(1)

def clicked_stop():
    global main_do 
    main_do = False
    cap.close();

def clicked_start():
    global main_do 
    main_do = True
    th1 = threading.Thread(target=ThreadCursor, args=())
    th1.start();
    th2 = threading.Thread(target=ThreadCV, args=())
    th2.start();

btn_start = Button(frame_top, text='Start', command=clicked_start, bg='#d5dbf0') 
btn_start.place(relx=0.05,rely=0.05,relwidth=0.4,relheight=0.9)
btn_stop = Button(frame_top, text='Stop', command=clicked_stop, bg='#d5dbf0') 
btn_stop.place(relx=0.55,rely=0.05,relwidth=0.4,relheight=0.9)
window.mainloop()
