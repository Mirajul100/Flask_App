from flask import Flask , render_template
import pandas as pd
import matplotlib as mt

app = Flask(__name__)

station = pd.read_csv("003 data-small/stations.txt" , skiprows=17)
station = station[["STAID","STANAME                                 "]]

@app.route("/")
def home():
    return render_template("home.html" , information=station.to_html())

@app.route("/api/v1/<station>/<data>")
def api(station , data):
    filePath =("003 data-small/TG_STAID" + str(station).zfill(6)+".txt")
    df = pd.read_csv(filePath , skiprows=20 , parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == data]["   TG"].squeeze() / 10
    result = {
        'station':station,
        'data':data,
        'temperature':temperature
    }
    return result

@app.route("/api/v1/<station>")
def stations(station):
    filePath = ("003 data-small/TG_STAID"+str(station).zfill(6)+".txt")
    df = pd.read_csv(filePath , skiprows=20 , parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station , year):
    filePath = ("003 data-small/TG_STAID" + str(station).zfill(6)+".txt")
    df = pd.read_csv(filePath , skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result

if __name__ == "__main__":
    app.run(debug=True)