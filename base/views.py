from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm


# Create your views here.

rooms= [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Lets learn Math!'},
    {'id': 3, 'name': 'Lets learn Science!'}
]
def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    return render(request, 'room.html')

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'room_form.html', {'form': form})

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'room_form.html', {'form':form})
  
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj':room})
  
