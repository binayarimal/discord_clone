from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

rooms= [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Lets learn Math!'},
    {'id': 3, 'name': 'Lets learn Science!'}
]
def home(request):
    return render(request, 'home.html', {'rooms': rooms})

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    return render(request, 'room.html')