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
model = tf.keras.applications.InceptionV3(weights='imagenet')

# Function to preprocess the image
def preprocess_image(image):
    image = image.resize((299, 299))  # Resize the image to the input size of Inception V3
    image = np.array(image)  # Convert PIL Image object to NumPy array
    image = image / 255.0  # Normalize pixel values to the range of 0 to 1
    image = (image - 0.5) * 2.0  # Scale pixel values to the range of -1 to 1
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

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
    image = Image.open(image_path)
    preprocessed_image = preprocess_image(image)

    # Make predictions
    predictions = model.predict(preprocessed_image)
    predicted_label = decode_predictions(predictions)

    return predicted_label

# Example usage
# image_url = 'https://iili.io/H4fdDmv.jpg'  # Replace with the URL or local path of the image you want to classify
# image_path = urllib.request.urlretrieve(image_url)[0]  # Download the image from the URL
# image_path='/home/dinju/Downloads/doge1111.jpg'
# predicted_breed = classify_dog_breed(image_path)
# print('Predicted dog breed:', predicted_breed)
