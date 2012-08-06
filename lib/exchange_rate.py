from PyQt4.QtCore import SIGNAL
import decimal
import httplib
import json
import threading
import config

class Exchanger(threading.Thread):

    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent
        self.quote_currencies = None
        self.lock = threading.Lock()
        # Do price discovery
        self.start()

    def exchange(self, btc_amount, quote_currency):
        with self.lock:
            if self.quote_currencies is None:
                return None
            quote_currencies = self.quote_currencies.copy()
        if quote_currency not in quote_currencies:
            return None
        return btc_amount * quote_currencies[quote_currency]

    def run(self):
        self.discovery()

    def discovery(self):
        if config.coin == 'Bitcoin':
            connection = httplib.HTTPSConnection('intersango.com')
            connection.request("GET", "/api/ticker.php")
            response = connection.getresponse()
            if response.status == 404:
                return
            response = json.loads(response.read())
            # 1 = BTC:GBP
            # 2 = BTC:EUR
            # 3 = BTC:USD
            # 4 = BTC:PLN
            quote_currencies = {}
            try:
                quote_currencies["GBP"] = self.lookup_rate(response, 1)
                quote_currencies["EUR"] = self.lookup_rate(response, 2)
                quote_currencies["USD"] = self.lookup_rate(response, 3)
                with self.lock:
                    self.quote_currencies = quote_currencies
                self.parent.emit(SIGNAL("refresh_balance()"))
            except KeyError:
                pass
        elif config.coin == "Litecoin":
            quote_currencies = {}

            # LTC/BTC - https://btc-e.com/api/2/10/ticker
            connection = httplib.HTTPSConnection('btc-e.com')
            connection.request("GET", "/api/2/10/ticker")
            response = connection.getresponse()
            if response.status != 404:
                response = json.loads(response.read())
                try:
                    quote_currencies["BTC"] = decimal.Decimal(response["ticker"]["last"])
                except KeyError:
                    pass

            # LTC/USD - https://btc-e.com/api/2/14/ticker
            connection = httplib.HTTPSConnection('btc-e.com')
            connection.request("GET", "/api/2/14/ticker")
            response = connection.getresponse()
            if response.status != 404:
                response = json.loads(response.read())
                try:
                    quote_currencies["USD"] = decimal.Decimal(response["ticker"]["last"])
                except KeyError:
                    pass

            self.quote_currencies = quote_currencies
            self.parent.emit(SIGNAL("refresh_balance()"))

    def lookup_rate(self, response, quote_id):
        return decimal.Decimal(response[str(quote_id)]["last"])

if __name__ == "__main__":
    exch = Exchanger(("EUR", "USD", "GBP"))
    print exch.exchange(1, "EUR")

