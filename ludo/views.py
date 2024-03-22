from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import Http404

def lobby(request, room_code):
    context = {"room_code": room_code,}
    return render(request, "lobby.html", context)

def index(request):
    if request.method == "POST":
        room_code = request.POST.get("room_code")
        return redirect('/ludo/lobby/%s'%(room_code))
    return render(request, "index.html", {})

def game(request):
    # if request.method == "POST":
    #     room_code = request.POST.get("room_code")
    #     context = {"room_code": room_code,}
    return render(request , 'game.html')

