import json

from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe


def main(request):
    return render(request, 'main.html')

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
