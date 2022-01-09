import numpy as np
from sklearn.svm import SVC
from PIL import Image
import pickle
import base64
from io import BytesIO
import cv2
from numpy import load
import Dbconnect
from scipy.spatial.distance import cosine

modelFile = r"res10_300x300_ssd_iter_140000.caffemodel"
configFile = r"deploy.prototxt"


def crop_face(image):
    img64 = np.frombuffer(base64.b64decode(image), dtype=np.uint8)
    img = cv2.imdecode(img64, cv2.IMREAD_ANYCOLOR)
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 1.0, (224, 224),
                                 (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.6:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # y = startY - 10 if startY - 10 > 10 else startY + 10
            face = img[startY:endY, startX:endX]
    return face


def resize_image(array_image):
    # im_bytes = base64.b64decode(path)
    # im_file = BytesIO(im_bytes)
    # size = (160, 160)
    # image = Image.open(im_file)
    # image = image.resize(size)
    # face_array = np.asarray(image)
    face_array = cv2.resize(array_image, dsize=(160, 160), interpolation=cv2.INTER_CUBIC)
    return face_array


def get_embedding(model, pixels):
    face_pixels = pixels.astype('float32')
    # standardlize pixel values across channels(global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    # tranform face into one sample
    samples = np.expand_dims(face_pixels, axis=0)
    # make prediction to get embedding
    embedded_vector = model.predict(samples)
    return embedded_vector[0]


def get_prediction(sample):
    predicted = ""
    # load model
    pkl_filename = '../../svm/faces_svm.pkl'
    with open(pkl_filename, 'rb') as file:
        svm = pickle.load(file)
    # predict label
    y_predicted = svm.predict(sample)
    y_prob = svm.predict_proba(sample)
    is_exist = True
    passing_threshold = 0
    print(y_prob)
    # for i in y_prob[0]:
    #     if i > 0.5:
    #         print("pass")
    #         passing_threshold += 1
    #         break
    # if passing_threshold == 1:
    #     is_exist is True
    # else:
    #     check_is_exist = check_exist_user(sample, y_predicted[0])
    #     if check_is_exist == True:
    #         is_exist = True
    #     else:
    #         is_exist = False
    print(y_predicted)
    is_pass = False
    for i in y_prob[0]:
        if i > 0.7:
            print("pass")
            is_pass = True
            break
    if is_pass is False:
        check_is_exist = check_exist_user(sample, y_predicted[0])
        if check_is_exist is True:
            is_exist = True
        else:
            is_exist = False
    if is_exist is True:
        try:
            name = Dbconnect.find_user_name(int(y_predicted[0]))
            predicted = name
            print(name)
            Dbconnect.insert_checkin_log(int(y_predicted[0]))
        except Exception as e:
            print(e)
            print("Database error")
    return predicted, is_exist


def is_have_svm():
    pkl_filename = '../../svm/faces_svm.pkl'
    is_have = True
    try:
        with open(pkl_filename, 'rb') as file:
            svm = pickle.load(file)
    except Exception as e:
        print(e)
        is_have = False
        pass
    return is_have


def get_predict_label(sample):
    pkl_filename = '../../svm/faces_svm.pkl'
    with open(pkl_filename, 'rb') as file:
        svm = pickle.load(file)
    y_predicted = svm.predict(sample)
    y_prob = svm.predict_proba(sample)
    passed_threshold = 0
    for i in y_prob[0]:
        if i > 0.5:
            passed_threshold += 1
            break
    if passed_threshold == 1:
        is_exist = True
    else:
        check_is_exist = check_exist_user(sample, y_predicted[0])
        if check_is_exist is True:
            is_exist = True
        else:
            is_exist = False
    return is_exist


def check_exist_user(x_test, y_predicted):
    data = load('../../processed_data/data_file.npz', allow_pickle=True)
    x, y = data[0], data[1]
    is_exist = False
    # how many sample is true
    test_sample = 0
    total_match = 0
    chosen_user = []
    chosen_label = []
    for i in range(0, len(y)):
        if len(chosen_user) < 6:
            if y[i] == y_predicted:
                chosen_user.append(x[i])
                chosen_label.append(y[i])
            else:
                continue
    print("len user", len(chosen_user))
    for i in range(0, len(chosen_user)):
        # test_sample += 1
        result = is_match(chosen_user[i], x_test)
        if result is True:
            total_match += 1
    # for i in range(0, len(y)):
    #     if test_sample < 3:
    #         if y[i] == y_predicted:
    #             test_sample += 1
    #             result = is_match(x[i], x_test)
    #             if result is True:
    #                 total_match += 1
    #     else:
    #         break
    print("total match", total_match)
    if total_match >= 4:
        print("no dang dung")
        is_exist = True
    return is_exist


def is_match(x_train, x_test):
    thresh = 0.4
    score = cosine(x_train, x_test)
    print("score", score)
    if score <= thresh:
        return True
    return False


def is_human_face(img_for_detect):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    im_bytes = base64.b64decode(img_for_detect)
    im_file = BytesIO(im_bytes)
    image = Image.open(im_file)
    gray = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return False
    else:
        return True


def encode_img(img):
    with open(img, "rb") as image_file:
        encode_string = base64.b64encode(image_file.read())
    return encode_string


def incremental_train(name, new_emb, new_label):
    # data = load('../../processed_data/data_file.npz', allow_pickle=True)
    # get old data from file
    is_success = 0
    # get old class, labels, vectors
    old_embed, old_label = load_data()
    # start incremental training
    if len(old_label) > 0:
        try:
            print("start incremental train")
            print(old_label)
            max_number = int(max(old_label)) + 1
            new_labels = [i + max_number for i in new_label]
            new_labels = concatenate(old_label, new_labels)
            new_emb = concatenate(old_embed, new_emb)
            print("start save model")
            saving_path = '../../processed_data/data_file.npz'
            with open(saving_path, 'wb') as outfile:
                pickle.dump((new_emb, new_labels), outfile, pickle.HIGHEST_PROTOCOL)
            print(len(new_emb))
            print(len(new_labels))
            save_model()
            print("model saved")
            is_success = 1
        except Exception as e:
            print("incremental error utils-167", e)
            pass
    else:
        try:
            new_labels = concatenate(old_label, new_label)
            new_emb = concatenate(old_embed, new_emb)
            print("start save model")
            saving_path = '../../processed_data/data_file.npz'
            with open(saving_path, 'wb') as outfile:
                pickle.dump((new_emb, new_labels), outfile, pickle.HIGHEST_PROTOCOL)
            print(len(new_emb))
            print(len(new_labels))
            save_model()
            print("model saved")
            is_success = 1
        except Exception as e:
            print(e)
            pass
    if is_success == 1:
        Dbconnect.insert_user(name)
        print("inserted database")
    return is_success


def load_data():
    x_embed = []
    y_label = []
    try:
        data = load('../../processed_data/data_file.npz', allow_pickle=True)
        x_embed, y_label = data[0], data[1]
    except Exception as e:
        print("utils-196 error ", e)
        pass
    return x_embed, y_label


def concatenate(old, new):
    for i in new:
        old.append(i)
    return old


def save_data(new_embedded, new_labels):
    # save vectors and label
    class_save_path = '../../processed_data/data_file.npz'
    with open(class_save_path, 'wb') as outfile:
        pickle.dump((new_embedded, new_labels), outfile, pickle.HIGHEST_PROTOCOL)
    print("saved data")


def save_model():
    data = np.load('../../processed_data/data_file.npz', allow_pickle=True)
    X, y = data[0], data[1]
    # normalize input vectors
    model = SVC(kernel='linear', probability=True)
    model.fit(X, y)
    # save model
    try:
        with open('../../svm/faces_svm.pkl', 'wb') as file:
            pickle.dump(model, file)
    except Exception as e:
        print(e)
