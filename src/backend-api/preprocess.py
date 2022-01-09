import numpy as np
import os.path
from PIL import Image
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from keras.models import load_model
import pickle
from sklearn.svm import SVC
from sklearn.svm import OneClassSVM


model = load_model('facenet_keras.h5')
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
def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std

    samples = np.expand_dims(face_pixels, axis=0)
    embedded_vector = model.predict(samples)
    return embedded_vector[0]

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
def process_model(path):
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
            label = int(get_label[-2])
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
    print(class_names)
    with open(class_save_path, 'wb') as class_file:
        pickle.dump(class_names, class_file, pickle.HIGHEST_PROTOCOL)


def save_compressed(embedded_vector, encode_labels, string_name):
    if os.path.exists('../../processed_data/faces_' + string_name + '_data.npz'):
        os.remove('../../processed_data/faces_' + string_name + '_data.npz')
        np.savez_compressed('../../processed_data/faces_' + string_name + '_data.npz', embedded_vector, encode_labels)
    else:
        np.savez_compressed('../../processed_data/faces_' + string_name + '_data.npz', embedded_vector, encode_labels)


# save_className('../../data/train')
path_train = '../../data/train/'
save_path = '../../processed_data/data_file.npz'
X, Y = process_model(path_train)
print(Y)

# save processed data
with open(save_path, 'wb') as outfile:
    pickle.dump((X, Y), outfile, pickle.HIGHEST_PROTOCOL)

# get test data
# path_test = '../../data/test/'
# save_test_path = '../../processed_data/test_file.npz'
# X_test, Y_test = process_model(path_test)
# with open(save_test_path, 'wb') as outfile:
#     pickle.dump((X_test, Y_test), outfile, pickle.HIGHEST_PROTOCOL)

# start train data
train_data = np.load('../../processed_data/data_file.npz', allow_pickle=True)
X, y = train_data[0], train_data[1]
# normalize input vectors
# in_encoder = Normalizer(norm='l2')
# X = in_encoder.transform(X)
model = SVC(kernel='linear', probability=True)
model.fit(X, y)
pkl_filename = '../../svm/faces_svm.pkl'
with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)
print("Saved model")

# one_class_model = OneClassSVM(gamma='auto')
# one_class_model.fit(X)
# with open('../../svm/faces_OneSvm.pkl', 'wb') as file:
#     pickle.dump(one_class_model , file)
# print("Saved one class")

# y_predicted = model.predict(X)
# conf_mat = confusion_matrix(y_predicted, y)
# acc = np.sum(conf_mat.diagonal()) / np.sum(conf_mat)
print('train all data:')
# print('Overall accuracy: {} %'.format(acc*100))
