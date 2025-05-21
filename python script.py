import serial
import time
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configurație port serial (modifică după caz)
SERIAL_PORT = 'COM3'       # sau '/dev/ttyUSB0' pe Linux
BAUD_RATE = 115200

# Inițializează buffer pentru grafic
BUFFER_SIZE = 100
data_buffer = deque([0]*BUFFER_SIZE, maxlen=BUFFER_SIZE)

# Inițializează graficul
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 4095)   # ADC pe 12 biți
ax.set_xlim(0, BUFFER_SIZE)
ax.set_title("Semnal de la ESP32")
ax.set_ylabel("Valoare ADC")
ax.set_xlabel("Timp (ultimele N puncte)")

def update_plot(frame):
    global ser
    try:
        line_raw = ser.readline().decode().strip()
        if line_raw.startswith("CH"):
            val = float(line_raw.split(":")[1])
            data_buffer.append(val)
            line.set_data(range(len(data_buffer)), list(data_buffer))
    except:
        pass
    return line,

# Deschide conexiunea serială
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Așteaptă pornirea ESP-ului

# Pornește animația
ani = animation.FuncAnimation(fig, update_plot, interval=50)
plt.tight_layout()
plt.show()

# Închide portul serial când se termină
ser.close()
