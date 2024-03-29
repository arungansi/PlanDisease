import numpy as np
import pickle
import cv2
from os import listdir
from sklearn.preprocessing import LabelBinarizer
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation, Flatten, Dropout, Dense
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

EPOCHS = 25
INIT_LR = 1e-3
BS = 32
default_image_size = tuple((256, 256))
image_size = 0
directory_root = '../downloads/documents/archive_1/plantvillage/'
width=256
height=256
depth=3

def convert_image_to_array(image_file):
    try:
        img_file = cv2.imread(image_file)
        if img_file is not None :
            img_rsz = cv2.resize(img_file, default_image_size)   #resize the image to the desired size 
            return img_to_array(img_rsz)
        else :
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None

image_list, label_list = [], []

try:
    print("[INFO] Loading images ...")
    root_dir = listdir(directory_root)
    for directory in root_dir :
        # remove .DS_Store from list
        if directory == ".DS_Store" :
            root_dir.remove(directory)

    for plant_folder in root_dir :
        plant_disease_folder_list = listdir(f"{directory_root}/{plant_folder}")
        
        print(f"[INFO] Processing {plant_folder} ...")
        plant_disease_image_list = listdir(f"{directory_root}/{plant_folder}/")
                
        for single_plant_disease_image in plant_disease_image_list :
            if single_plant_disease_image == ".DS_Store" :
                plant_disease_image_list.remove(single_plant_disease_image)


        for image_file in plant_disease_image_list:
            image_path = f"{directory_root}/{plant_folder}/{image_file}"
            if image_path.endswith(".jpg") == True or image_path.endswith(".JPG") == True:
                image_list.append(convert_image_to_array(image_path))
                label_list.append(plant_folder)
    print("[INFO] Image loading completed")  
except Exception as e:
    print(f"Error : {e}")

print(len(image_list))

label_binarizer = LabelBinarizer()
image_labels = label_binarizer.fit(label_list)
pickle.dump(label_binarizer,open('label_transform.pkl', 'wb'))
n_classes = len(label_binarizer.classes_)

print(n_classes)

pickle.dump(image_list,open('image_list.pkl', 'wb'))

np_image_list = np.array(image_list, dtype=np.float16) / 225.0

pickle.dump(np_image_list,open('np_image_list.pkl', 'wb'))

