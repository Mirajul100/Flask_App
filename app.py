from flask import Flask , render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

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

if __name__ == "__main__":
    app.run(debug=True)