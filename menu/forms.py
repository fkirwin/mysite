import datetime

from django import forms
from django.contrib.auth.models import User

from .models import Menu, Item, Ingredient

years = list((year for year in range(datetime.date.today().year-10, datetime.date.today().year+10)))

class MenuForm(forms.ModelForm):
    season = forms.CharField(max_length=20, required=True)
    items = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': '10'}), queryset=Item.objects.all())
    expiration_date = forms.DateField(input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
                                      initial=datetime.date.today().year+10,
                                      widget=forms.SelectDateWidget(years=years),
                                      required=False)

    class Meta:
        model = Menu
        exclude = ('created_date',)


class ItemForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    description = forms.Textarea()
    chef = forms.ModelChoiceField(queryset=User.objects.all())
    standard = forms.BooleanField(required=False)
    ingredients = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': '10'}), queryset=Ingredient.objects.all())

    class Meta:
        model = Item
        exclude = ('created_date',)