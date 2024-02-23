from django.contrib.auth.models import User
from django.db import models

class Room(models.Model):
    TYPES=(('direct', 'direct'),
           ('group', 'group'))
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(User, related_name='users')
    type = models.CharField(choices=TYPES, default='direct', max_length=255)
    


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)