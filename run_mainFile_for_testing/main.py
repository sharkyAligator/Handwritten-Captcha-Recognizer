# -*- coding: utf-8 -*-
"""Copy of Captcha_Recognition_Sigmoids_final_submission.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EeNUOuKs78EXObxuZRHchk6XKVEyFHJU
"""


import pandas as pd 
import cv2 
import imutils
import tensorflow as tf
from tensorflow import keras
import numpy as np
import glob
from PIL import Image
import os

# from google.colab.patches import cv2_imshow 
# path=str(os.getcwdb())
# print("jk")
# print(path)
# print("jk")
# img= cv2.imread(r"C:\Users\Ashish\Desktop\submission\test.jpeg",1)   # complete path of the captcha image to be recognised

img= cv2.imread("image.JPEG",1)
img6 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(img1,(5,5),0)
blur = cv2.GaussianBlur(img6,(15,15),0)           #removes disturbance, noise in image
edged = cv2.Canny(blur, 30, 150)                #canny edge detection

# kernal = np.ones((5,5),dtype=np.uint8)
kernal = np.ones((5,5),dtype=np.uint8)
dilation = cv2.dilate(edged,kernal,iterations=1)  

ht,wt=dilation.shape
defx=300                                                                      #resize image to width 300 and height in proportion
defh=defx*(ht/wt)

imgr = cv2.resize(dilation, (defx,(int)(defh)),interpolation = cv2.INTER_NEAREST)

kernal = np.ones((2,2),dtype=np.uint8)
dilation2 = cv2.dilate(imgr,kernal,iterations=1)

white = [0,0,0]
padig = cv2.copyMakeBorder(dilation2, 5, 5, 5,5, cv2.BORDER_CONSTANT,value=white)
# cv2_imshow(imgr)
cv2.imshow("image",imgr)
print(imgr.shape)

#Different operation on original image for correct contour detection
#img1 = cv2.cvtColor(imgr, cv2.COLOR_BGR2GRAY)
# cv2_imshow(img1)
#cv2.imshow("image",img1)

# blur = cv2.GaussianBlur(img1,(5,5),0)
#blur = cv2.GaussianBlur(img1,(3,3),0)           #removes disturbance, noise in image
#edged = cv2.Canny(blur, 30, 150)                #canny edge detection

# kernal = np.ones((5,5),dtype=np.uint8)
#kernal = np.ones((3,3),dtype=np.uint8)
#dilation = cv2.dilate(edged,kernal,iterations=1)  

# cv2_imshow(dilation)
#cv2.imshow("image",dilation)



#function to sort contours from left to right 

def sort_contours(cnts, method="left-to-right"): 
	reverse = False
	i = 0
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True

	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1

	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
 
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)
 


#finding contours in our captcha

