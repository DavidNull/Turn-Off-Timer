import os
import sys
import tkinter as tk
from datetime import datetime, timedelta

def apagado_1_hora():
    tiempoapagado = datetime.now() + timedelta(hours=1)
    shutdown_system(tiempoapagado)

def apagado_2_horas():
    tiempoapagado = datetime.now() + timedelta(hours=2)
    shutdown_system(tiempoapagado)

def shutdown_system(tiempoapagado):
    segundos_apagado = int((tiempoapagado - datetime.now()).total_seconds())
    try:
        os.system(f'shutdown /s /t {segundos_apagado}')
        result.config(text=f"El sistema se apagará en {segundos_apagado} segundos.")
        cancelar.config(state=tk.NORMAL)
    except Exception as e:
        result.config(text=f"Error inesperado: {str(e)}")

def cancel_shutdown():
    os.system('shutdown /a')
    result.config(text="Se canceló el apagado.")
    cancelar.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Programa de Apagado")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

boton_1 = tk.Button(frame, text="Apagar en 1 hora", command=apagado_1_hora)
boton_1.grid(row=0, column=0, padx=5, pady=5)

boton_2 = tk.Button(frame, text="Apagar en 2 horas", command=apagado_2_horas)
boton_2.grid(row=0, column=1, padx=5, pady=5)

result = tk.Label(frame, text="")
result.grid(row=1, column=0, columnspan=2, pady=5)

cancelar = tk.Button(frame, text="Cancelar Apagado", command=cancel_shutdown, state=tk.DISABLED)
cancelar.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
