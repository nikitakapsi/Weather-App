from flask import Flask,render_template
import pandas as pd
app = Flask(__name__)


files =pd.read_csv("data_small/stations.txt",skiprows=17)
stations=files[['STAID', 'STANAME                                 ']]


@app.route("/")
def index():
    return render_template("home.html",data=stations.to_html())

@app.route("/api/<station>/<date>")
def about(station,date):
    filename="data_small/TG_STAID"+str(station).zfill(6)+".txt"
    df=pd.read_csv(filename,skiprows=20, parse_dates=['    DATE'])
    temp=df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return {"station":station,"date":date,"temp":temp}


@app.route("/api/<station>/")
def all_station(station):
    filename="data_small/TG_STAID"+str(station).zfill(6)+".txt"
    df=pd.read_csv(filename,skiprows=20, parse_dates=['    DATE'])
    res=df.to_dict(orient="records")

    return res

@app.route("/api/yearly/<station>/<year>")
def all_year(station,year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE']=df['    DATE'].astype(str)
    res=df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return res


if __name__ == "__main__":
    app.run(debug=True)