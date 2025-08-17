# 🔢 Handwritten Digit Recognition Web App

A real-time handwritten digit recognition application built with Python, Streamlit, and TensorFlow. This app allows users to draw digits on a canvas and get instant predictions using a trained neural network.

## ✨ Features

- **Interactive Drawing Canvas**: Draw digits using mouse or touch input
- **Real-time Prediction**: Get instant digit recognition results with ensemble methods
- **Confidence System**: View prediction confidence with adjustable threshold
- **Model Persistence**: Trained model is saved and reused (no retraining needed)
- **Clean UI**: Minimal, modern interface with responsive design
- **Visual Feedback**: See the processed image that goes into the model
- **Robust Recognition**: Better handling of rotated, scaled, and distorted digits
- **Image Preprocessing**: Automatic digit detection, cropping, and centering
- **Top 3 Predictions**: See multiple possible digits with confidence rankings
- **Training Monitoring**: Monitor model training with early stopping and learning rate scheduling

## 🏗️ Architecture

The application uses a **Convolutional Neural Network (CNN)** with the following structure:

- **Input Layer**: 28×28×1 grayscale images (MNIST format)
- **Data Augmentation**: Random rotation (±11.5°), zoom (±10%), translation (±10%), brightness, and noise
- **Initial Conv**: 7×7 convolution with 64 filters for larger receptive field
- **Residual Blocks**: Multiple residual connections with skip connections for better gradient flow
- **Batch Normalization**: Applied throughout for stable training
- **Global Pooling**: Global average pooling instead of flattening for better generalization
- **Dense Layers**: 256 → 128 neurons with progressive dropout (0.4 → 0.3)
- **Output Layer**: 10 neurons with softmax activation (digits 0-9)

## 📁 File Structure

```
project-7-digit-recognition/
├── app.py              # Main Streamlit application
├── model.h5            # Trained neural network model (auto-generated)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd project-7-digit-recognition
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL manually

## 🎯 How to Use

1. **First Run**: The app will automatically train a new model on the MNIST dataset (takes ~5-8 minutes)
2. **Subsequent Runs**: The app will load the pre-trained model instantly
3. **Drawing**: Use your mouse or touch to draw a digit (0-9) in the canvas
4. **Prediction**: Click the "🚀 Predict Digit" button to get results
5. **Results**: View the predicted digit, confidence level, and detailed confidence scores

## 🔧 Technical Details

### Model Training
- **Dataset**: MNIST (70,000 handwritten digits)
- **Training**: Up to 15 epochs with early stopping and learning rate scheduling
- **Data Augmentation**: Rotation, zoom, translation, brightness, and noise variations
- **Accuracy**: Typically achieves 98%+ accuracy on test set
- **Model Size**: ~2.5MB (efficient for web deployment)
- **Training Time**: ~5-8 minutes on first run

### Image Processing
- **Input**: User-drawn image from canvas
- **Preprocessing**: 
  - Automatic digit detection and cropping
  - Center the digit in a 28×28 canvas
  - Preserve aspect ratio during resizing
  - Contrast enhancement
  - Normalize pixel values to [0,1]
  - Invert colors (MNIST format: white digits on black background)
- **Ensemble Prediction**: Generate 5 augmented versions for robust results
- **Output**: Tensor ready for model prediction

### Performance
- **Training Time**: ~5-8 minutes on first run
- **Prediction Time**: <200ms per image (ensemble prediction with 5 versions)
- **Memory Usage**: ~800MB during training, ~300MB during inference
- **Robustness**: Better handling of rotated, scaled, and distorted digits

## 🎨 Customization

### Modifying the Model
Edit the `train_model()` function in `app.py` to:
- Change network architecture
- Adjust training parameters
- Use different optimizers or loss functions

### UI Customization
Modify the CSS styles in the `st.markdown()` section to:
- Change colors and fonts
- Adjust layout and spacing
- Add custom animations

### Adding Features
Consider adding:
- Model performance metrics
- Training history visualization
- Multiple model comparison
- Export predictions to file

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'tensorflow'"**
   - Solution: Install dependencies with `pip install -r requirements.txt`

2. **Model training fails**
   - Check internet connection (needs to download MNIST dataset)
   - Ensure sufficient RAM (>2GB available)
   - Try reducing batch size in training

3. **Canvas not working**
   - Ensure `streamlit-drawable-canvas` is installed
   - Check browser compatibility

4. **Slow performance**
   - First run includes model training (expected)
   - Subsequent runs use cached model (fast)

### System Requirements
- **Minimum**: 4GB RAM, Python 3.8+
- **Recommended**: 8GB RAM, Python 3.9+
- **OS**: Windows, macOS, or Linux

## 📚 Dependencies

- **TensorFlow 2.15.0**: Deep learning framework
- **Streamlit 1.28.1**: Web application framework
- **NumPy 1.24.3**: Numerical computing
- **Matplotlib 3.7.2**: Plotting and visualization
- **Pillow 10.0.1**: Image processing
- **streamlit-drawable-canvas 0.9.3**: Interactive drawing component

## 🤝 Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting new features
- Improving documentation
- Optimizing the model architecture

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **MNIST Dataset**: Created by Yann LeCun and Corinna Cortes
- **TensorFlow**: Google's open-source machine learning framework
- **Streamlit**: The fastest way to build data apps

---

**Happy Digit Recognition! 🎉**
