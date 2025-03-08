import serial
import time

# Set up the serial connection (adjust the port and baud rate as needed)
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Update to correct port
time.sleep(2)  # Give time for Arduino to initialize

def read_arduino_data():
    if arduino.in_waiting > 0:
        # Read data from Arduino and decode it to a string
        data = arduino.readline().decode('utf-8').strip()
        return data
    return None

try:
    while True:
        # Read and print data from the Arduino
        data = read_arduino_data()
        if data:
            print(f"Received: {data}")
        time.sleep(0.1)  # Delay between reads
except KeyboardInterrupt:
    print("Exiting...")
finally:
    arduino.close()  # Close the serial connection