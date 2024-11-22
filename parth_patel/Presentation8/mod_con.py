import os
import numpy as np
import pandas as pd
# from tensorflow.keras.utils import to_categorical  # use for more than 2 classes
import cv2

# Paths
labels_csv = "severity_labels.csv"
patches_dir = "/Users/parth/Desktop/Final_Presentation/patches_selected" # change to patches_selected directory

# Labels
labels_df = pd.read_csv(labels_csv)
patch_to_severity = dict(zip(labels_df["patch_grouping"], labels_df["severity"]))

# Data generator
def data_generator(batch_size, is_train=True):
    patch_groupings = list(patch_to_severity.keys())
    
    # Shuffle if training
    if is_train:
        np.random.shuffle(patch_groupings)
    
    while True:
        for i in range(0, len(patch_groupings), batch_size):
            batch_groupings = patch_groupings[i:i + batch_size]
            images = []
            labels = []
            
            for grouping in batch_groupings:
                # Load patch images
                patch_dir = os.path.join(patches_dir, grouping)
                stains = []
                for stain_file in ["stain1.tif", "stain2.tif", "stain3.tif"]:
                    stain_path = os.path.join(patch_dir, stain_file)
                    
                    # Handle missing files
                    if not os.path.exists(stain_path):
                        print(f"Warning: Missing {stain_file} in {patch_dir}")
                        continue
                    
                    stain_img = cv2.imread(stain_path, cv2.IMREAD_COLOR)
                    if stain_img is None:
                        print(f"Error: Could not load {stain_file} in {patch_dir}")
                        continue
                    
                    # Crop the stain to 400x400 (center crop)
                    # May be able to introduce padding to consistent size instead but generally patches were 400x400
                    h, w, _ = stain_img.shape
                    top = (h - 400) // 2
                    left = (w - 400) // 2
                    stain_img = stain_img[top:top + 400, left:left + 400]
                    stains.append(stain_img)
                
                # Ensure we have exactly 3 stains
                if len(stains) != 3:
                    print(f"Warning: Incomplete stains for {grouping}. Skipping.")
                    continue
                
                # Concatenate stains into a single image
                patch = np.concatenate(stains, axis=-1)  # Stain 1 (Channels 1-3): [ H&E ], Stain 2 (Channels 4-6): [ SOX10 ], Stain 3 (Channels 7-9): [ Melan-A ]
                
                images.append(patch)
                
                # Append severity label
                labels.append(patch_to_severity[grouping])
            
            # Convert to numpy arrays
            if images and labels:  # Ensure batch is not empty
                images = np.array(images, dtype="float32") / 255.0  # Normalize to [0, 1]
                labels = np.array(labels, dtype="float32")  # Keep labels as binary
                
                yield images, labels
            else:
                print("Empty batch encountered. Skipping.")



gen = data_generator(batch_size=3)

# Fetch a single batch
images, labels = next(gen)
print(f"Image batch shape: {images.shape}")  # Expected: (batch_size, 400, 400, 9) - 9 represents stain channel x RGB
print(f"Label batch shape: {labels.shape}")

# CNN model
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input

model = Sequential([
    Input(shape=(400, 400, 9)),  # Adjusted for 9 channels

    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')  # Binary
])


# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print model summary
model.summary()

batch_size = 3
epochs = 3

# Create the generator
train_gen = data_generator(batch_size=batch_size, is_train=True)

# Train the model
history = model.fit(
    train_gen,
    steps_per_epoch=len(patch_to_severity) // batch_size,  # Number of batches per epoch
    epochs=epochs
)

# Validation generator
val_gen = data_generator(batch_size=batch_size, is_train=False)

# Evaluate the model
val_loss, val_acc = model.evaluate(val_gen, steps=5)
print(f"Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_acc:.4f}")

import matplotlib.pyplot as plt

# Plot training accuracy
plt.plot(history.history['accuracy'], label='Training Accuracy')
if 'val_accuracy' in history.history:
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')
plt.show()

# Plot training loss
plt.plot(history.history['loss'], label='Training Loss')
if 'val_loss' in history.history:
    plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.show()

# Predict using the trained model
images, labels = next(train_gen)
predictions = model.predict(images)

# Convert predictions to binary classes using a threshold
threshold = 0.5
predicted_classes = (predictions > threshold).astype(int)

print("Predictions (Raw):", predictions.flatten())
print("Predicted Classes:", predicted_classes.flatten())
print("True Labels:", labels)
