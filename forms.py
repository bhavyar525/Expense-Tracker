from django import forms
from .models import SpentData, CreditData
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Form for SpentData
class SpentDataForm(forms.ModelForm):
    class Meta:
        model = SpentData
        fields = [ 'date','category', 'product_name', 'price']
        widgets = {
            'category': forms.Select(attrs={'id': 'id_category'}),  # Assuming category is a choice field
            'price': forms.NumberInput(attrs={'id': 'id_price'}),
        }

# Form for CreditData
class CreditDataForm(forms.ModelForm):
    class Meta:
        model = CreditData
        fields = ['date','money']