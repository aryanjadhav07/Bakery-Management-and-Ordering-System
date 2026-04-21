from django import forms
from django.core.exceptions import ValidationError
from .models import Product


def validate_image_file(file):
    """
    Accept jpg, jpeg, png, gif, webp.
    Django's ImageField already runs Pillow validation; this adds
    an explicit extension check so the error message is clear.
    """
    if not file:
        return
    name = getattr(file, 'name', '')
    ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
    allowed = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    if ext not in allowed:
        raise ValidationError(
            f'Unsupported file type ".{ext}". '
            f'Please upload a JPG, PNG, GIF, or WEBP image.'
        )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description',
            'price', 'price_half_kg', 'price_1kg', 'price_2kg',
            'image',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter cake name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the cake...',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
            }),
            'price_half_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
            }),
            'price_1kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
            }),
            'price_2kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/gif,image/webp',
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'name'):
            validate_image_file(image)
        return image
