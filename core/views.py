from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import pytz

# Create your views here.
def welcome(request):
    return render(request, "core/welcome.html")

#2 Users list 
def users_list(request):
    users = [
        {"full_name": "Alice Jonshon", "age": 25},
        {"full_name": "Bob Smith", "age": 30},
        {"full_name": "Charlie Brown", "age": 22},
    ]
    return render(request, "core/users_list.html", {"users": users})

#3 City time
def city_time(request):
    cities = {
        "Almaty": "Asia/Almaty",
        "New York": "America/New_York",
        "Moscow": "Europe/Moscow",
        "UTC": "UTC",
    }
    city = request.GET.get("city", "UTC")
    tz = pytz.timezone(cities[city])
    now = datetime.now(tz)
    return render(request, "core/city_time.html",{"city": city, "time": now, "cities": cities})

#4 Counter 
def counter(request):
    if "count" not in request.session:
        request.session["count"] = 0
    if request.method == "POST":
        if "inc" in request.POST:
            request.session["count"] += 1
        elif "reset" in request.POST:
            request.session["count"] = 0
    return render(request, "core/counter.html", {"count": request.session["count"]})
