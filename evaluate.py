# -*- coding: utf-8 -*-
import numpy as np
import os
import cv2
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from screeninfo import get_monitors

script_path = os.path.join(os.path.dirname(__file__), "modelo_inceptionV3_CPU.keras")
model = load_model(script_path)

def predecir(save, ahora):
    count_p = 0
    classes = {0: 'gato', 1: 'perro', 2: 'persona', 3: 'puertas'}
    image_path = save
    print(f"Imagenes en el directorio: {save}")
    
    image_files = [f for f in os.listdir(image_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    if not image_files:
        print("No se encontraron imagenes en el directorio.")
        return False

    # Obtener dimensiones de la pantalla
    screen_width = get_monitors()[0].width
    screen_height = get_monitors()[0].height

    resultados = []

    for image in image_files:
        full_path = os.path.join(image_path, image)
        print(f"Procesando imagen: {full_path}")
        
        image_bgr = cv2.imread(full_path)
        if image_bgr is None:
            print(f"Error al cargar la imagen: {full_path}")
            continue

        resized_image = cv2.resize(image_bgr, (224, 224))
        image_array = img_to_array(resized_image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        predictions = model.predict(image_array, verbose=0)[0]
        predicted_class = np.argmax(predictions)
        confidence = predictions[predicted_class] * 100
        predicted_label = classes[predicted_class]

        print(f"Prediccion: {predicted_label} ({confidence:.2f}%)")

        clase_final = "persona" if predicted_label == "persona" else "no persona"
        if clase_final == "persona":
            count_p += 1

        resultados.append({
            "filename": image,
            "clase": clase_final,
            "confidence": round(confidence, 2)
        })

        # Mostrar predicción en ventana
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5 
        thickness = 2
        color = (0, 0, 255) 
        lineas = ["Prediccion:", f"{clase_final}", f"({confidence:.2f}%)"]
        x, y = 20, 30
        dy = 40

        for i, linea in enumerate(lineas):
            cv2.putText(image_bgr, linea, (x, y + i * dy), font, font_scale, color, thickness)

        height, width, _ = image_bgr.shape
        window_name = f"Prediccion: {image}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, width, height)
        cv2.moveWindow(window_name, (screen_width - width) // 2, (screen_height - height) // 2)

        cv2.imshow(window_name, image_bgr)
        cv2.waitKey(3000)

    with open('imagenesActuales.json', 'w') as file:
        json.dump(resultados, file, indent=4)

    cv2.destroyAllWindows()
    return count_p >= 3
