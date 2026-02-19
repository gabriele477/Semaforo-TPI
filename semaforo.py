import serial
from datetime import datetime
import csv
 
porta = "COM10"
tempo = 9600
 
ser = serial.Serial(porta, tempo)
 
with open("eventi_led.csv", "a", newline="") as file:
    writer = csv.writer(file)
 
    while True:
        linea = ser.readline().decode().strip()
 
        if "," not in linea:
            continue
 
        evento, led = linea.split(",")
 
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
        writer.writerow([timestamp, evento, led])
        file.flush()
 
        print(timestamp, evento, led)