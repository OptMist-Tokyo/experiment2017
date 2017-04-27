
# coding: utf-8

# In[46]:

import cv2
import threading
from datetime import datetime

cap = cv2.VideoCapture('movie4.MOV') # iPhoneだと1920 times 1080
RATIO = 2.0 

FIRST_THREAD_COUNT = threading.activeCount() # 起動時のスレッド数（自分の環境だとなぜか5）

class FaceThread(threading.Thread): # スレッド処理をするクラス
    def __init__(self,frame):
        super(FaceThread, self).__init__()
        self._cascade_path = "haarcascades/haarcascade_profileface.xml"
        self._frame = frame
        
    def run(self):
        self._gray = cv2.cvtColor(self._frame,cv2.COLOR_BGR2GRAY)
        self._cascade = cv2.CascadeClassifier(self._cascade_path)
        self._face = self._cascade.detectMultiScale(self._gray)
        
        if len(self._face) > 0:
            #print("face is detected.")
            self._color = (255,0,0)
            for self._rect in self._face:
                cv2.rectangle(self._frame,tuple(self._rect[0:2]),tuple(self._rect[0:2] + self._rect[2:4]),self._color,thickness = 2)
                
            # 現在時間を名前に付けて写真を保存
            self._now = datetime.now().strftime("%Y%m%d-%H%M%S%f")
            self._image_path = "capture/" + self._now + ".jpg"
            cv2.imwrite(self._image_path,self._frame)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == 0:
        break
    height = int(frame.shape[0])
    width = int(frame.shape[1])
    resized_frame = cv2.resize(frame,(int(width/RATIO),int(height/RATIO))) # 動画のサイズを1/RATIOにする

    cv2.imshow("movie",resized_frame)
    
    #別スレッドが既に立ち上がっていなければ，別スレッド開始
    if(threading.activeCount() == FIRST_THREAD_COUNT): 
        th = FaceThread(resized_frame)
        th.start()
        
    c = cv2.waitKey(100) # ここに顔認識されるフレーム数が依存（つらい）
    if(c == 27):
        break # ESCで抜ける
    
cap.release()
cv2.destroyAllWindows()


# In[ ]:



