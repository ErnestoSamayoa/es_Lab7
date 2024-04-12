import serial
import tkinter as tk
import threading

arduino_port = 'COM3'  # Cambiar al puerto COM correcto
baud_rate = 9600

# Dimensiones del rectángulo que representa el potenciómetro
POT_WIDTH = 20
POT_HEIGHT = 200
POT_X = 300
POT_Y = 100

# Función para enviar el comando al Arduino
def send_command(command):
    ser.write(command.encode())

# Función para manejar el botón InOrden
def button_inorden_pressed():
    send_command('1')
    print("Botón InOrden de Python")
    # Cambiar el color de los círculos
    canvas.itemconfig(led_azul, fill="blue")
    canvas.itemconfig(led_rojo, fill="red")
    canvas.itemconfig(led_amarillo, fill="yellow")

# Función para manejar el botón PostOrden
def button_postorden_pressed():
    send_command('2')
    print("Botón PostOrden de Python")
    # Cambiar el color de los círculos
    canvas.itemconfig(led_azul, fill="blue")
    canvas.itemconfig(led_rojo, fill="yellow")
    canvas.itemconfig(led_amarillo, fill="red")

# Función para manejar el botón PreOrden
def button_preorden_pressed():
    send_command('3')
    print("Botón PreOrden de Python")
    # Cambiar el color de los círculos
    canvas.itemconfig(led_azul, fill="red")
    canvas.itemconfig(led_rojo, fill="blue")
    canvas.itemconfig(led_amarillo, fill="yellow")

# Función para leer datos desde Arduino en segundo plano
def leer_datos_desde_arduino():
    while True:
        if ser.in_waiting > 0:
            mensaje = ser.readline().decode().strip()
            print("Mensaje recibido desde Arduino:", mensaje)
            try:
                valor_potenciometro = int(mensaje)
                actualizar_potenciometro(valor_potenciometro)
            except ValueError:
                pass

# Función para actualizar la posición del rectángulo vertical que representa el potenciómetro
def actualizar_potenciometro(valor_potenciometro):
    # Normalizar el valor del potenciómetro al rango de la altura del rectángulo
    altura = int((valor_potenciometro / 1023) * POT_HEIGHT)
    # Calcular las coordenadas del rectángulo vertical
    y0 = POT_Y + POT_HEIGHT - altura
    y1 = POT_Y + POT_HEIGHT
    # Actualizar la posición del rectángulo vertical
    canvas.coords(rect_potenciometro, POT_X, y0, POT_X + POT_WIDTH, y1)

# Inicia la comunicación serial
ser = serial.Serial(arduino_port, baud_rate)
ser.timeout = 1  # Configura un timeout para la lectura serial

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("DashBoard")

canvas = tk.Canvas(root, width=400, height=370)
canvas.pack()

# Agregar los LEDs al canvas
led_azul = canvas.create_oval(30, 50, 80, 100, fill="white")
led_rojo = canvas.create_oval(110, 50, 160, 100, fill="white")
led_amarillo = canvas.create_oval(190, 50, 240, 100, fill="white")

# Agregar un rectángulo vertical al canvas para representar el potenciómetro
rect_potenciometro = canvas.create_rectangle(POT_X, POT_Y, POT_X + POT_WIDTH, POT_Y + POT_HEIGHT, fill="green")

# Agregar botones al canvas
button_inorden = tk.Button(root, text="InOrden", command=button_inorden_pressed)
button_inorden.place(x=20, y=200)

button_postorden = tk.Button(root, text="PostOrden", command=button_postorden_pressed)
button_postorden.place(x=100, y=200)

button_preorden = tk.Button(root, text="PreOrden", command=button_preorden_pressed)
button_preorden.place(x=180, y=200)

# Crear un hilo para leer datos de Arduino en segundo plano
thread_arduino = threading.Thread(target=leer_datos_desde_arduino)
thread_arduino.start()

# Mantener la ventana abierta
root.mainloop()
