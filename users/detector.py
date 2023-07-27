import os
import tensorflow as tf
# import logging
# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
# tf.get_logger().setLevel('ERROR')
import numpy as np
import urllib.request
from PIL import Image
import os.path
# Load the pre-trained Inception V3 model
# model = tf.keras.applications.InceptionV3(weights='imagenet')
from keras.models import load_model
import keras.utils as image

model = load_model('/home/DinjuVJ/tail_wise_ai/users/2023-07-18_dog_breed_model.h5')
selected_breed_list = ['scottish_deerhound',
 'maltese_dog',
 'afghan_hound',
 'entlebucher',
 'bernese_mountain_dog',
 'shih-tzu',
 'great_pyrenees',
 'pomeranian',
 'basenji',
 'samoyed',
 'airedale',
 'tibetan_terrier',
 'leonberg',
 'cairn',
 'beagle',
 'japanese_spaniel',
 'australian_terrier',
 'blenheim_spaniel',
 'miniature_pinscher',
 'irish_wolfhound',
 'lakeland_terrier',
 'saluki',
 'papillon',
 'whippet',
 'siberian_husky',
 'norwegian_elkhound',
 'pug',
 'chow',
 'italian_greyhound',
 'pembroke',
 'ibizan_hound',
 'border_terrier',
 'newfoundland',
 'lhasa',
 'silky_terrier',
 'bedlington_terrier',
 'dandie_dinmont',
 'irish_setter',
 'sealyham_terrier',
 'rhodesian_ridgeback',
 'old_english_sheepdog',
 'collie',
 'boston_bull',
 'english_foxhound',
 'bouvier_des_flandres',
 'african_hunting_dog',
 'schipperke',
 'kelpie',
 'weimaraner',
 'bloodhound',
 'bluetick',
 'saint_bernard',
 'labrador_retriever',
 'chesapeake_bay_retriever',
 'norfolk_terrier',
 'english_setter',
 'wire-haired_fox_terrier',
 'kerry_blue_terrier',
 'scotch_terrier',
 'yorkshire_terrier',
 'groenendael',
 'greater_swiss_mountain_dog',
 'irish_terrier',
 'basset',
 'keeshond',
 'west_highland_white_terrier',
 'gordon_setter',
 'malamute',
 'affenpinscher',
 'toy_poodle']
# Function to preprocess the image
def preprocess_image(image):
    image = image.resize((299, 299))  # Resize the image to the input size of Inception V3
    image = np.array(image)  # Convert PIL Image object to NumPy array
    image = image / 255.0  # Normalize pixel values to the range of 0 to 1
    image = (image - 0.5) * 2.0  # Scale pixel values to the range of -1 to 1
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image
def predict_from_image(img_path):

    img = image.load_img(img_path, target_size=(299, 299))
    img_tensor = image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]
    
    pred = model.predict(img_tensor)
    sorted_breeds_list = sorted(selected_breed_list)
    predicted_class = sorted_breeds_list[np.argmax(pred)]
    
    # plt.imshow(img_tensor[0])                           
    # plt.axis('off')
    # plt.show()

    return predicted_class, max(pred)
# Function to decode the predictions into human-readable labels
def decode_predictions(predictions):
    label = tf.keras.applications.imagenet_utils.decode_predictions(predictions, top=1)[0][0]
    return label[1]

# Function to classify the dog breed in an image
def classify_dog_breed(image_path):
    if  not os.path.isfile(image_path):
        print('Image not exist')
        return False
    # Load and preprocess the image
    # image = Image.open(image_path)
    classes, prob = predict_from_image(image_path)

    # Make predictions
    # predictions = model.predict(preprocessed_image)
    # predicted_label = decode_predictions(predictions)

    return classes

# Example usage
# image_url = 'https://iili.io/H4fdDmv.jpg'  # Replace with the URL or local path of the image you want to classify
# image_path = urllib.request.urlretrieve(image_url)[0]  # Download the image from the URL
# image_path='/home/dinju/Downloads/doge1111.jpg'
# predicted_breed = classify_dog_breed(image_path)
# print('Predicted dog breed:', predicted_breed)
