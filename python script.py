import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# === CONFIG ===
SERIAL_PORT = 'COM6' 
BAUD_RATE = 115200
WINDOW_SIZE = 100

# === INITIALIZARE ===
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

d1_vals = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
d2_vals = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
avg_vals = deque([0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))  

# === PLOTLINES ===
line1, = ax1.plot([], [], label='Dioda 1')
line2, = ax1.plot([], [], label='Dioda 2')
line_avg, = ax2.plot([], [], label='Average', color='purple')

ax1.set_title('Diode Raw')
ax1.set_ylim(-1500, 1500)
ax1.set_xlim(0, WINDOW_SIZE)
ax1.legend()

ax2.set_title('Average')
ax2.set_ylim(-1500, 1500)
ax2.set_xlim(0, WINDOW_SIZE)
ax2.legend()

def update(frame):
    try:
        line = ser.readline().decode().strip()
        parts = line.split()
        if len(parts) == 3:
            v1, v2, avg = map(int, parts)
            d1_vals.append(v1)
            d2_vals.append(v2)
            avg_vals.append(avg)

            line1.set_data(range(len(d1_vals)), list(d1_vals))
            line2.set_data(range(len(d2_vals)), list(d2_vals))
            line_avg.set_data(range(len(avg_vals)), list(avg_vals))

    except:
        pass
    return line1, line2, line_avg

ani = animation.FuncAnimation(fig, update, interval=10, blit=True)

plt.tight_layout()
plt.show()
