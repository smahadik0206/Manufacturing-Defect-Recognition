**Automatic Defect Recognition in Manufacturing**
This project implements a machine learning solution for automating the detection of defects in manufacturing processes. Leveraging image processing and deep learning, the model classifies product images into "defective" or "non-defective" categories, aiming to improve quality control efficiency and reduce manual inspection time.

**Features**
Image Preprocessing: Converts images to a standard format and size for model consistency.
Model Training: Trains a convolutional neural network (CNN) on labeled manufacturing defect images.
Defect Detection: Automatically identifies and classifies defects in new images.
Performance Evaluation: Assesses model accuracy, precision, and recall to ensure reliability.

**Setup and Usage**

**Install Dependencies:**
pip install -r requirements.txt

Prepare Data: Place labeled images in data/ directory with subfolders for each class.

**Train Model:**
python train.py

**Test Model:**
python test.py

**Technologies Used**
Python
TensorFlow/Keras (for CNN model)
OpenCV (for image processing)

**Results and Future Work**
The model achieves a high accuracy in defect detection and can be further optimized by tuning hyperparameters and increasing the dataset size. Future work may include real-time defect detection integration and expanding to additional defect types.
