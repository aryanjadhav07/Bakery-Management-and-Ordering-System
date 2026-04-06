from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'price_half_kg', 'price_1kg', 'price_2kg', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cake name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the cake...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'price_half_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'price_1kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'price_2kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
