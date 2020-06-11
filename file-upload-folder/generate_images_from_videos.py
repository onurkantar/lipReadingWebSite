from PIL import Image, ImageDraw
import cv2
import numpy as np
import glob
import os, shutil
import dlib
from os import listdir
from os.path import isfile, join
import datetime as dt
import time
import dlib
from random import shuffle

project_path=os.getcwd()

main_path = join(project_path,"uploads")
data_path=join(project_path,"data")
new_video_path=join(project_path,"downloads")

detector = dlib.get_frontal_face_detector() #Face detector
predictor = dlib.shape_predictor(os.path.join(project_path,"shape_predictor_68_face_landmarks.dat")) #Landmark identifier. Set the filename to whatever you named the downloaded file

def main():
    for root, dirs, files in os.walk(main_path, topdown=False):
        if root is not None:
            for file in files:
                framenumber = 1
                videoPath = join(root,file)
                videoName = str(file.split('.')[0])
                innerSavePath = data_path
                innerVideoPath = new_video_path
                cap = cv2.VideoCapture(videoPath)
                try:
                    if not os.path.exists(innerSavePath):
                        os.makedirs(innerSavePath)
                except OSError:
                    print ('Error: Creating directory of data')

                try:
                    if not os.path.exists(innerVideoPath):
                        os.makedirs(innerVideoPath)
                except OSError:
                    print ('Error: Creating directory of data')


                size = 256, 256
                while(True):
                    
                    ret, frame = cap.read()
                    if frame is None:
                        break
                    print("frame : {}".format(framenumber))
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                    clahe_image = clahe.apply(gray)

                    detections = detector(clahe_image, 1) #Detect the faces in the image

                    for k,d in enumerate(detections): #For each detected face
                        shape = predictor(clahe_image, d) #Get coordinates

                    x = []
                    y = []
                    for i in range(50,68):
                        x.append(shape.part(i).x)
                        y.append(shape.part(i).y)

                    img = Image.fromarray(frame, 'RGB')
                    crop = img.crop((min(x)-20,min(y)-20,max(x)+20,max(y)+20))
                    crop = crop.resize(size)

                    filename = str(framenumber)
                    cv2.imwrite('{}.png'.format(join(innerSavePath,filename)),np.array(crop))
                    framenumber = framenumber + 1
                
                if framenumber >= 30:
                    generate_video(innerSavePath,innerVideoPath,videoName)
                shutil.rmtree(innerSavePath,ignore_errors=True)
                cap.release()
        shutil.rmtree(main_path,ignore_errors=True)
        os.makedirs(main_path)
    return None

def generate_video(image_folder,path,video_name):
      
    images = [img for img in os.listdir(image_folder) 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 
     
    # Array images should only consider 
    # the image files ignoring others if any 
    
    plain_paths = []
    for image_path in images:
        plain_paths.append(int(image_path.split('.')[0]))

    plain_paths.sort()

    try:
        num_of_videos = int(len(plain_paths)/30)
        extra_frame = int((len(plain_paths) - (num_of_videos*30))/num_of_videos)
    except Exception:
        return None
        
    videos_list = []

    for i in range(0,num_of_videos*30,num_of_videos):
        dummy = []

        for j in range(num_of_videos):
            dummy.append(str(plain_paths[i+j]) + ".png")

        videos_list.append(dummy)

    for i in range(extra_frame):
        dummy = []

        for j in range(num_of_videos):
            dummy.append(str(plain_paths[(num_of_videos*30)+j+(i*num_of_videos)]) + ".png")

        videos_list.append(dummy)

    for i in range(num_of_videos):
        # setting the frame width, height width 
        # the width, height of first image 
        height, width, layers = 256 , 256 , 3  
    
        new_name = str(video_name) + "_" + str(i) + ".avi"
        video = cv2.VideoWriter(join(path,new_name), 0, 15, (width, height))  
    
        # Appending the images to the video one by one 
        for video_sample in videos_list:  
            video.write(cv2.imread(os.path.join(image_folder + "\\", video_sample[i])))  

        # Deallocating memories taken for window creation 
        cv2.destroyAllWindows()  
        video.release()  # releasing the video generated 

if __name__ == "__main__":
    main()