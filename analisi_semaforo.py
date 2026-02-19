import csv
from datetime import datetime
 
file_csv = "eventi_led.csv"
 
conteggio_led = {}
primo_ts = None
ultimo_ts = None
 
with open(file_csv, "r") as file:
    reader = csv.reader(file)
 
    for riga in reader:
        if len(riga) != 3:
            continue
 
        timestamp_str, evento, led = riga
 
        if led not in conteggio_led:
            conteggio_led[led] = 0
        conteggio_led[led] += 1
 
        ts = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
 
        if primo_ts is None:
            primo_ts = ts
        ultimo_ts = ts
 
tempo_totale = None
if primo_ts and ultimo_ts:
    tempo_totale = ultimo_ts - primo_ts
 
print("Conteggio LED:")
for led, count in conteggio_led.items():
    print(f"  {led}: {count} volte")
 
print("\nPrimo evento:", primo_ts)
print("Ultimo evento:", ultimo_ts)
 
if tempo_totale:
    print("Tempo totale di utilizzo:", tempo_totale)
 