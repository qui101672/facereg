# Python libraries
###### For machine learning
- tensorflow==2.0.0
- sklearn
- Keras
- opencv(cv2)

###### For processing data 
- numpy
- pillow (PIL)
- pickle
- base64
- shutil

###### For running back-end
- flask
- flask_cors
- colorama

###### For running python back-end
- /src/backend-api/preprocess.py (run this before running server)
- /src/backend-api/apis.py (run this file)

###### For server and DB configuration
- src/backend-api/server_config.py

# For using api
- /recognition => for face recogntion

    | Parameter | Data type |
    | --- | --- |
    | image | base64 |
    
- Example recognition: 
{
    "data": {
        "message": "Successful Recognition",
        "predicted": "le hoang qui",
        "status": "1"
    }
}

- /registration => for adding a new face

    | Parameter | Data type |
    | --- | --- |
    | image[] | files |
    | name | string name |

- Example train new face:     
{
    "data": {
        "message": "Successful Added"",
        "status": "1"
    }
}


