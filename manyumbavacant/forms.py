from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Property, Landlord

class LandlordForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = ['name', 'phone', 'alt_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'alt_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LandlordRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    alt_phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'phone', 'alt_phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Landlord.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                phone=self.cleaned_data['phone'],
                alt_phone=self.cleaned_data['alt_phone'],
                is_verified=True
            )
        return user

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['landlord', 'is_approved', 'approved_by', 'approved_at', 'flag_count', 
                   'is_active', 'created_at', 'updated_at', 'view_count', 'listing_tier', 
                   'tier_expiry', 'payment_reference', 'payment_confirmed', 'promotion_start', 'total_paid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional initially; we'll enforce in clean()
        for field in self.fields:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        property_type = cleaned_data.get('property_type')

        if property_type in ['rent', 'lease']:
            # Required for rent/lease
            if not cleaned_data.get('monthly_rent'):
                self.add_error('monthly_rent', 'Monthly rent is required for rent/lease properties.')
            if not cleaned_data.get('house_type'):
                self.add_error('house_type', 'House type is required for rent/lease properties.')
            # Optional fields get defaults
            if not cleaned_data.get('total_units'):
                cleaned_data['total_units'] = 1
            if not cleaned_data.get('min_lease_months'):
                cleaned_data['min_lease_months'] = 6

        elif property_type == 'airbnb':
            if not cleaned_data.get('nightly_rate'):
                self.add_error('nightly_rate', 'Nightly rate is required for Airbnb properties.')
            # Defaults
            if not cleaned_data.get('bedrooms'):
                cleaned_data['bedrooms'] = 1
            if not cleaned_data.get('beds'):
                cleaned_data['beds'] = 1
            if not cleaned_data.get('baths'):
                cleaned_data['baths'] = 1

        elif property_type == 'conference':
            if not cleaned_data.get('hourly_rate'):
                self.add_error('hourly_rate', 'Hourly rate is required for conference facilities.')
            if not cleaned_data.get('capacity_range'):
                self.add_error('capacity_range', 'Capacity range is required for conference facilities.')
            # Defaults for non-conference fields (ignore them)
            # Set dummy values for fields that are not applicable but the model expects
            cleaned_data['monthly_rent'] = None
            cleaned_data['nightly_rate'] = None
            cleaned_data['house_type'] = ''
            cleaned_data['total_units'] = 1
            cleaned_data['min_lease_months'] = 6

        # For any type, ensure total_units and min_lease_months have defaults
        if not cleaned_data.get('total_units'):
            cleaned_data['total_units'] = 1
        if not cleaned_data.get('min_lease_months'):
            cleaned_data['min_lease_months'] = 6

        return cleaned_data