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
        #widgets = {
        #    'seller': forms.Select(attrs={'class': 'form-control'}),
        #}

    #def clean(self):
    #    price = self.cleaned_data.get('price')
    #    if price < 0:
    #        raise forms.ValidationError("Price must be greater than 0")
    #    return price