from django.shortcuts import get_object_or_404, redirect, render
import requests
from decouple import config
from pprint import pprint
from .models import City
from django.contrib import messages

# Create your views here.
def index(request):
    cities = City.objects.all()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric&lang=de'
    #pprint(content)
    #print(type(content))
    
    g_city = request.GET.get('name')
    if g_city:
        reponse = requests.get(url.format(g_city, config('API_KEY')))
        print(reponse.status_code)
        if reponse.status_code == 200:
            content = reponse.json()
            a_city = content['name']
            if City.objects.filter(name=a_city):
                messages.warning(request, 'City already exist')
            else:
                City.objects.create(name=a_city)
                messages.success(request, 'City succesfully added')
        else:
            messages.warning(request, 'City does note exisit')
        return redirect('home')   
    city_data = []
    for city in cities:
        reponse = requests.get(url.format(city, config('API_KEY')))
        content = reponse.json()
        #pprint(content)
        data = {
            'city': city,
            'temp': content['main']['temp'],
            'desc': content['weather'][0]['description'],
            'icon': content['weather'][0]['icon'],
        }
        city_data.append(data)
    print(city_data)
    context = {
        'city_data': city_data
    }
    
    return render(request, 'myApp/index.html', context )

        # url almanin f format yöntemi
        # url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config('API_KEY')}"
        # response = requests.get(url)
        
def delete(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    return redirect ('home')
        