from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm


# Create your views here.

# rooms= [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Lets learn Math!'},
#     {'id': 3, 'name': 'Lets learn Science!'}
# ]
def loginPage(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username).lower()
        except:
            messages.error(request, "Invalid Username")

        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username Or Password does not exist')

    return render(request, 'login_register.html', {"page":page} )

def logOutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):

    form = UserCreationForm(request.POST)
    if form.is_valid():
        user=form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, "An error occured during registration.")

    return render(request, 'login_register.html',{"form":form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)|
        Q(host__username__icontains=q)

    
    ) 
   
    topics = Topic.objects.all()
    return render(request, 'home.html', {'rooms': rooms, 'topics': topics})


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
  
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            topic= room.topic,
            body=request.POST.get('body')    
        )
        room.participants.add(request.User)
        return redirect('room', pk=room.id)
    
    return render(request, 'room.html', {'room': room,
                                          'room_messages': room_messages,
                                          'participants': participants})

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'room_form.html', {'form': form})

@login_required(login_url='login')
def updateRoom(request, pk):

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if room.host != request.user:
        return HttpResponse('You donot have permission to update room')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'room_form.html', {'form':form})
  
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if room.host != request.user:
        return HttpResponse('You donot have permission to update room')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj':room})
  
