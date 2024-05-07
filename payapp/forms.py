from django import forms
from .models import Payment, PaymentRequest


class PaymentSendForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PaymentSendForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["sender"].initial = user
            self.fields["sender"].widget = forms.HiddenInput()

        self.fields["recipient"].label = "Email"
        self.fields["recipient"].widget = forms.EmailInput(
            attrs={'class': 'form-control', "required": True})
        self.fields["amount"].widget.attrs.update(
            {"class": "form-control", "required": True})

    class Meta:
        model = Payment
        fields = ["sender", "recipient", "amount"]


class PaymentRequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PaymentRequestForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["requested_to"].initial = user
            self.fields["requested_to"].widget = forms.HiddenInput()
        self.fields["requested_from"].widget = forms.EmailInput(
            attrs={'class': 'form-control', "required": True})
        self.fields["requested_from"].label = "From"
        self.fields["amount"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = PaymentRequest
        fields = ["requested_to", "requested_from", "amount"]
