import xdeen.services.selectors as selectors
from xdeen.config import config, reset_config
from xdeen.enums import exchanges
from xdeen.store import store


def set_up():
    reset_config()
    config['app']['considering_exchanges'] = [exchanges.SANDBOX]
    config['app']['trading_exchanges'] = [exchanges.SANDBOX]
    config['env']['exchanges'][exchanges.SANDBOX]['assets'] = [
        {'asset': 'USDT', 'balance': 2000}
    ]
    store.reset()


def test_have_correct_exchanges_in_store_after_creating_store():
    set_up()

    e = selectors.get_exchange(exchanges.SANDBOX)
    assert len(store.exchanges.storage) == 1
    assert e.assets['USDT'] == 2000
