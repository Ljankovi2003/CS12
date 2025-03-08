import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the serial connection (adjust the port to match your system)
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Change port if needed
time.sleep(2)  # Allow time for Arduino to initialize

# Lists to store the values
time_vals = []
gx_vals = []
gy_vals = []
gz_vals = []

# Function to read Arduino data
def read_arduino_data():
    if arduino.in_waiting > 0:
        try:
            data = arduino.readline().decode('utf-8').strip()
            if data.startswith("GX"):
                return "GX", int(data.split()[1])
            elif data.startswith("GY"):
                return "GY", int(data.split()[1])
            elif data.startswith("GZ"):
                return "GZ", int(data.split()[1])
        except ValueError:
            return None
    return None

# Live plot update function
def update(frame):
    data = read_arduino_data()
    if data:
        sensor, value = data
        time_vals.append(len(time_vals))  # Simulated time step
        if sensor == "GX":
            gx_vals.append(value)
            gy_vals.append(gy_vals[-1] if gy_vals else 0)
            gz_vals.append(gz_vals[-1] if gz_vals else 0)
        elif sensor == "GY":
            gy_vals.append(value)
            gx_vals.append(gx_vals[-1] if gx_vals else 0)
            gz_vals.append(gz_vals[-1] if gz_vals else 0)
        elif sensor == "GZ":
            gz_vals.append(value)
            gx_vals.append(gx_vals[-1] if gx_vals else 0)
            gy_vals.append(gy_vals[-1] if gy_vals else 0)

        # Keep only last 100 points
        if len(time_vals) > 100:
            time_vals.pop(0)
            gx_vals.pop(0)
            gy_vals.pop(0)
            gz_vals.pop(0)

        # Clear and redraw the plot
        ax.clear()
        ax.plot(time_vals, gx_vals, label="GX", color="red")
        ax.plot(time_vals, gy_vals, label="GY", color="green")
        ax.plot(time_vals, gz_vals, label="GZ", color="blue")

        ax.set_xlabel("Time Steps")
        ax.set_ylabel("Gyro Values")
        ax.set_title("Live Gyroscope Data (GX, GY, GZ)")
        ax.legend()
        ax.grid()

# Setup Matplotlib figure
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, interval=100)  # Update every 100ms

try:
    plt.show()
except KeyboardInterrupt:
    print("Exiting...")
    arduino.close()
