import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from datetime import datetime, timedelta
import threading
import time

# Variables 
shutdown_timer = None
warning_timer = None
shutdown_time = None

def animar_aviso(label, texto):
    label.config(text=texto, foreground="#d35400")
    for alpha in range(0, 101, 10):
        label.update()
        label.tk.call(label._w, 'config', '-foreground', f'#{int(211*alpha/100):02x}{int(84*alpha/100):02x}00')
        time.sleep(0.02)

def iniciar_apagado():
    global shutdown_timer, warning_timer, shutdown_time
    try:
        horas = spin_horas.get()
        minutos = spin_minutos.get()
        if not horas.isdigit() or not minutos.isdigit():
            animar_aviso(result, "Por favor, introduce una hora válida")
            return
        horas = int(horas)
        minutos = int(minutos)
        if horas == 0 and minutos == 0:
            animar_aviso(result, "Por favor, introduce una hora válida")
            return
        total_segundos = horas * 3600 + minutos * 60
        shutdown_time = datetime.now() + timedelta(seconds=total_segundos)
        os.system(f'shutdown /s /t {total_segundos}')
        animar_aviso(result, f"El sistema se apagará en {horas}h {minutos}m.")
        cancelar.config(state=tk.NORMAL)
        if shutdown_timer:
            root.after_cancel(shutdown_timer)
        if warning_timer:
            root.after_cancel(warning_timer)
        aviso_segundos = int(total_segundos * 0.9)
        warning_timer = root.after(aviso_segundos * 1000, mostrar_aviso)
    except Exception as e:
        animar_aviso(result, "Por favor, introduce una hora válida")

def mostrar_aviso():
    messagebox.showinfo("Aviso de Apagado", "¡Queda solo el 10% del tiempo antes del apagado!")

def cancel_shutdown():
    global shutdown_timer, warning_timer
    os.system('shutdown /a')
    animar_aviso(result, "Se canceló el apagado.")
    cancelar.config(state=tk.DISABLED)
    if shutdown_timer:
        root.after_cancel(shutdown_timer)
    if warning_timer:
        root.after_cancel(warning_timer)

def set_1h():
    spin_horas.delete(0, tk.END)
    spin_horas.insert(0, '1')
    spin_minutos.delete(0, tk.END)
    spin_minutos.insert(0, '0')

def set_2h():
    spin_horas.delete(0, tk.END)
    spin_horas.insert(0, '2')
    spin_minutos.delete(0, tk.END)
    spin_minutos.insert(0, '0')

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("Temporizador de Apagado - DavidNull 🐰")
root.geometry("400x320")
root.resizable(True, True)
root.configure(bg="#181818")

try:
    icon_img = PhotoImage(file="timer_icon.png")
    root.iconphoto(True, icon_img)
except Exception:
    icon_img = None

style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#181818')
style.configure('TLabel', background='#181818', foreground='#f8f8f2', font=('Segoe UI Semibold', 11))
style.configure('TButton', font=('Segoe UI Semibold', 11, 'bold'), background='#282828', foreground='#f8f8f2', borderwidth=0, relief='flat')
style.map('TButton',
    background=[('active', '#44475a'), ('pressed', '#6272a4')],
    foreground=[('active', '#50fa7b'), ('pressed', '#f8f8f2')],
    relief=[('pressed', 'groove'), ('!pressed', 'flat')]
)
style.configure('Cancel.TButton', font=('Segoe UI Semibold', 10, 'bold'), background='#a93226', foreground='#f8f8f2', borderwidth=0, relief='flat')
style.map('Cancel.TButton',
    background=[('active', '#922b21'), ('pressed', '#641e16')],
    foreground=[('active', '#f8f8f2'), ('pressed', '#f8f8f2')],
    relief=[('pressed', 'groove'), ('!pressed', 'flat')]
)

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill='both')

label_titulo = ttk.Label(frame, text="Apagar PC", font=('Arial Rounded MT Bold', 26, 'bold'), foreground='#27ae60', background='#181818')
label_titulo.grid(row=0, column=0, columnspan=4, pady=(0, 18), sticky='ew')

label_horas = ttk.Label(frame, text="Horas:")
label_horas.grid(row=1, column=0, sticky='e', padx=(0,5))
spin_horas = tk.Spinbox(frame, from_=0, to=23, width=5, font=('Segoe UI', 12), bg='#f8f8f2', fg='#181818', insertbackground='#181818', highlightbackground='#f8f8f2', relief='flat', borderwidth=6)
spin_horas.grid(row=1, column=1, sticky='we', pady=2)

label_minutos = ttk.Label(frame, text="Minutos:")
label_minutos.grid(row=1, column=2, sticky='e', padx=(10,5))
spin_minutos = tk.Spinbox(frame, from_=0, to=59, width=5, font=('Segoe UI', 12), bg='#f8f8f2', fg='#181818', insertbackground='#181818', highlightbackground='#f8f8f2', relief='flat', borderwidth=6)
spin_minutos.grid(row=1, column=3, sticky='we', pady=2)

boton_iniciar = ttk.Button(frame, text="Iniciar Apagado", command=iniciar_apagado)
boton_iniciar.grid(row=2, column=0, columnspan=4, pady=10, sticky='ew')

result = ttk.Label(frame, text="")
result.grid(row=3, column=0, columnspan=4, pady=5, sticky='ew')

cancelar = ttk.Button(frame, text="Cancelar Apagado", command=cancel_shutdown, state=tk.DISABLED, style='Cancel.TButton')
cancelar.grid(row=4, column=3, pady=10, sticky='e')

for i in range(4):
    frame.columnconfigure(i, weight=1)
for i in range(5):
    frame.rowconfigure(i, weight=1)

for boton in [boton_iniciar, cancelar]:
    boton.configure(style=boton.cget('style') or 'TButton')
    boton.bind('<Enter>', lambda e, b=boton: b.configure(style='Hover.TButton' if b != cancelar else 'Cancel.TButton'))
    boton.bind('<Leave>', lambda e, b=boton: b.configure(style=b.cget('style') or 'TButton'))
    boton.bind('<ButtonPress>', lambda e, b=boton: b.configure(style='Pressed.TButton' if b != cancelar else 'Cancel.TButton'))
    boton.bind('<ButtonRelease>', lambda e, b=boton: b.configure(style='Hover.TButton' if b != cancelar else 'Cancel.TButton'))

style.configure('Hover.TButton', background='#44475a', foreground='#50fa7b', borderwidth=0, relief='flat')
style.configure('Pressed.TButton', background='#6272a4', foreground='#f8f8f2', borderwidth=0, relief='groove')

root.mainloop()
