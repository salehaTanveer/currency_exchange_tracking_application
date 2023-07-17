import json
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from manage import app, scheduler
from models import ExchangeRate


@app.route("/")
def hello():
    # Test api
    return "Hello, World!"


@app.route("/exchange_rates", methods=["GET"])
def get_latest_rates():
    """
    Return a list of latest rates of all currencies.
    :return:
    """
    rates = ExchangeRate.query.all()
    rates = [rate.to_json() for rate in rates]
    return rates, 200


@app.route("/exchange_rates/compare", methods=["GET"])
def compare_rates():
    """
    Returns a list of all currencies with the new rate of today and rate of the day before.
    :return:
    """
    rates = ExchangeRate.query.all()
    rates = [rate.to_json_comparison() for rate in rates]
    return rates, 200


def update_latest_rates():
    with app.app_context():
        path = Service('/usr/bin/chromium-browser/chromedriver.exe')
        driver = webdriver.Chrome(service=path)
        driver.get(
            "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        exchange_rates = []
        table = soup.find('table', {'class': 'forextable'})
        rows = table.findAll('tr')
        for a in rows:
            data = {}
            name = a.find('td', attrs={'class': 'alignLeft'})
            abr = a.find('td', attrs={'class': 'currency'})
            rate = a.find('span', attrs={'class': 'rate'})
            if abr and abr not in data:
                data["currency"] = name.text
                data["currency_abr"] = abr.text
                data["new_rate"] = rate.text

                exchange_rates.append(data)

        ExchangeRate.upsert(exchange_rate=exchange_rates)

    return json.dumps(exchange_rates), 200


if __name__ == '__main__':
    scheduler.add_job(id='ScheduledTask', func=update_latest_rates, max_instances=1, trigger="cron",
                      day='*', hour=16, timezone='CET')
    scheduler.start()
    app.run(host="127.0.0.1", port="5000", debug=True, use_reloader=False)
