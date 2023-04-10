from django import forms
from .models import products, agricultureBasics,grassCutters
import random


class ProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = '__all__'


class AgroBasicForm(forms.ModelForm):
    class Meta:
        model = agricultureBasics
        fields = '__all__'




