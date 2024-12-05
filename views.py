from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SpentDataForm, CreditDataForm,RegisterForm
from .models import SpentData, CreditData, Category
from django.db.models import Sum
from django.contrib import messages
import json

def register_login(request):
    form = RegisterForm()  # Initialize the form for both GET and POST requests

    if request.method == 'POST':
        if 'register' in request.POST:  # Check if the registration button was clicked
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('index')  # Redirect to the home page
            else:
                messages.error(request, "Please correct the errors from register page.")
        
        elif 'login' in request.POST:  # Check if the login button was clicked
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'register_login.html', {'form': form})

@login_required
def index(request):
    # Calculate total balance
# Correct querying from the models, not forms
    total_spent = SpentData.objects.filter(user=request.user).aggregate(total=Sum('price'))['total'] or 0
    total_credit = CreditData.objects.filter(user=request.user).aggregate(total=Sum('money'))['total'] or 0
    balance = total_credit - total_spent

    return render(request, 'index.html', {'balance': balance})

# View for the dashboard (showing spent and credit data)
@login_required
def dashboard(request):
    spent_data = SpentData.objects.filter(user=request.user).order_by('-id')
    credit_data = CreditData.objects.filter(user=request.user).order_by('-id')
    total_spent = SpentData.objects.filter(user=request.user).aggregate(total=Sum('price'))['total'] or 0
    total_credit = CreditData.objects.filter(user=request.user).aggregate(total=Sum('money'))['total'] or 0
    balance = total_credit - total_spent
    categories = list(spent_data.values_list('category__name', flat=True))
    amounts = [float(spent.price) for spent in spent_data]  # Convert Decimal to float

    return render(request, 'dashboard.html', {
        'total_spent': total_spent,
        'total_credit': total_credit,
        'spent_data': spent_data,
        'credit_data': credit_data,
        'balance':balance,
        'categories_json': json.dumps(categories),  # Properly serialize to JSON
        'amounts_json': json.dumps(amounts),        # Properly serialize to JSON
    })


# View for adding spent data (expenses)
@login_required
def add_spent_data(request):
    total_credits = CreditData.objects.filter(user=request.user).aggregate(Sum('money'))['money__sum'] or 0
    total_spent = SpentData.objects.filter(user=request.user).aggregate(Sum('price'))['price__sum'] or 0
    user_balance = total_credits - total_spent

    if request.method == 'POST':
        form = SpentDataForm(request.POST)
        if form.is_valid():
            spent_data = form.save(commit=False)
            spent_data.user = request.user  # Attach the logged-in user
            # Check if the entered price is greater than the user's total balance
            if spent_data.price > user_balance:
                # Add an error message for insufficient balance
                messages.error(request, 'Insufficient balance in account. Please enter a lower amount.')
            else:
                # If balance is sufficient, save the spent data
                spent_data.save()
                return redirect('dashboard')
    else:
        form = SpentDataForm()
    return render(request, 'spent_form.html', {'form': form , 'balance':user_balance})

# View for adding credit data (income)
@login_required
def add_credit_data(request):
    if request.method == 'POST':
        form = CreditDataForm(request.POST)
        if form.is_valid():
            credit_data = form.save(commit=False)
            credit_data.user = request.user  # Attach the logged-in user
            credit_data.save()
            return redirect('dashboard')
    else:
        form = CreditDataForm()
    return render(request, 'credit_form.html', {'form': form})