from django.db import IntegrityError
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from .models import Room, Message
from .forms import RoomForm

@login_required
def rooms(request):
    # Exclude 'personal_' rooms from the list displayed to users
    rooms = Room.objects.exclude(name__startswith='personal_').all()
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'room/rooms.html', {'rooms': rooms, 'users': users})

@login_required
def room(request, slug=None):
    if slug is None:
        return HttpResponseBadRequest("Room slug is required")

    try:
        # Include 'personal_' rooms for direct access
        room = Room.objects.get(slug=slug)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")

    rooms = Room.objects.exclude(name__startswith='personal_').all()  # Retrieve all rooms excluding 'personal_' rooms
    messages = Message.objects.filter(room=room)[:25]
    users = User.objects.exclude(username=request.user.username)
    context = {'room': room, 'messages': messages, 'users': users, 'rooms': rooms}
    return render(request, 'room/room.html', context)



def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.slug = slugify(room.name)  # Generate slug from room name
            room.save()
            return redirect('rooms')
    else:
        form = RoomForm()
    return render(request, 'room/create_room.html', {'form': form})

@login_required
def create_personal_room(request, username):
    # Generate room names
    room_name_1 = f'personal_{request.user.username}_{username}'
    room_name_2 = f'personal_{username}_{request.user.username}'
    
    # Generate slugs
    slug_1 = slugify(room_name_1)
    slug_2 = slugify(room_name_2)

    # Check if a room with either name exists
    try:
        room = Room.objects.get(slug__in=[slug_1, slug_2])
    except Room.DoesNotExist:
        # Create a new room if no existing room is found
        room = Room.objects.create(name=room_name_1, slug=slug_1)

    return redirect('room', slug=room.slug)
