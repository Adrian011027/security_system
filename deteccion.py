import subprocess
import cv2
import numpy as np
import time
import os
from datetime import datetime
import sys
import tkinter as tk
from tkinter import simpledialog
import threading
from send_alert import enviar_mensaje_sms
from evaluate import predecir
import json
import requests

# Función para cargar las coordenadas desde un archivo JSON
def cargar_coordenadas():
    try:
        with open("coordenadas_area.json", "r") as archivo_json:
            coordenadas = json.load(archivo_json)
            return coordenadas["x1"], coordenadas["y1"], coordenadas["x2"], coordenadas["y2"]
    except FileNotFoundError:
        print("Error: No se encontró el archivo de coordenadas.")
        return None
    except json.JSONDecodeError:
        print("Error: No se pudo leer el archivo de coordenadas.")
        return None

# Llamamos a la función para obtener la IP de la cámara
def get_ip():
    try:
        with open("camara.json", "r") as file:
            data = json.load(file)
            return data.get("ip", "0")
    except FileNotFoundError:
        return "0"
camera_ip = get_ip()  
print(f"Camara ip = {camera_ip}")
# Si la IP no es '0', usamos la IP proporcionada, de lo contrario, usamos la cámara predeterminada
if camera_ip == "0":
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif camera_ip == "1":
    video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
else:
    video = cv2.VideoCapture(f"rtsp://{camera_ip}")  # Asegúrate de que la URL esté correcta según tu cámara

if not video.isOpened():
    print("Error: No se puede abrir la cámara.")
    exit()

# Cargar las coordenadas desde el JSON
coordenadas = cargar_coordenadas()
if coordenadas is None:
    video.release()
    exit()

x1, y1, x2, y2 = coordenadas
print(f"Área seleccionada desde JSON: ({x1}, {y1}), ({x2}, {y2})")

# Procesar video con el área seleccionada
i = 0
NUM_CAPTURES = 5
BASE_SAVE_PATH = os.path.join(os.getcwd(), "web")
motion_start_time = None
show_motion = True  # Flag para mostrar cuadros verdes

while True:
    ret, frame = video.read()
    if not ret:
        break
    hilo_activado = False

    if (x1, y1, x2, y2):
        roi = frame[y1:y2, x1:x2]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        if i == 20:
            bgGray = gray_roi
        if i > 20:
            dif = cv2.absdiff(gray_roi, bgGray)
            _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
            cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            cv2.imshow('th', th)

            motion_detected = False
            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)

                min_width = int(0.1 * (x2 - x1))
                min_height = int(0.1 * (y2 - y1))

                if w >= min_width and h >= min_height:
                    if show_motion:
                        cv2.rectangle(frame, (x1 + x, y1 + y), (x1 + x + w, y1 + y + h), (0, 255, 0), 2)
                    motion_detected = True

            # detección de movimiento
            if motion_detected:
                if motion_start_time is None:
                    motion_start_time = time.time()
                elif time.time() - motion_start_time >= 4:  # Detecta movimiento continuo por 4 segundos
                    ahora = datetime.now()
                    captures_taken = 0
                    newdir = datetime.now().strftime("%Y%m%d%H%M%S")  # variable que contiene la clave en string
                    SAVE_PATH = os.path.join(BASE_SAVE_PATH, newdir)
                    os.makedirs(SAVE_PATH, exist_ok=True)
                    for _ in range(NUM_CAPTURES):
                        ret, frame = video.read()
                        if not ret:
                            print("No se pudo capturar un nuevo cuadro. Fin del video.")
                            break
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        capture_path = f"{SAVE_PATH}\\imagen{captures_taken + 1}.jpg"
                        cv2.imwrite(capture_path, frame)  
                        print(f"Imagen guardada en: {capture_path}")
                        captures_taken += 1
                        time.sleep(1)

            
                    flag_person = predecir(SAVE_PATH, ahora)
                    
                    print(flag_person)
                    try:
                            result = subprocess.run(
                                ['node', './seed.js', newdir],
                                capture_output=True,
                                text=True,
                                check=True,
                                encoding='utf-8'  # 🔥 Esto es lo que evita el UnicodeDecodeError
                            )                            
                            print("Salida de seed.js:\n", result.stdout)
                            if result.stderr:
                                print("Errores en seed.js:\n", result.stderr)

                    except subprocess.CalledProcessError as e:
                        print("Error al ejecutar seed.js:", e.stderr)
                    except Exception as e:
                        print("Error general:", str(e))
                    print(flag_person)
                    if flag_person:
                        hilo = threading.Thread(target=enviar_mensaje_sms, args=(ahora, newdir))
                        hilo.start()
                        hilo_activado = True  # flag evita activación myultiple
                        print("\nSe envía el SMS.")
                    else:
                        print("No se detectó a ninguna persona.")
                    print("Capturas guardadas. Reiniciando detección.")
                    motion_start_time = None  # reset el tiempo de detección
            else:
                motion_start_time = None
        i += 1

        if show_motion:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
