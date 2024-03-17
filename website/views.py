from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')

    if request.user.is_authenticated:
        # Check if user is superuser
        if request.user.is_superuser:
            records = Record.objects.all()
        else:
            records = Record.objects.filter(created_by=request.user)
    else:
        records = None

    return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        try:
            customer_record = Record.objects.get(id=pk, created_by=request.user)
            return render(request, 'record.html', {'customer_record': customer_record})
        except Record.DoesNotExist:
            messages.error(request, "Record not found or you don't have permission to view it.")
    else:
        messages.error(request, "You Must Be Logged In To View That Page...")
    return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        try:
            delete_it = Record.objects.get(id=pk, created_by=request.user)
            delete_it.delete()
            messages.success(request, "Record Deleted Successfully...")
        except Record.DoesNotExist:
            messages.error(request, "Record not found or you don't have permission to delete it.")
    else:
        messages.error(request, "You Must Be Logged In To Do That...")
    return redirect('home')


def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                record = form.save(commit=False)
                record.created_by = request.user
                record.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "You Must Be Logged In...")
    return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        try:
            current_record = Record.objects.get(id=pk, created_by=request.user)
            form = AddRecordForm(request.POST or None, instance=current_record)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect('home')
        except Record.DoesNotExist:
            messages.error(request, "Record not found or you don't have permission to update it.")
    else:
        messages.error(request, "You Must Be Logged In...")
    return redirect('home')
