from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Laptop

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('user_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].label = "Registrati come"


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = '__all__'
        exclude = ['seller']

    def clean_ram(self):
        ram = self.cleaned_data['ram']
        if ram < 0:
            raise forms.ValidationError("Ram must be greater than 0")
        return ram

    def clean_storage(self):
        storage = self.cleaned_data['storage']
        if storage < 0:
            raise forms.ValidationError("Storage must be greater than 0")
        return storage

    def clean_display_inches(self):
        display_inches = self.cleaned_data['display_inches']
        if display_inches < 0:
            raise forms.ValidationError("Display inches must be greater than 0")
        return display_inches

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Price must be greater than 0")
        return price

class SearchForm(forms.Form):
    search_string = forms.CharField(label='Cerca')
