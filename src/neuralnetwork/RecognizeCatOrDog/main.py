import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import matplotlib.pyplot as plt

print("Descargando ZIP de datos")
url = 'https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip'
carpeta_zip = tf.keras.utils.get_file('cats_and_dogs_filterted.zip', origin=url, extract=True)

carpeta_base = os.path.join(os.path.dirname(carpeta_zip), 'cats_and_dogs_filtered')
carpeta_entrenamiento = os.path.join(carpeta_base, 'train')
carpeta_validacion = os.path.join(carpeta_base, 'validation')

carp_entren_gatos = os.path.join(carpeta_entrenamiento, 'cats')  
carpeta_entren_perros = os.path.join(carpeta_entrenamiento, 'dogs')  
carpeta_val_gatos = os.path.join(carpeta_validacion, 'cats')  
carpeta_val_perros = os.path.join(carpeta_validacion, 'dogs') 

num_gatos_entren = len(os.listdir(carp_entren_gatos))
num_perros_entren = len(os.listdir(carpeta_entren_perros))
num_gatos_val = len(os.listdir(carpeta_val_gatos))
num_perros_val = len(os.listdir(carpeta_val_perros))
total_entrenamiento = num_gatos_entren + num_perros_entren
total_val = num_gatos_val + num_perros_val

TAMANO_LOTE = 100
TAMANO_IMG = 150

print("Realizando aumento de datos")
image_gen_entrenamiento = ImageDataGenerator(
      rescale=1./255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')

data_gen_entrenamiento = image_gen_entrenamiento.flow_from_directory(batch_size=TAMANO_LOTE,
                                                     directory=carpeta_entrenamiento,
                                                     shuffle=True,
                                                     target_size=(TAMANO_IMG,TAMANO_IMG),
                                                     class_mode='binary')

image_gen_val = ImageDataGenerator(rescale=1./255)

data_gen_validacion = image_gen_val.flow_from_directory(batch_size=TAMANO_LOTE,
                                                 directory=carpeta_validacion,
                                                 target_size=(TAMANO_IMG, TAMANO_IMG),
                                                 class_mode='binary')

modelo = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(2)
])

modelo.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

print("Entrenando modelo...")
epocas=60
history = modelo.fit_generator(
    data_gen_entrenamiento,
    steps_per_epoch=int(np.ceil(total_entrenamiento / float(TAMANO_LOTE))),
    epochs=epocas,
    validation_data=data_gen_validacion,
    validation_steps=int(np.ceil(total_val / float(TAMANO_LOTE)))
)

print("Modelo entrenado!")