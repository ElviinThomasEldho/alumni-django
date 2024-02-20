from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils.text import slugify

from .models import Room, Message
from .forms import RoomForm

def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

def room(request, slug=None):
    rooms = Room.objects.all()
    if slug is None:
        return HttpResponseBadRequest("Room slug is required")

    try:
        room = Room.objects.get(slug=slug)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")

    messages = Message.objects.filter(room=room)[:25]
    context = {'rooms': rooms, 'room': room, 'messages': messages}
    return render(request, 'room/room.html', context)

def room_view(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'room.html', context)

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
