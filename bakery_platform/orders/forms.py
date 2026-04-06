from django import forms

class OrderForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField()