cnts = cv2.findContours(padig.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

cnts = sort_contours(cnts, method="left-to-right")[0]   #Sorting contours from left to right 

oo=padig.copy()
jj=padig.copy()

#drawing bounding boxes of contours 
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
  
    roi = padig[y:y + h, x:x + w]
    #thresh = cv2.threshold(roi, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    (tH, tW) = roi.shape
    area=cv2.contourArea(c)
    
    if(area>50):
      print(area," ","###",x," ",y," ",w," ",h)
      cv2.drawContours(oo,c,-1,(255,255,255),1)
      peri=cv2.arcLength(c,True)
      approx=cv2.approxPolyDP(c,0.01*peri,True)
      x, y, w, h=cv2.boundingRect(approx)
      cv2.rectangle(jj,(x-3,y-3),(x+w+3,y+h+3),(255,255,255),1)


cv2.imshow("image",jj)

##########
#j = cv2.cvtColor(oo,cv2.COLOR_BGR2GRAY)

#ret,thresh2 = cv2.threshold(oo,127,255,cv2.THRESH_BINARY_INV)

#cv2.imshow("image",thresh2)

#kernal = np.ones((4,4),dtype=np.uint8)
#dilation1 = cv2.dilate(thresh2,kernal,iterations=1)

#cv2.imshow("image",dilation1)
##########


# new_model = tf.keras.models.load_model(r"C:\Users\Ashish\Desktop\submission\model.h5")  #imported out trained and saved model, enter full path
new_model = tf.keras.models.load_model("model.h5")
classes='ABCEFHJKMNOPSTUWXYZ1234567'                 #define a string depicted the character set taken by us

# Find contours, obtain bounding box, extract and save Region of interest(ROI)


ROI_no = 0
images = []

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    area=cv2.contourArea(c)

    if(area>50):
      ROI = oo[y-2:y+h+2, x-2:x+w+2]

      # cv2.imwrite('/content/segmented_char/ROI_{}.png'.format(ROI_no), ROI)
      images.append(ROI)
      ROI_no += 1

# image_paths = [img for img in glob.glob("/content/segmented_char/*.png")] #get paths of seperated images in captcha

# image_paths.sort()




out=""
white = [0,0,0]

for img in images:
   

    
    ht2, wt2 = img.shape

    
    if ht2>wt2:     #resizing the image in proportion 28*28, case1  height>width
      
      defh=28
      defx=defh*(wt2/ht2)
      defx = int(defx)

      new = cv2.resize(img, (defx,(int)(defh)),interpolation = cv2.INTER_NEAREST)
      
      h1,w1=new.shape

      var = h1-w1

      if var%2==0:
        new2 = cv2.copyMakeBorder(new, 0, 0, int(var/2),int(var/2), cv2.BORDER_CONSTANT,value=white)  #padding
        new3 = cv2.copyMakeBorder(new2, 1, 1, 1,1, cv2.BORDER_CONSTANT,value=white)
        new4 = cv2.resize(new3, (28,28),interpolation = cv2.INTER_NEAREST)

      else :
        new2 = cv2.copyMakeBorder(new, 0, 0, int(var/2),int(var/2)+1, cv2.BORDER_CONSTANT,value=white) #padding
        new3 = cv2.copyMakeBorder(new2, 1, 1, 1,1, cv2.BORDER_CONSTANT,value=white)
        new4 = cv2.resize(new3, (28,28),interpolation = cv2.INTER_NEAREST)


    elif wt2>ht2:       ##resizing the image in proportion 28*28, case2 width>height
      defx=28
      defh=defx*(ht2/wt2)
      defh = int(defh)

      new = cv2.resize(img, (defx,(int)(defh)),interpolation = cv2.INTER_NEAREST)
      
      h1,w1=new.shape

      var = w1-h1

      if var%2==0:
        new2 = cv2.copyMakeBorder(new, int(var/2),int(var/2),0,0, cv2.BORDER_CONSTANT,value=white) #padding
        new3 = cv2.copyMakeBorder(new2, 1, 1, 1,1, cv2.BORDER_CONSTANT,value=white)
        new4 = cv2.resize(new3, (28,28),interpolation = cv2.INTER_NEAREST)

      else :
        new2 = cv2.copyMakeBorder(new, int(var/2),int(var/2)+1,0,0,cv2.BORDER_CONSTANT,value=white) #padding
        new3 = cv2.copyMakeBorder(new2, 1, 1, 1,1, cv2.BORDER_CONSTANT,value=white)
        new4 = cv2.resize(new3, (28,28),interpolation = cv2.INTER_NEAREST)

    else:
     new2 = cv2.resize(img,(28,28), interpolation=cv2.INTER_NEAREST)
     new3 = cv2.copyMakeBorder(new2, 1, 1, 1,1, cv2.BORDER_CONSTANT,value=white) #padding
     new4 = cv2.resize(new3, (28,28),interpolation = cv2.INTER_NEAREST)

  ############################################################################################################
    
    #n = cv2.cvtColor(new2,cv2.COLOR_BGR2GRAY)
    d,m=cv2.threshold(new4,110,255,cv2.THRESH_BINARY) #converted images to binary image

    imgn = np.expand_dims(m, axis=0)   #converting array into dimension matching with inputs of model
    pred = new_model.predict(imgn)     #predicting the image
    print(pred)                      
    MaxPosition=np.argmax(pred)        #the maxmimum probability output is the ans predicted by model
    prediction_label=classes[MaxPosition]  # print the image with its 
    print(prediction_label)                # predicted output
    out = out+prediction_label         #update the answer string
    cv2.imshow("image",img)






print("The captcha predicted by model is : ")
print(out)  #Final ans, detected handwritten captcha by model


cv2.imshow("image",jj)
cv2.waitKey(0)
