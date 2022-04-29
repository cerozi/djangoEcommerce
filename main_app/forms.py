from django import forms

PAGAMENTO_OPCOES = (
    ('CC', 'Cartão de Crédito'),
    ('P', 'Paypal'),
)


class CheckoutForm(forms.Form):
    rua = forms.CharField()
    bairro = forms.CharField()
    num = forms.IntegerField()
    complemento = forms.CharField()
