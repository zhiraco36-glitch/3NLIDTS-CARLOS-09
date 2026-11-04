import tkinter as tk 
from tkinter import messagebox
import serial
import time
import threading


arduino_port = "COM3"
baud_rate = 9600
arduino = None


def conectar():
    global arduino 
    try:
        arduino = serial.Serial(arduino_port, baud_rate)
        time.sleep(2)
        lbConection.config(text="estado: conectado", fg="green")
        messagebox.showinfo("conexion","conexion establecida.")
        start_reading()
    except serial.SerialException:
        messagebox.showerror("Error", "nose puede conectar al arduino. Verifique")


def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        lbConection.config(text="Estado: Desconectado", fg="red")
        messagebox.showinfo("conexion","Conexio terminada.")
    else:
        messagebox.showwarning("advertencia", "No hay conexion activa.")


def enviar_limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = tbLimTemp.get()
            if limite.isdigt():
               arduino.write(f"{limite}\n".encode())
               messagebox.showinfo("Enviado",f"Limite de temperatura ({limite}c)enviado.")
            else:
                messagebox.showerror("error","imgrese un valor numerico para el limite.")
        except Exception as e:
          messagebox.showerror("Error",f"no se pudo enviar el limite:{e}")
    else:
        messagebox.showwarning("advertencia","conectese ala arduino antes de enviar el limite.")


def read_from_arduino():
    global arduino 
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip()
            if "temperatura" in data:
                temp_value = data.split(":")[1].strip().split(" ")[0]
                lbTemp.config(text=f"{temp_value} c")
            time.sleep(1)
        except Exception as e:
            print(f"error leyendo datos: {e}")
            break


def start_reading():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()


root = tk.Tk()
root.title("interfaz de monitoreo de temperatura")
root.geometry("300x350")


lbTitleTemp = tk.Label(root, text ="temperatura actual", font =("Arial",12))
lbTitleTemp.pack(pady=10)


lbTemp = tk.Label(root,text="--c", font=("Arial",24))
lbTemp.pack()


lbConection = tk.Label(root, text="Estado: Desconectado", fg="red",font=("Arial",10))
lbConection.pack(pady=5)


lbLimitTemp = tk.Label(root, text="Limite de temperatura:" )
lbLimitTemp.pack(pady=5)
tbLimTemp = tk.Entry(root, width=10)
tbLimTemp.pack(pady=5)


btnEnviar = tk.Button(root, text= "Enviar Limite", command=enviar_limite, font=("Arial",10))
btnEnviar.pack(pady=5)


btnConectar = tk.Button(root, text = "conectar",command= conectar, font=("Arial",10))
btnConectar.pack(pady=5)


btnDesconectar = tk.Button(root, text="Desconectar", command=desconectar, font=("Arial", 10))
btnDesconectar.pack(pady=5)

root.mainloop
