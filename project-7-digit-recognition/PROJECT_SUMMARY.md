# Handwritten Digit Recognition Project

## Overview
A web application for recognizing handwritten digits using a convolutional neural network trained on the MNIST dataset.

## Project Structure
```
project-7-digit-recognition/
├── app.py              # Main Streamlit application
├── model.h5            # Trained neural network model
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore rules
```

## Key Features
- Interactive drawing canvas for digit input
- Real-time digit recognition with confidence scores
- Ensemble prediction methods for improved accuracy
- Automatic image preprocessing and centering
- Confidence threshold filtering
- Top 3 prediction rankings

## Technical Implementation
- **Framework**: Streamlit for web interface
- **Model**: CNN with residual connections and data augmentation
- **Training**: MNIST dataset with rotation, zoom, and translation augmentation
- **Architecture**: 7x7 initial conv, residual blocks, global pooling, dense layers
- **Optimization**: Adam optimizer, learning rate scheduling, early stopping

## Performance
- Training time: ~5-8 minutes (first run)
- Prediction time: <200ms per image
- Accuracy: 98%+ on test set
- Robust handling of rotated and distorted digits

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `streamlit run app.py`
3. Draw digits on canvas and click predict
4. View results with confidence scores

## Dependencies
- TensorFlow 2.12+
- Streamlit 1.25+
- NumPy, Matplotlib, Pillow
- streamlit-drawable-canvas
