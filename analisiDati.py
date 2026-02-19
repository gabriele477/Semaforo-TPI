import dearpygui.dearpygui as dpg
import csv
from datetime import datetime
import os

def carica_dati():
    file_csv = "dati_semaforo.csv"
    if not os.path.exists(file_csv):
        return {}, None, None, None

    conteggio_led = {}
    primo_ts = None
    ultimo_ts = None

    with open(file_csv, "r") as file:
        reader = csv.reader(file)
        for riga in reader:
            if len(riga) != 3:
                continue
            
            timestamp_str, evento, led = riga
            nome_led = f"LED {led}"
            
            conteggio_led[nome_led] = conteggio_led.get(nome_led, 0) + 1
            ts = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            
            if primo_ts is None: primo_ts = ts
            ultimo_ts = ts

    tempo_totale = ultimo_ts - primo_ts if primo_ts and ultimo_ts else "N/A"
    return conteggio_led, primo_ts, ultimo_ts, tempo_totale

def aggiorna_interfaccia():
    conteggi, inizio, fine, totale = carica_dati()
    
    # Aggiorna Testi
    dpg.set_value("testo_inizio", f"Primo evento: {inizio}")
    dpg.set_value("testo_fine", f"Ultimo evento: {fine}")
    dpg.set_value("testo_totale", f"Tempo totale: {totale}")
    
    # Aggiorna Istogramma
    labels = list(conteggi.keys())
    valori = [float(v) for v in conteggi.values()]
    dpg.set_value("serie_barre", [labels, valori])

# Setup Dear PyGui
dpg.create_context()

with dpg.window(label="Analisi Dati Semaforo", width=600, height=500):
    dpg.add_button(label="Aggiorna Dati", callback=aggiorna_interfaccia)
    dpg.add_separator()
    
    with dpg.group(horizontal=True):
        with dpg.child_window(width=250, height=120):
            dpg.add_text("Statistiche Temporali")
            dpg.add_text("Nessun dato", tag="testo_inizio", color=[150, 255, 150])
            dpg.add_text("Nessun dato", tag="testo_fine", color=[255, 150, 150])
            dpg.add_text("Nessun dato", tag="testo_totale")

    dpg.add_spacer(height=10)
    dpg.add_text("Distribuzione Utilizzo LED")
    
    with dpg.plot(label="Conteggio Attivazioni", height=-1, width=-1):
        dpg.add_plot_legend()
        asse_x = dpg.add_plot_axis(dpg.mvXAxis, label="LED", no_gridlines=True)
        asse_y = dpg.add_plot_axis(dpg.mvYAxis, label="Volte")
        dpg.add_bar_series([], [], label="Attivazioni", parent=asse_y, tag="serie_barre")

dpg.create_viewport(title='Dashboard Analisi Arduino', width=620, height=540)
dpg.setup_dearpygui()
dpg.show_viewport()

# Caricamento iniziale
aggiorna_interfaccia()

dpg.start_dearpygui()
dpg.destroy_context()