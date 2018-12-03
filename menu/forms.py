from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

from .models import Menu, Item, Ingredient

years = list((year for year in range(datetime.date.today().year-10, datetime.date.today().year+10)))

class MenuForm(forms.ModelForm):
    season = forms.CharField(max_length=20, required=True)
    items = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': '10'}), queryset=Item.objects.all())
    expiration_date = forms.DateField(input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
                                      initial=datetime.date.today(),
                                      widget=forms.SelectDateWidget(years=years))

    class Meta:
        model = Menu
        exclude = ('created_date',)