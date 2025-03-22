import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import subprocess
import os
import cv2
import json
from autenticacion import iniciar_login

def get_ip():
    try:
        with open("camara.json", "r") as file:
            data = json.load(file)
            return data.get("ip", "0")
    except FileNotFoundError:
        return "0"

def centrar_ventana(ventana, width=600, height=400):
    """ Centra la ventana justo en el centro de la pantalla """
    ventana.withdraw()  # Ocultar temporalmente para calcular bien la posición
    ventana.update_idletasks()

    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    ventana.geometry(f"{width}x{height}+{x}+{y}")
    ventana.deiconify()  # Mostrar la ventana ya centrada


def mostrar_menu():
    menu = tk.Tk()
    menu.title("Menú Principal")

    # Centrar la ventana
    centrar_ventana(menu, 600, 400)

    frame_left = tk.Frame(menu, width=300, height=400, bg="white")
    frame_left.pack(side="left", fill="both")

    try:
        script_path = os.path.join(os.path.dirname(__file__), "area.jpg")
        img = Image.open(script_path)
        img = img.resize((300, 400))
        img = ImageTk.PhotoImage(img)
        label_img = tk.Label(frame_left, image=img)
        label_img.image = img
        label_img.pack()
    except Exception as e:
        label_img = tk.Label(frame_left, text="Imagen no encontrada", bg="white")
        label_img.pack()

    frame_right = tk.Frame(menu, width=300, height=400, bg="lightgray")
    frame_right.pack(side="right", fill="both", expand=True)

    botones = ["Nueva Área", "Configuracion", "Start"]
    for boton in botones:
        if boton == "Nueva Área":
            tk.Button(frame_right, text=boton, width=20, height=2, bg="#007BFF", fg="white", font=("Helvetica", 12),
                      command=lambda: seleccionar_area(menu)).pack(pady=10)
        elif boton == "Start":
            tk.Button(frame_right, text=boton, width=20, height=2, bg="#007BFF", fg="white", font=("Helvetica", 12),
                      command=run_main_script).pack(pady=10)
        elif boton == "Configuracion":
            tk.Button(frame_right, text=boton, width=20, height=2, bg="#007BFF", fg="white", font=("Helvetica", 12),
                      command=settings).pack(pady=10)

    menu.mainloop()

def run_main_script():
    script_path = os.path.join(os.path.dirname(__file__), "deteccion.py")
    subprocess.Popen(["python", script_path], shell=True)

def settings():
    root = tk.Tk()
    root.withdraw()  

    ip = tk.simpledialog.askstring("Dirección IP", "Ingresa la dirección IP de la cámara (deja vacío para usar la cámara predeterminada):")

    if not ip:
        ip = "0"

    data = {"ip": ip}
    with open("camara.json", "w") as file: 
        json.dump(data, file, indent=4)

def seleccionar_area(menu):
    menu.destroy()

    
    camera_ip = get_ip()  
    if camera_ip == "0":
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    elif camera_ip == "1":
        video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    else:
        video = cv2.VideoCapture(f"rtsp://{camera_ip}")  # Asegúrate de que la URL esté correcta según tu cámara

    if not video.isOpened():
        messagebox.showerror("Error", "No se pudo abrir la cámara.")
        return

    for _ in range(30):
        ret, frame = video.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo leer un cuadro de la cámara.")
            video.release()
            return

    cv2.imshow('Seleccione el área de interés y presione Enter', frame)
    roi = cv2.selectROI('Seleccione el área de interés y presione Enter', frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow('Seleccione el área de interés y presione Enter')

    if roi == (0, 0, 0, 0):
        messagebox.showinfo("Información", "No se seleccionó un área.")
        video.release()
        return

    coordenadas = {
        "x1": roi[0],
        "y1": roi[1],
        "x2": roi[0] + roi[2],
        "y2": roi[1] + roi[3]
    }
    with open("coordenadas_area.json", "w") as archivo_json:
        json.dump(coordenadas, archivo_json)
    messagebox.showinfo("Información", "Coordenadas guardadas en 'coordenadas_area.json'.")

    imagen_con_recuadro = frame.copy()
    cv2.rectangle(imagen_con_recuadro, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 0, 255), 2)
    cv2.imwrite("./area.jpg", imagen_con_recuadro)
    messagebox.showinfo("Información", "Imagen con recuadro guardada como 'area.jpg'.")

    video.release()
    cv2.destroyAllWindows()
    mostrar_menu()

if __name__ == "__main__":
    iniciar_login(mostrar_menu)  # Primero inicia el login, luego llama a mostrar_menu si es exitoso
