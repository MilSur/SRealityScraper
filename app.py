from flask import Flask, render_template
from scraper import SRealityFlatsScraper
from database import get_db
import time

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM flats;')
    flats = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', flats=flats)

if __name__ == "__main__":
    time.sleep(10) # waiting for Webdrive container to startup
    with SRealityFlatsScraper() as scraper:
        scraper.fetch_all()
    app.run(host='0.0.0.0', port=8080)