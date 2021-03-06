# -*- coding: utf-8 -*-
"""final_intruder_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13DUI9XfGutQUODGfdRclOnKl3aRe77Ca

Clone and Build Darknet
- clone darknet repo (AlexeyAB)
- change makefile to have GPU and OPENCV enabled 
- make darknet
"""

!git clone https://github.com/AlexeyAB/darknet

# Commented out IPython magic to ensure Python compatibility.
# change makefile settings to enable GPU and OPENCV
# %cd darknet 
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile

# CUDA verification
!/usr/local/cuda/bin/nvcc --version

# make darknet
!make

"""Define helper functions """

# Commented out IPython magic to ensure Python compatibility.
def imShow(path):
  import cv2
  import matplotlib.pyplot as plt
#   %matplotlib inline 

  image = cv2.imread(path)
  height, width = image.shape[:2]
  resized_image = cv2.resize(image,(3*width, 3*height), interpolation = cv2.INTER_CUBIC)

  fig = plt.gcf()
  fig.set_size_inches(18,10)
  plt.axis("off")
  plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
  plt.show()

def upload():
  from google.colab import files 
  uploaded = files.upload()
  for name, data in uploaded.items():
    f.write(data)
    print('saved file', name)

def download(path):
  from google.colab import files 
  files.download(path)

"""

Set up google drive"""

# Commented out IPython magic to ensure Python compatibility.
# %cd .. 
from google.colab import drive 
drive.mount('/content/gdrive')

# link created, /content/gdrive/My\ Drive/ is equal to /mydrive
!ln -s /content/gdrive/My\ Drive/ /mydrive
!ls /mydrive

# Commented out IPython magic to ensure Python compatibility.
# %cd darknet

"""Training Stage - Custom YOLOv3 Object Detector

- upload custom dataset into Cloud
"""

# check where dataset is stored (zip file)
!ls /mydrive/final_results_yolov3

# copy .zip file into root directory of cloud VM
!cp /mydrive/final_results_yolov3/obj.zip ../

# unzip file (located in /darknet/data/obj)
!unzip ../obj.zip -d data/

!cp /mydrive/final_results_yolov3/test.zip ../
!unzip ../test.zip -d data/

"""- configure files for training

a) cfg file
"""

# copy yolov3.cfg to edit 
!cp cfg/yolov3.cfg /mydrive/final_results_yolov3/yolov3_custom2.cfg

# edit cfg file in a separate text editor

# upload custom .cfg back into cloud VM 
!cp /mydrive/final_results_yolov3/yolov3_custom.cfg ./cfg

"""b) obj.names and obj.data"""

# create new files obj.names and obj.data in a separate text editor

# upload obj.names and obj.data files to cloudVM from drive 

!cp /mydrive/final_results_yolov3/obj.names ./data 
!cp /mydrive/final_results_yolov3/obj.data ./data

"""c) generate train.txt and test.txt

train.txt will hold all paths to our training images, and test.txt will be used to test the performance of our model 
"""

# upload generate_train.py script to cloud VM from google drive 
!cp /mydrive/final_results_yolov3/generate_train.py ./

#upload generate_test.py script to cloud VM from google drive
!cp /mydrive/final_results_yolov3/generate_test.py ./

# run python scripts

!python generate_train.py
!python generate_test.py

!ls data/

"""Download pre-trained weights for convolutional layers 




- this will help the object detector be more accurate and require less training time. Helps the model converge faster 
"""

# upload pretrained convolutional layer weights 

!wget http://pjreddie.com/media/files/darknet53.conv.74

"""Train custom object detector """

# train custom detector 

!./darknet detector train data/obj.data cfg/yolov3_custom.cfg darknet53.conv.74 -dont_show

# if runtime crashes, use backed up weights to pick up training where you left off 

!./darknet detector train data/obj.data cfg/yolov3_custom.cfg /mydrive/final_results_yolov3/backup/yolov3_custom_last.weights -dont_show

# accuracy?

!./darknet detector map data/obj.data cfg/yolov3_custom.cfg /mydrive/final_results_yolov3/backup/yolov3_custom_last.weights

"""Run Custom Object Detector """

# Commented out IPython magic to ensure Python compatibility.
# set custom cfg to test mode 

# %cd cfg
!sed -i 's/batch=64/batch=1/' yolov3_custom.cfg
!sed -i 's/subdivisions=16/subdivisions=1/' yolov3_custom.cfg
# %cd ..

# run your custom detector with this command (upload an image to your google drive to test, thresh flag sets accuracy that detection must be in order to show it)
!./darknet detector test data/obj.data cfg/yolov3_custom.cfg /mydrive/final_results_yolov3/backup/yolov3_custom_last.weights /mydrive/final_results_yolov3/images/bikers.jpg -thresh 0.3
imShow('predictions.jpg')
