from django import forms
from .models import Good


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = [
            "product_code",
            "name",
            "category",
            "supplier",
            "manufacturer",
            "unit",
            "price",
            "discount",
            "amount",
            "description",
            "photo",
        ]
