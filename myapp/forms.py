from django import forms
from .models import Country, State, City, Address
from datetime import date

class AddressForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select country", required=True)
    state = forms.ModelChoiceField(queryset=State.objects.none(), empty_label="Select state", required=True)
    city = forms.ModelChoiceField(queryset=City.objects.none(), empty_label="Select city", required=True)
    first_name = forms.CharField(max_length=10,required=True) 


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
      

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
    
    def save(self, commit=True):
        # Get the instance of the model, without saving it to the database
        instance = super(AddressForm, self).save(commit=False)

        # Set the state and city based on the selected values
        country = self.cleaned_data.get('country')
        state = self.cleaned_data.get('state')
        city = self.cleaned_data.get('city')

        if country:
            instance.country = country

        if state:
            instance.state = state

        if city:
            instance.city = city

        # Save the instance to the database
        if commit:
            instance.save()

        return instance
    class Meta:
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
