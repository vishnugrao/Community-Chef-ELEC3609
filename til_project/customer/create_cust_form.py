from django import forms
from .models import Customer

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'password-input'}),
        }

    # You can also add additional CSS classes to other fields by overriding __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs['class'] = 'form-field'
        self.fields['lastname'].widget.attrs['class'] = 'form-field'
        self.fields['username'].widget.attrs['class'] = 'form-field'
        self.fields['email'].widget.attrs['class'] = 'form-field'