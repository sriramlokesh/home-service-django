from django import forms
from .models import *
import re


class stateform(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'

class cityform(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'

class ServiceCatogoryForm(forms.ModelForm):
    class Meta:
        model=ServiceCatogarys
        fields = ('Name', 'img', 'Description')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'subcategory', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category-select'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'subcategory-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter product description'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial subcategory choices based on category
        if self.instance.pk and self.instance.category:
            self.fields['subcategory'].choices = self.get_subcategory_choices(self.instance.category)
        else:
            # Default to grocery subcategories
            self.fields['subcategory'].choices = self.get_subcategory_choices('grocery')

    def get_subcategory_choices(self, category):
        """Get subcategory choices based on category"""
        if category == 'grocery':
            return [
                ('dairy', 'Dairy & Eggs'),
                ('snacks', 'Snacks & Branded Foods'),
                ('beverages', 'Beverages'),
                ('bakery', 'Bakery & Biscuits'),
                ('breakfast', 'Breakfast & Instant Food'),
                ('staples', 'Staples'),
                ('sweets', 'Sweets & Chocolates'),
            ]
        elif category == 'electricals':
            return [
                ('bulbs', 'Bulbs & Tubelights'),
                ('switches', 'Switches & Sockets'),
                ('wires', 'Wires & Cables'),
                ('appliances', 'Small Appliances'),
                ('batteries', 'Batteries & Chargers'),
            ]
        elif category == 'plumbing':
            return [
                ('pipes', 'Pipes & Fittings'),
                ('taps', 'Taps & Faucets'),
                ('showers', 'Showers & Accessories'),
                ('tools', 'Tools & Adhesives'),
            ]
        return []

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
    
    class Meta:
        model = AdminRegistrationRequest
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Indian phone number (e.g., 9876543210)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        if AdminRegistrationRequest.objects.filter(username=username, status='pending').exists():
            raise forms.ValidationError("A registration request with this username is already pending.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        if AdminRegistrationRequest.objects.filter(email=email, status='pending').exists():
            raise forms.ValidationError("A registration request with this email is already pending.")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        
        # Remove any spaces, dashes, or other characters
        phone_number = re.sub(r'[\s\-\(\)]', '', phone_number)
        
        # Indian phone number validation regex
        # Accepts: 10 digits starting with 6, 7, 8, 9 (mobile numbers)
        # Also accepts: +91 followed by 10 digits
        indian_phone_regex = r'^(\+91)?[6-9]\d{9}$'
        
        if not re.match(indian_phone_regex, phone_number):
            raise forms.ValidationError(
                "Please enter a valid Indian phone number. "
                "Format: 10 digits starting with 6, 7, 8, or 9 (e.g., 9876543210) "
                "or +91 followed by 10 digits (e.g., +919876543210)"
            )
        
        # If it starts with +91, remove it for storage
        if phone_number.startswith('+91'):
            phone_number = phone_number[3:]
        
        return phone_number

class AdminEditForm(forms.ModelForm):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password (leave blank to keep current)'}),
        required=False
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        required=False
    )
    
    class Meta:
        model = AdminRegistrationRequest
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Indian phone number (e.g., 9876543210)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        
        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match.")
        
        return cleaned_data
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        
        # Remove any spaces, dashes, or other characters
        phone_number = re.sub(r'[\s\-\(\)]', '', phone_number)
        
        # Indian phone number validation regex
        indian_phone_regex = r'^(\+91)?[6-9]\d{9}$'
        
        if not re.match(indian_phone_regex, phone_number):
            raise forms.ValidationError(
                "Please enter a valid Indian phone number. "
                "Format: 10 digits starting with 6, 7, 8, or 9 (e.g., 9876543210) "
                "or +91 followed by 10 digits (e.g., +919876543210)"
            )
        
        # If it starts with +91, remove it for storage
        if phone_number.startswith('+91'):
            phone_number = phone_number[3:]
        
        return phone_number

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter place name', 'label': 'Place'}),
        }
        labels = {
            'name': 'Place',
        }