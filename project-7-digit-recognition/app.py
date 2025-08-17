import streamlit as st
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
from streamlit_drawable_canvas import st_canvas
import io

# Set page configuration
st.set_page_config(
    page_title="Handwritten Digit Recognition",
    page_icon="🔢",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #1f77b4;
    }
    .confidence-bar {
        background-color: #e0e0e0;
        border-radius: 5px;
        height: 20px;
        margin: 5px 0;
    }
    .confidence-fill {
        background-color: #1f77b4;
        height: 100%;
        border-radius: 5px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_or_train_model():
    """
    Load pre-trained model if it exists, otherwise train a new one.
    Uses caching to avoid retraining on every run.
    """
    model_path = "model.h5"
    
    if os.path.exists(model_path):
        st.success("✅ Loading pre-trained model...")
        return tf.keras.models.load_model(model_path)
    else:
        st.info("🔄 Training new model... This may take a few minutes...")
        return train_model()

def train_model():
    """
    Train a sophisticated CNN model on the MNIST dataset with data augmentation.
    Returns the trained model optimized for robust digit recognition.
    """
    # Load and preprocess MNIST dataset
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    
    # Normalize pixel values to [0, 1]
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    # Reshape data for the model (add channel dimension)
    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)
    
    # Data augmentation pipeline for training
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomTranslation(0.1, 0.1),
        tf.keras.layers.RandomBrightness(0.2),
        tf.keras.layers.GaussianNoise(0.01),
    ])
    
    # CNN model with residual connections
    def residual_block(x, filters, kernel_size=3):
        """Residual block with skip connection"""
        shortcut = x
        
        # Main path
        x = tf.keras.layers.Conv2D(filters, kernel_size, padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)
        x = tf.keras.layers.Conv2D(filters, kernel_size, padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        
        # Add skip connection if dimensions match
        if shortcut.shape[-1] == filters:
            x = tf.keras.layers.Add()([shortcut, x])
        else:
            # If dimensions don't match, use 1x1 conv to match
            shortcut = tf.keras.layers.Conv2D(filters, 1, padding='same')(shortcut)
            shortcut = tf.keras.layers.BatchNormalization()(shortcut)
            x = tf.keras.layers.Add()([shortcut, x])
        
        x = tf.keras.layers.Activation('relu')(x)
        return x
    
    # Input layer
    inputs = tf.keras.Input(shape=(28, 28, 1))
    
    # Apply data augmentation during training
    x = data_augmentation(inputs)
    
    # Initial convolution with larger receptive field
    x = tf.keras.layers.Conv2D(64, 7, padding='same')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    x = tf.keras.layers.MaxPooling2D(2, 2)(x)
    
    # Residual blocks
    x = residual_block(x, 64)
    x = residual_block(x, 64)
    
    # Transition layer
    x = tf.keras.layers.Conv2D(128, 3, strides=2, padding='same')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    
    # More residual blocks
    x = residual_block(x, 128)
    x = residual_block(x, 128)
    
    # Global average pooling instead of flattening
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    
    # Dense layers with strong regularization
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    
    # Output layer
    outputs = tf.keras.layers.Dense(10, activation='softmax')(x)
    
    # Create model
    model = tf.keras.Model(inputs, outputs)
    
    # Optimizer configuration
    optimizer = tf.keras.optimizers.Adam(
        learning_rate=0.001,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-7
    )
    
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', 'top_3_accuracy']
    )
    
    # Training callbacks
    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-6,
        verbose=1
    )
    
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    # Model training
    history = model.fit(
        x_train, y_train,
        epochs=15,
        batch_size=64,
        validation_data=(x_test, y_test),
        callbacks=[lr_scheduler, early_stopping],
        verbose=1
    )
    
    # Save the trained model
    model.save("model.h5")
    st.success("✅ Model trained and saved successfully!")
    
    # Display training summary
    st.info(f"Final Training Accuracy: {history.history['accuracy'][-1]:.4f}")
    st.info(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")
    
    return model

def preprocess_image(image):
    """
    Preprocess the drawn image to match MNIST format.
    Includes center cropping, normalization, and contrast enhancement.
    """
    # Convert to grayscale if needed
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Find the bounding box of the digit (remove excess white space)
    rows = np.any(img_array < 128, axis=1)
    cols = np.any(img_array < 128, axis=0)
    
    if np.any(rows) and np.any(cols):
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        
        # Add some padding around the digit
        padding = 4
        rmin = max(0, rmin - padding)
        rmax = min(img_array.shape[0], rmax + padding)
        cmin = max(0, cmin - padding)
        cmax = min(img_array.shape[1], cmax + padding)
        
        # Crop the image to the digit area
        img_array = img_array[rmin:rmax, cmin:cmax]
    
    # Resize to 20x20 (preserve aspect ratio better)
    if img_array.size > 0:
        image_small = Image.fromarray(img_array).resize((20, 20), Image.Resampling.LANCZOS)
        img_array = np.array(image_small)
    
    # Create a 28x28 canvas with the digit centered
    canvas = np.zeros((28, 28), dtype=np.float32)
    
    if img_array.size > 0:
        # Calculate centering offsets
        y_offset = (28 - img_array.shape[0]) // 2
        x_offset = (28 - img_array.shape[1]) // 2
        
        # Place the digit in the center
        canvas[y_offset:y_offset + img_array.shape[0], 
               x_offset:x_offset + img_array.shape[1]] = img_array
    
    # Normalize to [0, 1]
    canvas = canvas.astype('float32') / 255.0
    
    # Invert colors (MNIST has white digits on black background)
    canvas = 1.0 - canvas
    
    # Apply contrast enhancement
    canvas = np.clip((canvas - 0.5) * 1.2 + 0.5, 0, 1)
    
    # Reshape for model input (add batch and channel dimensions)
    canvas = canvas.reshape(1, 28, 28, 1)
    
    return canvas

def predict_digit(model, image):
    """
    Predict the digit using ensemble methods for improved accuracy.
    Returns prediction and confidence scores.
    """
    # Create multiple augmented versions of the input image
    augmented_images = []
    
    # Original image
    augmented_images.append(image)
    
    # Create augmentation layers
    rotation_layer = tf.keras.layers.RandomRotation(0.1, fill_mode='constant', fill_value=0.0)
    zoom_layer = tf.keras.layers.RandomZoom(0.05, fill_mode='constant', fill_value=0.0)
    translation_layer = tf.keras.layers.RandomTranslation(0.05, 0.05, fill_mode='constant', fill_value=0.0)
    
    # Generate augmented versions
    for _ in range(4):  # Create 4 additional augmented versions
        aug_img = image.copy()
        
        # Apply random augmentations
        aug_img = rotation_layer(aug_img, training=True)
        aug_img = zoom_layer(aug_img, training=True)
        aug_img = translation_layer(aug_img, training=True)
        
        augmented_images.append(aug_img)
    
    # Get predictions for all versions
    all_predictions = []
    all_confidences = []
    
    for aug_img in augmented_images:
        pred = model.predict(aug_img, verbose=0)
        all_predictions.append(pred[0])
        all_confidences.append(np.max(pred[0]))
    
    # Ensemble prediction (average of all predictions)
    ensemble_pred = np.mean(all_predictions, axis=0)
    
    # Get final prediction and confidence
    predicted_digit = np.argmax(ensemble_pred)
    confidence = np.max(ensemble_pred)
    
    # Get all confidence scores for visualization
    confidence_scores = ensemble_pred
    
    # Store ensemble info for display
    st.session_state.ensemble_predictions = all_predictions
    st.session_state.ensemble_confidences = all_confidences
    
    return predicted_digit, confidence, confidence_scores

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🔢 Handwritten Digit Recognition</h1>', unsafe_allow_html=True)
    
    # Load or train model
    model = load_or_train_model()
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎨 Draw your digit here")
        st.markdown("Use your mouse or touch to draw a digit (0-9) in the canvas below:")
        
        # Create a canvas for drawing
        canvas_result = st_canvas(
            stroke_width=20,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=400,
            width=400,
            drawing_mode="freedraw",
            key="canvas"
        )
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Prediction button
        if st.button("🚀 Predict Digit", type="primary", use_container_width=True):
            if canvas_result.image_data is not None:
                # Convert canvas data to PIL Image
                canvas_image = Image.fromarray(canvas_result.image_data)
                
                # Preprocess the image
                processed_image = preprocess_image(canvas_image)
                
                # Make prediction
                predicted_digit, confidence, confidence_scores = predict_digit(model, processed_image)
                
                # Store results in session state for display
                st.session_state.prediction = predicted_digit
                st.session_state.confidence = confidence
                st.session_state.confidence_scores = confidence_scores
                st.session_state.processed_image = processed_image
                
                st.success(f"Prediction complete! Predicted digit: {predicted_digit}")
                
                # Confidence indicator
                if confidence > 0.9:
                    st.success("🎯 High confidence prediction")
                elif confidence > 0.7:
                    st.info("✅ Good confidence prediction")
                elif confidence > 0.5:
                    st.warning("⚠️ Moderate confidence - consider redrawing")
                else:
                    st.error("❌ Low confidence - try drawing more clearly")
            else:
                st.error("Please draw a digit first!")
        
        # Drawing tips
        st.markdown("---")
        st.markdown("""
        **💡 Drawing Tips:**
        - Draw digits in the center of the canvas
        - Make digits large enough to fill most of the canvas
        - Use clear, bold strokes
        - The model handles slight rotations and distortions
        """)
    
    with col2:
        st.subheader("📊 Prediction Results")
        
        # Confidence threshold slider
        confidence_threshold = st.slider(
            "Confidence Threshold", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.7, 
            step=0.05,
            help="Only show predictions above this confidence level"
        )
        
        # Display prediction if available
        if hasattr(st.session_state, 'prediction'):
            # Check if confidence meets threshold
            if st.session_state.confidence >= confidence_threshold:
                st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                st.markdown(f"**Predicted Digit:** {st.session_state.prediction}")
                st.markdown(f"**Confidence:** {st.session_state.confidence:.2%}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display confidence bar
                st.markdown("**Confidence Level:**")
                confidence_percentage = st.session_state.confidence * 100
                st.markdown(f"""
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {confidence_percentage}%"></div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show ensemble prediction info
                if hasattr(st.session_state, 'ensemble_confidences'):
                    st.markdown("**Ensemble Predictions:**")
                    avg_conf = np.mean(st.session_state.ensemble_confidences)
                    st.markdown(f"Average confidence across 5 versions: **{avg_conf:.2%}**")
                    
                    # Show individual prediction confidences
                    st.markdown("**Individual predictions:**")
                    for i, conf in enumerate(st.session_state.ensemble_confidences):
                        st.markdown(f"Version {i+1}: {conf:.2%}")
                
                # Display all digit confidences (filtered by threshold)
                st.markdown("**Confidence for each digit:**")
                for i, conf in enumerate(st.session_state.confidence_scores):
                    if conf >= confidence_threshold * 0.5:  # Show digits with reasonable confidence
                        color = "#1f77b4" if i == st.session_state.prediction else "#cccccc"
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; margin: 2px 0;">
                            <span>Digit {i}:</span>
                            <span style="color: {color}; font-weight: bold;">{conf:.3f}</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Display the processed image
                st.markdown("**Processed Image (28x28):**")
                fig, ax = plt.subplots(figsize=(4, 4))
                ax.imshow(st.session_state.processed_image[0, :, :, 0], cmap='gray')
                ax.axis('off')
                ax.set_title('Input to Model')
                st.pyplot(fig)
                plt.close()
                
                # Show top 3 predictions
                top_3_indices = np.argsort(st.session_state.confidence_scores)[-3:][::-1]
                st.markdown("**Top 3 Predictions:**")
                for rank, idx in enumerate(top_3_indices):
                    conf = st.session_state.confidence_scores[idx]
                    if rank == 0:
                        st.markdown(f"🥇 **{idx}** ({conf:.2%})")
                    elif rank == 1:
                        st.markdown(f"🥈 **{idx}** ({conf:.2%})")
                    else:
                        st.markdown(f"🥉 **{idx}** ({conf:.2%})")
            else:
                st.warning(f"⚠️ Confidence too low ({st.session_state.confidence:.2%})")
                st.markdown(f"Prediction: **{st.session_state.prediction}** (below threshold)")
                st.markdown("Try drawing the digit more clearly or adjust the confidence threshold.")
        else:
            st.info("👆 Draw a digit and click 'Predict Digit' to see results here!")
    
    # Technical information
    st.markdown("---")
    st.markdown("""
    **How it works:**
    1. **Model Training**: A CNN with residual connections is trained on MNIST with data augmentation
    2. **Image Processing**: Your drawing is automatically cropped, centered, and enhanced
    3. **Ensemble Prediction**: Multiple augmented versions are analyzed for robust results
    4. **Confidence Filtering**: Adjust the confidence threshold for prediction quality
    
    **Features:**
    - Data augmentation during training (rotation, zoom, translation, noise)
    - Residual connections for better gradient flow
    - Batch normalization for stable training
    - Ensemble methods for improved accuracy
    - Automatic digit detection and centering
    
    **Architecture**: CNN with 7x7 initial conv, residual blocks, and global pooling
    """)

if __name__ == "__main__":
    main()
