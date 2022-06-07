from PIL import Image
from numpy import asarray
import numpy as np
import json
import requests
# import tensorflow as tf
# from tensorflow.keras import layers

SIZE=224
MODEL_URI='https://cruise-eyecoffee.herokuapp.com/v1/models/img_classifier:predict'
CLASSES = ["Rust","Healthy","Miner","Red Spider Mite"]


def get_prediction(image_path):
    # use PIL and numpy only
    image =  np.array(Image.open(image_path).resize((SIZE,SIZE)))    
    img = asarray(image)
    img = img.reshape(1, SIZE, SIZE, 3)
    img = img.astype('float32')
    img_rescaled = img / 255.0
    
    # not using tensorflow and keras layers because it will slow down the entire process
    # image =  np.array(Image.open(image_path).resize((SIZE,SIZE)))  
    # img_batch = tf.expand_dims(image, axis=0)
    # img_rescaled = layers.experimental.preprocessing.Rescaling(1./255)(img_batch)
    
    mydata = json.dumps({
        'instances': img_rescaled.tolist()
    })

    response = requests.post(MODEL_URI , data=mydata)
    result = json.loads(response.text)
    predictionList = result['predictions'][0]
    predictionIdx = predictionList.index(max(predictionList))
    return {"class_name":CLASSES[predictionIdx] , "percentage":max(predictionList)}
