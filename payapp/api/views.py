from decimal import Decimal
from django.http import JsonResponse
from django.views import View

from payapp.utils import exchange_rate


class ExchangeRateView(View):
    def calculate_exchange_rate(self, base_currency, target_currency):
        return exchange_rate(base_currency, target_currency)

    def get(self, request, currency1, currency2, amount_of_currency1):
        try:
            rate1_to_2 = self.calculate_exchange_rate(currency1, currency2)
        except KeyError:
            return JsonResponse(
                {'error': 'Invalid currency codes provided.'},
                status=400
            )

        if rate1_to_2 is None:
            return JsonResponse(
                {   
                    'status': 'error',
                    'message': 'Something went wrong. Make sure both currencies are valid.'},
                status=400
            )

        amount_of_currency2 = Decimal(amount_of_currency1) * Decimal(rate1_to_2)
        response_data = {
            'status': 'success',
            'data': {
                'base_currency': currency1,
                'target_currency': currency2,
                'amount': amount_of_currency2,
            }
        }

        return JsonResponse(response_data)