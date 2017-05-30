# -*- coding: UTF-8 -*- 

# -*- coding: UTF-8 -*- 

 
import cv2
import math 
import numpy as np 
import os

#mp4_path = './mp4/beranda.mp4'
#print mp4_path  
#cap = cv2.VideoCapture(mp4_path)
peopleinroom=0          #部屋の人数
peopleinscreen=0    
preexist=1              #画像内に人がいることを示すフラグ
j=0                     #動画の最初だけを区別するための処置
j0=0                    #butttaigaugoitatokinidousawohazimeruhuragu
mirror=False
size=None
delta=50                #radiaus of human
humanxs=[]
"""Capture video from camera"""
# カメラをキャプチャする
cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号
while(cap.isOpened()):
    #ret, frame = cap.read()
    #if ret:
        #動画内の連続する2コマを取り出す
    #    if j:
    #        img_src1 = img_src2 
    #    img_src2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[0:720,100:540]
    #    if j==0:
    #        j=1
    #        continue
    #    j+=1



    #while True:
        # retは画像を取得成功フラグ
        ret, frame = cap.read()

        # 鏡のように映るか否か
        if mirror is True:
            frame = frame[:,::-1]

        # フレームをリサイズ
        # sizeは例えば(800, 600)
        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)
        if j:
            img_src1 = img_src2 
        img_src2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[0:100,0:600]
        #print j
        if j==0:
            j=1
            continue
        j+=1
        if j==150:
            j=1
            f = open('text.txt', 'w') # 書き込みモードで開く
            f.writelines(str(peopleinroom)) # シーケンスが引数。
            f.close()
        # フレームを表示する
        #cv2.imshow('camera capture', frame)

        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            break

     
        # 背景画像との差分を算出
        img_diff = cv2.absdiff(img_src2, img_src1)
     
        # 差分を二値化
        img_diffm = cv2.threshold(img_diff, 20, 255, cv2.THRESH_BINARY)[1]
     
         
        # 膨張処理、収縮処理を施してマスク画像を生成
        operator = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_diffm, operator, iterations=4)
        img_mask = cv2.erode(img_dilate, operator, iterations=4)
     
        # マスク画像を使って対象を切り出す
        img_dst = cv2.bitwise_and(img_src2, img_mask)
         
    
        #表示画像の作成
        if np.mean(img_dst)>3:      #画像内に人がいる場合
            #モーメントから人の位置を求める
            M=cv2.moments(img_dst)
            meanx = int(M['m10']/M['m00'])     #人の中心座標
            meany = int(M['m01']/M['m00'])
            variance=int(M['m20']/M['m00']-(M['m10']/M['m00'])**2)             
            #print 'variance:',variance

            if variance>(2*delta)**2:       #if humaninscreen=2
                humanxr=int(meanx+((variance-delta**2)/2)**0.5)
                humanxl=int(meanx-((variance-delta**2)/2)**0.5)
                #print humanxr,humanxl
                
                if peopleinscreen==1:
                    if math.fabs(prehumanx-humanxr)<math.fabs(prehumanx-humanxl):
                        newx=humanxr
                    else: 
                        newx=humanxl
                    if newx>300: #and humany<350 and humany>150:    #ドアから人が出てきた時
                        peopleinroom+=1
                        print(peopleinroom)
                        print ('Entrance',newx)
                    img_dst=cv2.circle(img_dst, (humanxr,meany), 20, (255, 0, 0), -1)
                    img_dst=cv2.circle(img_dst, (humanxl,meany), 20, (255, 0, 0), -1)
                peopleinscreen=2
                    
            else:
                if peopleinscreen==2:
                    if math.fabs(meanx-humanxr)<math.fabs(meanx-humanxl):
                        oldx=humanxl
                    else: 
                        oldx=humanxr
                    if oldx>300: #and humany<350 and humany>150:    #ドアから人が入っていった時
                        peopleinroom-=1
                        print(peopleinroom)
                        print('Vanish  ',meanx,meany)
                if preexist==0:
                    if meanx>300: #and humany<350 and humany>150:    #ドアから人が出てきた時
                        peopleinroom+=1
                        print(peopleinroom)
                    print('Entrance',meanx,meany)
                    img_dst=cv2.circle(img_dst, (meanx,meany), 20, (255, 0, 0), -1)
                peopleinscreen=1
                prehumanx=meanx
                preexist=1 
        else:                       #画像内に人がいない場合
            peopleinscreen=0
            if j0==0:
                j0=1
                preexist=0
                continue
            
            if preexist==1:
                if meanx>300: #and humany<350 and humany>150:    #ドアから人が入っていった時
                    peopleinroom-=1
                    print(peopleinroom)
                print('Vanish  ',meanx,meany)
            preexist=0

        # 表示
        cv2.imshow("Show BACKGROUND SUBSTRACTION Image", img_dst)
        #cv2.waitKey()
    #else:break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
