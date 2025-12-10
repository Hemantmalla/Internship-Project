from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request,'restaurant/about.html')
def contact(request):
    return render(request,'restaurant/contact.html')
def feedback(request):
    return render(request,'restaurant/feedback.html')
def index(request):
    return render(request,'restaurant/index.html')
def menu(request):
    return render(request,'restaurant/menu.html')
def order(request):
    return render(request,'restaurant/order.html')
def privacy(request):
    return render(request,'restaurant/privacy.html')
def profile(request):
    return render(request,'restaurant/profile.html')
def reserve(request):
    return render(request,'restaurant/reserve.html')
def term(request):
    return render(request,'restaurant/term.html')
    