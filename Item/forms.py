from django import forms
from django.forms import fields
from .models import Item, User

class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        # fields = '__all__'
        exclude = ['user','status', 'is_ads']
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'