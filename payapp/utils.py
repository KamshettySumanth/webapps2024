from register.lists import CURRENCIES, CONVERSION_RATES

def exchange_rate(base_currency, target_currency):
    if base_currency == target_currency:
        return 1
    try:
        if base_currency not in CONVERSION_RATES or target_currency not in CONVERSION_RATES[base_currency]:
            return None
        print(CONVERSION_RATES[base_currency][target_currency])
        return CONVERSION_RATES[base_currency][target_currency]
    except:
        return None