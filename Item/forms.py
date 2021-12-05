from django import forms
from django.forms import fields
from .models import Item

class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        # fields = '__all__'
        exclude = ['user','status', 'is_ads']