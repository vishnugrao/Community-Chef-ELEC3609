from django import forms

class CustomerLoginForms(forms.Form):
    username = forms.CharField(max_length=225, widget=forms.TextInput(attrs={'class': 'form-field'}))
    password = forms.CharField(max_length=225, widget=forms.PasswordInput(attrs={'class': 'password-input'}))
