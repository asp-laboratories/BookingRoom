from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'BookingRoomApp/login.html')

def sign_up(request):
    return render(request, 'BookingRoomApp/sign_up.html')

def home(request):
    return render(request, 'BookingRoomApp/home.html')

def reservacion(request):
    return render(request, 'BookingRoomApp/reservacion.html')