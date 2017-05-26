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
preexist=1              #画像内に人がいることを示すフラグ
j=0                     #動画の最初だけを区別するための処置
j0=0                    #butttaigaugoitatokinidousawohazimeruhuragu
mirror=False
size=None
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
        j=1
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
            humanx = int(M['m10']/M['m00'])     #人の中心座標
            humany = int(M['m01']/M['m00'])
            if preexist==0:
                if humanx>300: #and humany<350 and humany>150:    #ドアから人が出てきた時
                    peopleinroom+=1
                    print(peopleinroom)
                print('Entrance',humanx,humany)
            img_dst=cv2.circle(img_dst, (humanx,humany), 20, (255, 0, 0), -1)
            preexist=1
        else:                       #画像内に人がいない場合
            if j0==0:
                j0=1
                preexist=0
                continue

            if preexist==1:
                if humanx>300: #and humany<350 and humany>150:    #ドアから人が入っていった時
                    peopleinroom-=1
                    print(peopleinroom)
                print('Vanish  ',humanx,humany)
            preexist=0

        # 表示
        cv2.imshow("Show BACKGROUND SUBSTRACTION Image", img_dst)
        #cv2.waitKey()
    #else:break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
