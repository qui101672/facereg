from flask import Flask, send_file, render_template
from flask_cors import CORS, cross_origin
from flask import request, jsonify
import utils
from keras.models import load_model
import numpy as np
import base64
import os
import shutil
import all_train
import server_config
import Dbconnect

# Create Flask Server Backend
app = Flask(__name__)
# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# api
@app.route('/recognition', methods=['POST', 'GET'])
@cross_origin(origin='*')
def recognize():
    anh64 = request.form.get("image")
    mess = "Something went wrong!"
    isBase64 = True
    prediction_status = 0
    predicted = ""
    # check is any user
    if len(os.listdir('../../data/train/')) <= 1:
        mess = "Please add more user"
        data = dict(message=str(mess), status=str(prediction_status), predicted=str(predicted))
        return jsonify(dict(data=data))
    is_have_svm = utils.is_have_svm()
    if is_have_svm is False:
        mess = "Please add more user"
        data = dict(message=str(mess), status=str(prediction_status), predicted=str(predicted))
        return jsonify(dict(data=data))
    # check is base64 string
    try:
        cropped_face = utils.crop_face(anh64)
        pixels = utils.resize_image(cropped_face)
    except:
        mess = "Incorrect base64 string"
        isBase64 = False
    if isBase64:
        try:
            # get face embedding
            face_emb = utils.get_embedding(model, pixels)
            face_emb = np.expand_dims(face_emb, axis=0)
            # make prediction
            predicted, status = utils.get_prediction(face_emb)
            print("predicted Name: ", predicted)
            if status is True and predicted == "":
                mess = "Database went wrong!"
            elif status is False:
                mess = "User Not Found"
            else:
                mess = "Success Recognition"
                prediction_status = 1
        except Exception as e:
            print(e)
            pass
    data = dict(message=str(mess), status=str(prediction_status), predicted=str(predicted))
    return jsonify(dict(data=data))


@app.route('/registration', methods=['POST'])
@cross_origin(origin='*')
def train():
    files = request.files.getlist("image[]")
    name = request.form.get("name")
    is_success = 0
    # check empty data
    if len(files) == 0 or name == "":
        mess = "Empty Data"
        data = dict(message=mess, status=str(is_success))
        return jsonify(dict(data=data))
    # get the id number
    data_path = '../../data/train'
    list_number_user = list()
    for number in os.listdir(data_path):
        list_number_user.append(number)
    max_number = max(list_number_user)
    max_number_db = Dbconnect.get_max_id()
    if max_number != max_number_db:
        max_number = max_number_db
    # create a user folder
    save_path = '../../data/train/' + str(max_number + 1)
    try:
        os.mkdir(save_path)
    except Exception as e:
        print("Folder create error apis-81", e)
        mess = "Can Not Add User"
        data = dict(message=mess, status=str(is_success))
        return jsonify(dict(data=data))
    # save image to folder
    for file in files:
        file.save(os.path.join(save_path, file.filename))
    # check image saved or not
    if len(os.listdir(save_path)) == 0:
        mess = "Can Not Add User Image"
        data = dict(message=mess, status=str(is_success))
        return jsonify(dict(data=data))
    # start check exist user
    is_have_svm = utils.is_have_svm()
    if is_have_svm is True:
        for link in os.listdir(save_path):
            image_path = save_path + "/" + link
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            # resize image
            pixels = utils.resize_image(encoded_string)
            # get face embedding
            face_emb = utils.get_embedding(model, pixels)
            # transper into tensor
            face_emb = np.expand_dims(face_emb, axis=0)
            # get prediction
            is_exist = utils.get_predict_label(face_emb)
            if is_exist is True:
                mess = "User is Existed"
                shutil.rmtree(save_path, ignore_errors=True)
                data = dict(message=mess, status=str(is_success))
                return jsonify(dict(data=data))
    # start extract feature
    new_labels = []
    new_embeds = []
    for link in os.listdir(save_path):
        image_path = save_path + "/" + link
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        pixels = utils.resize_image(encoded_string)
        # get face embedding
        face_emb = utils.get_embedding(model, pixels)
        new_embeds.append(face_emb)
        new_labels.append(0)
    # # check all images are the same person
    # for i in range(1, len(new_embedded)):
    #     check_result = utils.is_match(new_embedded[0], new_embedded[i])
    #     if check_result is False:
    #         shutil.rmtree(save_path, ignore_errors=True)
    #         mess = "Images are not same person"
    #         data = dict(message=mess, status=str(is_success))
    #         return jsonify(dict(data=data))
    # start training
    train_status = utils.incremental_train(name, new_embeds, new_labels)
    success_train = 1
    if train_status == success_train:
        mess = "Successful Added"
        is_success = 1
    else:
        mess = "Failed to Add"
        shutil.rmtree(save_path, ignore_errors=True)
    data = dict(message=mess, status=str(is_success))
    return jsonify(dict(data=data))


@app.route('/retrain', methods=['POST'])
@cross_origin(origin='*')
def re_train():
    train_success = False
    message = "Training not success"
    try:
        all_train.all_train(model)
        train_success = True
        message = "Training successful"
    except Exception as e:
        print("re_train error", e)
        pass
    x = dict(message=message, status=str(train_success))
    return jsonify(dict(data=x))


@app.route('/users', methods=['POST', 'GET'])
@cross_origin(origin='*')
def get_users():
    status = False
    message = "Cannot Fetch Users"
    try:
        users = Dbconnect.get_users()
        status = True
        message = "Fetch Successful"
    except:
        pass
    data = dict(message=message, status=str(status), data=users)
    return jsonify(dict(data=data))


if __name__ == '__main__':
    model = load_model('facenet_keras.h5')
    modelFile = "models/res10_300x300_ssd_iter_140000.caffemodel"
    configFile = "models/deploy.prototxt.txt"
    app.run(host=server_config.HOST, port=server_config.PORT, threaded=server_config.THREADED)
