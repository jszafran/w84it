from collections import namedtuple

Currency = namedtuple('CURRENCY', ['location', 'currency', 'code'])

CURRENCIES = {
    '-': Currency('-', '-', '-'),
    'USD': Currency('United States', 'US Dollar', 'USD'),
    'EUR': Currency('Europe', 'Euro', 'EUR'),
    'PLN': Currency('Poland', 'Polish Zloty', 'PLN'),
    'GBP': Currency('United Kingdom', 'British Pound', 'GBP'),
}


def get_currency_choices():
    return [(c.code, "{0} - {1}".format(c.code, c.currency))
            if c.code != '-' else ('-', '-')
            for c in CURRENCIES.values()]
