🔢 Handwritten Digit Recognition Web App

An advanced real-time handwritten digit recognition web application built with Python, Streamlit, and TensorFlow. The app enables users to draw digits on an interactive canvas and instantly receive predictions powered by a robust convolutional neural network (CNN).

✨ Features
🎨 User Experience

Interactive Drawing Canvas: Draw digits (0-9) using mouse or touch

Instant Prediction: Real-time classification with confidence scores

Visual Feedback: Shows both raw drawing and preprocessed image used by the model

Top 3 Predictions: Displays alternative predictions with ranking

Clean UI: Minimal, modern interface with responsive layout

🧠 AI & Model Features

Convolutional Neural Network (CNN) trained on MNIST dataset

Ensemble Predictions: Multiple augmented versions for robust output

Image Preprocessing: Auto-cropping, centering, and normalization

Training Optimizations: Early stopping, learning rate scheduling

High Accuracy: ~98% accuracy on MNIST test set

🛠️ Technical Features

Streamlit Framework: Lightweight, interactive web app framework

Model Persistence: Saves trained model (model.h5) for reuse

Fast Predictions: <200ms per digit

Efficient Memory Usage: Optimized for standard laptops/desktops

🏗️ Architecture

Input: User’s handwritten digit (drawn in canvas)

Preprocessing: Resized to 28×28, centered, normalized, color-inverted

Model: CNN with residual blocks, dropout, and batch normalization

Output: Predicted digit + confidence scores

User Input → Preprocessing → CNN Model → Predictions (0–9)

📁 File Structure
project-7-digit-recognition/
├── app.py              # Main Streamlit application
├── model.h5            # Pre-trained model (auto-generated after first run)
├── requirements.txt    # Python dependencies
└── README.md           # Documentation file

🚀 Getting Started
Prerequisites

Python 3.8+

pip (Python package manager)

Installation

Clone or Download

git clone <repository-url>
cd project-7-digit-recognition


Install Dependencies

pip install -r requirements.txt


Run the Application

streamlit run app.py


Open in Browser

App runs at: http://localhost:8501

🎯 How to Use

First Run: Model will train on MNIST (~5–8 min)

Subsequent Runs: Loads saved model instantly

Draw Digit: Use canvas to draw any digit (0–9)

Predict: Click "🚀 Predict Digit" button

Results: View predicted digit, confidence %, and top-3 predictions

🔧 Customization

Model: Edit train_model() in app.py to change architecture

UI Styling: Modify CSS in st.markdown()

Training Settings: Adjust epochs, batch size, optimizer

Features to Add:

Accuracy graphs

Confusion matrix visualization

Export predictions

🐛 Troubleshooting

Error: No module named 'tensorflow'

Run: pip install -r requirements.txt

Model training too slow

Reduce epochs or batch size in train_model()

Canvas not working

Ensure streamlit-drawable-canvas is installed

Use updated Chrome/Firefox browser

📊 Performance

Accuracy: ~98% on MNIST test set

Training Time: 5–8 min on CPU

Prediction Time: <200ms

Memory Usage: ~300MB (inference), ~800MB (training)

📚 Dependencies

TensorFlow – Deep learning framework

Streamlit – Web app framework

NumPy – Numerical operations

Matplotlib – Visualizations

Pillow – Image preprocessing

streamlit-drawable-canvas – Drawing interface

🤝 Contributing

Contributions are welcome!

Report bugs

Suggest new features

Improve accuracy or UI

📄 License

This project is open-source and available under the MIT License.

🙏 Acknowledgments

MNIST Dataset: Yann LeCun & Corinna Cortes

TensorFlow: Google Brain Team

Streamlit: For making ML deployment easy

✍️ Built with ❤️ using Python, Streamlit, and TensorFlow
