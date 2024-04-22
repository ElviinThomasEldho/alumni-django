from django.db import IntegrityError
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from .models import Room, Message
from main.models import Account

from .forms import RoomForm

@login_required
def rooms(request):
    # Include 'personal_' rooms in the list displayed to users
    rooms = Room.objects.all()
    public_rooms = Room.objects.exclude(name__startswith='personal_').all()
    users = User.objects.exclude(username=request.user.username)
    accounts = Account.objects.exclude(user=request.user).all()
    account = Account.objects.get(user=request.user)
    
    # Create a list to store 'personal_' rooms
    personal_rooms = []

    for room in rooms:
        # Check if the room name starts with 'personal_' and includes the current user's username
        if room.name.startswith('personal_') and request.user.username in room.name:
            # Extract the other user's username from the room name
            other_username = room.name.replace('personal_', '').replace(request.user.username, '').strip('_')
            # Get the other user's account
            other_user_account = Account.objects.get(user__username=other_username)
            # Create a dictionary to represent the 'personal_' room
            personal_room = {
                'name': f'{other_user_account.firstName} {other_user_account.lastName}',
                'username': other_username,
                'profile_image': other_user_account.profilePicture.url,
                'slug': room.slug
            }
            # Add the 'personal_' room to the list
            personal_rooms.append(personal_room)

    return render(request, 'room/rooms.html', {'username': other_username, 'public_rooms': public_rooms, 'rooms': rooms, 'users': users,'accounts': accounts, 'account': account, 'personal_rooms': personal_rooms})

@login_required
def room(request, slug=None):
    if slug is None:
        return HttpResponseBadRequest("Room slug is required")

    try:
        # Include 'personal_' rooms for direct access
        room = Room.objects.get(slug=slug)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")

    rooms = Room.objects.all()  # Retrieve all rooms excluding 'personal_' rooms
    messages = Message.objects.filter(room=room)[:25]
    users = User.objects.exclude(username=request.user.username)
    accounts = Account.objects.exclude(user=request.user).all()
    account = Account.objects.get(user=request.user)

    if room.type == 'direct':
        members = list(room.users.all())

        for member in members:
            if (member != request.user):
                target = member
                print(target)
        target = Account.objects.get(user=target)

        context = {'room': room, 'messages': messages, 'users': users, 'rooms': rooms, 'accounts': accounts, 'account': account, 'target': target}
        return render(request, 'room/room.html', context)
    else:
        context = {'room': room, 'messages': messages, 'users': users, 'rooms': rooms, 'accounts': accounts, 'account': account, 'target': room.name}
        return render(request, 'room/room.html', context)



def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.slug = room.name.replace(' ', '').lower()  # Generate slug from room name
            room.type = 'group'
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
    target = User.objects.get(username=username)
    # Check if a room with either name exists
    try:
        room = Room.objects.get(slug__in=[slug_1, slug_2])
    except Room.DoesNotExist:
        # Create a new room if no existing room is found
        room = Room.objects.create(name=room_name_1, slug=slug_1)
        room.users.add(request.user)
        room.users.add(target)
        room.type = 'direct'
        room.save()

    return redirect('room', slug=room.slug)

def newchat(request):
    accounts = Account.objects.exclude(user=request.user).all()
    account = Account.objects.get(user=request.user)
    context = {'accounts': accounts, 'account': account}
    return render(request, 'room/newchat.html', context)