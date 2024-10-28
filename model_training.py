import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf

# Define the path to your image folder
image_folder = 'C:/Users/digital/Documents/faulty/model/datasets/images'

# Get the list of image files in the folder
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder)]

# Load the images and labels
images = []
labels = []

for file in image_files:
    image = cv2.imread(file)
    image = cv2.resize(image, (150, 150))  # Resize the image to a specific size
    images.append(image)
    if 'NFaulty' in file:
        label = 'N'
    else:
        label = 'F'
    labels.append(label)  # Use the file name as the label

# Convert the lists to NumPy arrays
images = np.array(images)
labels = np.array(labels)

# Perform label encoding
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# Split the data into training and testing sets
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.2, random_state=42)

# Normalize the pixel values of the images
train_images = train_images / 255.0
test_images = test_images / 255.0

# Define the model architecture
model = keras.Sequential([
    keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(128, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(256, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(2, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(train_images, train_labels, epochs=10, batch_size=32, validation_data=(test_images, test_labels))

scores = model.evaluate(test_images, test_labels, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])

model.save("my_model2.h5")
