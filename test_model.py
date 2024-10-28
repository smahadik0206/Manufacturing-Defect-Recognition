import cv2
import os
import numpy as np
from tensorflow import keras

# Load the Keras model
model = keras.models.load_model('./my_model2.h5')

def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    # Resize the image to match the expected input shape of the model
    resized_image = cv2.resize(image, (150, 150))
    # Normalize the pixel values (if needed)
    normalized_image = resized_image / 255.0  # Assuming the model expects values between 0 and 1
    # Return the preprocessed image
    return normalized_image

# Function to predict image quality
def predict_image_quality(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    # Reshape the image to match the input shape of the model
    input_image = np.expand_dims(preprocessed_image, axis=0)
    # Make the prediction
    prediction = (model.predict(input_image) > 0.5).astype("int32")
    # Retrieve the predicted class or quality score (adjust based on your model's output)
    predicted_quality = prediction[0][0]  # Assuming the model predicts a single value
    # Return the predicted quality
    return predicted_quality


path = 'C:/Users/digital/Documents/faulty/model/test_images'
for i in os.listdir(path):
    image_path = os.path.join(path, i)
    predicted_quality = predict_image_quality(image_path)
    print(i, predicted_quality)
    # print("Predicted image quality:", predicted_quality)

print(model.summary())