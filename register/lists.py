NOTIFICATION = (
    ("payment_received", ("Payment Received")),
    ("payment_request_received", ("Payment Request Received")),
    ("payment_request_result", ("Payment Request Result")),
)

CURRENCIES = (
    ('EUR', 'Euro'),
    ('USD', 'US Dollar'),
    ('GBP', 'Great Britain Pound')
)

CONVERSION_RATES = {
    'USD': {
        'USD': 1.0,
        'GBP': 0.80,  # 1 USD = 0.80 GBP
        'EUR': 0.93,  # 1 USD = 0.93 EUR
    },
    'GBP': {
        'USD': 1.25,  # 1 GBP = 1.25 USD
        'GBP': 1.0,
        'EUR': 1.17,  # 1 GBP = 1.17 EUR
    },
    'EUR': {
        'USD': 1.07,  # 1 EUR = 1.07 USD
        'GBP': 0.86,  # 1 EUR = 0.86 GBP
        'EUR': 1.0,
    },
}