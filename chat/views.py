from django.shortcuts import render

def index_view(request):
    context = {}
    return render(request, "index.html", context)

def room_view(request, room_name):
    return render(request, "room.html", {"room_name": room_name})