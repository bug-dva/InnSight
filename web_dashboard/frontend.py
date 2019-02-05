from flask import Blueprint, render_template
from flask_nav.elements import Navbar, View

from forms import AnalyzeForm
from nav import nav
import csv
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

frontend = Blueprint('frontend', __name__)


nav.register_element('frontend_top', Navbar(
    View('Airbnb Price Insight', '.index'),
    View('Home', '.index')))


@frontend.route('/', methods=('GET', 'POST'))
def index():
    form = AnalyzeForm()

    if form.validate_on_submit():
        # data = read_from_file()
        data = read_from_db(form.zipcode.data)
        print(data)
        return render_template("index.html", form=form, data=data)

    return render_template('index.html', form=form)


def read_from_file():
    with open('data.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        dict_data = []

        for line in reader:
            dict_data.append(line)

        data = {'chart_data': dict_data}

        return data

def read_from_db(zipcode):
    try:
        connection = psycopg2.connect(user=config['DEFAULT']['DB_USER'],
                                      password=config['DEFAULT']['DB_PASSWORD'],
                                      host=config['DEFAULT']['POSTGRESQL_IP'],
                                      port=config['DEFAULT']['POSTGRESQL_PORT'],
                                      database="price_insight_db")
        cursor = connection.cursor()
        query = "select * from trend_by_zipcode_sf where zipcode = '%s' order by timestamp" % zipcode
        cursor.execute(query)
        records = cursor.fetchall()

        dict_data = []
        for row in records:
            dict_data.append({
                'zipcode': str(row[0]),
                'timestamp': str(row[1]).split(' ')[0],
                'price': str(row[2])
            })

        data = {'chart_data': dict_data}

        return data
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
