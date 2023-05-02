from django.shortcuts import render
from django.http import JsonResponse
from .forms import AddressForm
from .models import Country, State, City, Address


def address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = Address()
            country_name = form.cleaned_data['country']
            state_name = form.cleaned_data['state']
            city_name = form.cleaned_data['city']
            street_address = form.cleaned_data['first_name']
            address.country=Country.objects.get(name=country_name)
            address.state=State.objects.get(name=state_name)
            address.city=City.objects.get(name=city_name)
            address.street_address = street_address
            print(city_name)    
            address.save()       

    else:
        form = AddressForm()

    return render(request, 'address.html', {'form': form})


def load_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'state_dropdown_list_options.html', {'states': states})


def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})
