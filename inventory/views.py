from django.shortcuts import render, request

# Create your views here.
def HomeView(request):
    cntxt = {"Title": "Home"}
    return render(request, 'inventory/home.html', cntxt)