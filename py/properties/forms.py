from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Property, PropertyImage, User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'profile_picture', 'bio']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'profile_picture', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'address', 'city', 'state',
            'zip_code', 'bedrooms', 'bathrooms', 'square_feet',
            'property_type', 'status', 'featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'min': 0}),
            'bedrooms': forms.NumberInput(attrs={'min': 0}),
            'bathrooms': forms.NumberInput(attrs={'min': 0, 'step': 0.5}),
            'square_feet': forms.NumberInput(attrs={'min': 0}),
        }

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_primary'] 