title = 'Electrum'
coin = 'Bitcoin'
coin_lower = 'bitcoin'
wallet_dir = 'Electrum'
symbol = 'BTC'
addrtype = 0
currencies = ["EUR", "USD", "GBP"]
servers = [ 'ecdsa.org:50001:t', 'electrum.novit.ro:50001:t', 'uncle-enzo.info:50001:t', 'electrum.bytesized-hosting.com:50000:t']
argument = ''

def setup_litecoin():
    global title, coin, coin_lower, wallet_dir, symbol, addrtype, currencies, servers, argument
    title = 'Electrum Litecoin'
    coin = 'Litecoin'
    coin_lower = 'litecoin'
    wallet_dir = 'ElectrumLitecoin'
    symbol = 'LTC'
    addrtype = 48
    currencies = ["BTC", "USD"]
    servers = [ 'electrum.litecoin.net:50001:t', 'electrum.bytesized-hosting.com:50002:t' ]
    argument = '--litecoin'
