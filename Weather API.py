import pandas as pd
from flask import Flask, render_template


app = Flask(__name__)

stations = pd.read_csv('data-small/stations.txt', skiprows=17)
station_table = stations[["STAID", "STANAME                                 "]]
station_table = station_table.to_html()


@app.route('/')
def home():
    return render_template('home.html', data=station_table)


@app.route('/api/v1/<station>/<date>')
def station_date(station, date):
    filename = "data-small/TG_STAID" + station.zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == f"{date}"]['   TG'].squeeze() / 10
    return {'station': station,
            'date': date,
            'temperature': temperature}


@app.route('/api/v1/<station>/')
def only_station(station):
    filename = "data-small/TG_STAID" + station.zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient='records')
    return result


@app.route('/api/v1/year/<station>/<year>')
def one_station_one_year(station, year):
    filename = "data-small/TG_STAID" + station.zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient='records')
    return result


if __name__ == "__main__" :
    app.run(debug=True)
