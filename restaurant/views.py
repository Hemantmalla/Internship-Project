from django.shortcuts import render, redirect, get_object_or_404
from .forms import waiterForm, loginForm, ReservationForm, MenuItemForm
from django.http import JsonResponse
from .models import Reservation, CustomUser, MenuItem, SubCategory
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

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
def term(request):
    return render(request,'restaurant/term.html')
def role_selection(request):
    return render(request, 'restaurant/role.html')
def login_page(request):
    form = loginForm()
    return render(request, 'restaurant/login.html', {'form': form})

# custom user view start
# user login view start
# role selection view
def role_selection(request):
    if request.method == "POST":
        role = request.POST.get("role")
        
        request.session['selected_role'] = role

        if role == "waiter":
            return redirect("login")
        elif role == "user":
            return redirect("index")  

    return render(request, "restaurant/role.html")

# user login view end
# custom user view end
# waiter registration view start
def waiter_form(request):
    if request.method == "POST":
        form = waiterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'waiter'
            user.save()
            return redirect('login')
    else:
        form = waiterForm()  

    return render(request, 'restaurant/registerform.html', {'form': form})

def register_storage(request):
    if request.user.role != 'waiter':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    waiters = CustomUser.objects.filter(role='waiter')
    return render(request, 'restaurant/register_storage.html', {'waiters': waiters})

def login_page(request):
    error = ""
    if request.method == "POST":
            email = request.POST.get('waiter_email')
            password = request.POST.get('waiter_password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error = "Invalid email or password."
                
    form = loginForm()
    return render(request, 'restaurant/login.html', {'error': error})
# waiter registration view end
    
# reservation page view start
def reserve(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            num_people = form.cleaned_data['num_people']

            if num_people > 12:
                form.add_error('num_people', 'Maximum 12 people allowed')
                return render(request, 'reserve.html', {'form': form})
            else:
                form.save()
                messages.success(request, 'Reservation added successfully!')
                return redirect('reserve')
    else:
        form = ReservationForm()
    reservations = Reservation.objects.all()
    return render(request, 'restaurant/reserve.html', {
        'form': form,
        'reservations': reservations,
        'is_waiter': 'waiter_id' in request.session
        })

def update_res(request, res_id):
    reservation = get_object_or_404(Reservation, res_id=res_id)

    if 'waiter_id' not in request.session:
        return redirect('login')

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reserve')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'restaurant/update_res.html', {'form': form})

def delete_res(request, res_id):
    if 'waiter_id' not in request.session:
        return redirect('login')

    reservation = get_object_or_404(Reservation, res_id=res_id)
    reservation.delete()
    return redirect('reserve')

# reservation page view end


# login required start
@login_required
def order(request):
    if request.user.role != 'waiter':
        return HttpResponseForbidden("Access denied.")
    
    return render(request,'restaurant/order.html')

@login_required
def profile(request):
    if request.user.role != 'waiter':
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request,'restaurant/profile.html')
# login required end

# logout view start
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('role')

# ---------- MENU PAGE VIEWS ----------

def menu_view(request):
    subcategories = SubCategory.objects.all()
    items_by_slug = {}
    for sc in subcategories:
        items_by_slug[sc.slug] = MenuItem.objects.filter(subcategory=sc)

    return render(request, "urban_umami/nav/menu.html", {
        "subcategories": subcategories,
        "items_by_slug": items_by_slug
    })

def add_menu_item(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("menu")  
    else:
        form = MenuItemForm()
    return render(request, "urban_umami/add_item.html", {"form": form})


# ---------- CART PAGE VIEWS ----------
def add_to_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(MenuItem, id=item_id)

        cart = request.session.get("cart", {})

        if str(item_id) in cart:
            cart[str(item_id)]["quantity"] += 1
        else:
            cart[str(item_id)] = {
                "name": item.name,
                "price": float(item.price),
                "image": item.image.url if item.image else "",
                "quantity": 1,
            }

        request.session["cart"] = cart

        return JsonResponse({
            "success": True,
            "cart_count": sum(i["quantity"] for i in cart.values())
        })
    
def cart_view(request):
    cart = request.session.get("cart", {})
    total = sum(item["price"] * item["quantity"] for item in cart.values())

    return render(request, "restaurant/card.html", {
        "cart": cart,
        "total": total
    })
def update_qty(request, item_id, action):
    cart = request.session.get("cart", {})

    if str(item_id) in cart:
        if action == "inc":
            cart[str(item_id)]["quantity"] += 1
        elif action == "dec":
            if cart[str(item_id)]["quantity"] > 1:
                cart[str(item_id)]["quantity"] -= 1
            else:
                del cart[str(item_id)]

    request.session["cart"] = cart
    return JsonResponse({"success": True})


# ---------- ORDER PAGE VIEWS ----------

def order_view(request):
    cart = request.session.get("cart", {})
    order_items = []

    for item in cart.values():
        for _ in range(item["quantity"]):
            order_items.append({
                "image":item['image'],
                "name": item["name"],
                "price": item["price"]
            })

    request.session["cart"] = {}

    return render(request, "restaurant/order.html", {
        "order_items": order_items
    })



# ---------- BILL GENARATATION start ----------
def generate_bill(request):
    if request.method == "POST":

        bill_data = {
            "customer": request.POST.get("customer"),
            "phone": request.POST.get("phone"),
            "table": request.POST.get("table"),
            "date": request.POST.get("date"),
            "time": request.POST.get("time"),
            "items": request.POST.get("items"),
            "total": request.POST.get("total"),
        }
        generated_bills = request.session.get("generated_bills", [])
        generated_bills.append(bill_data)
        request.session["generated_bills"] = generated_bills
        order_list = request.session.get("order_list", [])
        order_list.append(bill_data)
        request.session["order_list"] = order_list
        return redirect("generated_bill")




# ---------- BILL STORING DETAILS ----------
def generated_bill_view(request):
    bills = request.session.get("generated_bills", [])
    return render(request, "restaurant/generatedbill.html", {
        "bills": bills
    })


# ---------- ORDER STORING DETAILS ----------
def order_list_view(request):
    order_list = request.session.get("order_list", [])
    return render(request, "restaurant/orderdetail.html", {
        "order_list": order_list
    })
    
# ---------- BILL GENARATATION end ----------
