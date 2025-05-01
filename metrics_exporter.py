from flask import Flask, Response
from prometheus_client import Gauge, generate_latest
import pandas as pd
import glob

app = Flask(__name__)

# Prometheus Gauges
red_count = Gauge('red_entries', 'Number of red tagged entries')
green_count = Gauge('green_entries', 'Number of green tagged entries')

@app.route('/metrics')
def metrics():
    # Read all CSVs in output_files
    all_files = glob.glob("output_files/part-*.csv")
    df_list = [pd.read_csv(f, header=None, names=["timestamp", "service", "latency", "status_code", "color"]) for f in all_files]
    
    if df_list:
        df = pd.concat(df_list)
        red = len(df[df["color"] == "red"])
        green = len(df[df["color"] == "green"])
        red_count.set(red)
        green_count.set(green)
    
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)