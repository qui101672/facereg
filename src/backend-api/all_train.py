import numpy as np
import os.path
from PIL import Image
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.svm import SVC

# get the images link
def get_links(path):
    imageList = list()
    subdir_list = []
    for subdir in os.listdir(path):
        subdir_list.append(int(subdir))
    subdir_list.sort()
    print(subdir_list)
    for subdir in subdir_list:
        dirs = path + str(subdir) + "/"
        for imglinks in os.listdir(dirs):
            link = dirs + imglinks
            imageList.append(link)
    return imageList

# get embedding face
def get_embedding(model_embed, face_pixels):
    face_pixels = face_pixels.astype('float32')
    # standardlize pixel values across channels(global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    # tranform face into one sample
    samples = np.expand_dims(face_pixels, axis=0)
    # make prediction to get embedding
    yhat = model_embed.predict(samples)
    return yhat[0]

# resize the face
def resize_images(img):
    dest_size = (160, 160)
    try:
        image = Image.open(img)
        image = image.resize(dest_size)
        pixels = np.asarray(image)
        return pixels
    except:
        print(img)

# preprocess images, labels
def process_model(model, path):
    # images_file = []
    faces = []
    labels = []
    links = get_links(path)
    for link in links:
        # get extract face
        pixels = resize_images(link)
        try:
            face_embed = get_embedding(model, pixels)
            faces.append(face_embed)
            # get label
            get_label = link.split("/")
            label = get_label[-2]
            labels.append(label)
        except:
            print(link)
        # images_file.append(link)
    # encoding label
    # label_encoder = LabelEncoder()
    # encode_labels = label_encoder.fit_transform(class_name)
    # encode_labels = encode_labels.tolist()
    # encode_labels.sort()
    return faces, labels

def save_className(path):
    class_names = list()
    class_save_path = '../../processed_data/class_name.npz'
    for subdir in os.listdir(path):
        class_names.append(subdir)
    with open(class_save_path, 'wb') as class_file:
        pickle.dump(class_names, class_file, pickle.HIGHEST_PROTOCOL)

# save_className('../../data/train')
def all_train(pre_model):
    path_train = '../../data/train/'
    save_path = '../../processed_data/data_file.npz'
    X, Y = process_model(pre_model, path_train)
    # save processed data
    with open(save_path, 'wb') as outfile:
        pickle.dump((X, Y), outfile, pickle.HIGHEST_PROTOCOL)
    # start train data
    train_data = np.load('../../processed_data/data_file.npz', allow_pickle=True)
    X, y = train_data[0], train_data[1]
    model = SVC(kernel='linear', probability=True)
    model.fit(X, y)
    # save model pkl
    pkl_filename = '../../svm/faces_svm.pkl'
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)
    print("Saved model")