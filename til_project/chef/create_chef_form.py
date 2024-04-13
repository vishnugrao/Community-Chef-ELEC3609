from django import forms
from .models import Chef, Recipe

class ChefRegistrationForm(forms.ModelForm):
    class Meta:
        model = Chef
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

class RecipeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-field'
        self.fields['description'].widget.attrs['class'] = 'form-field'
        self.fields['image'].widget.attrs['class'] = 'image-field'
    