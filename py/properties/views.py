from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login
from .models import Property, PropertyImage, User
from .forms import PropertyForm, PropertyImageForm, UserRegistrationForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Real Estate Sales.')
            return redirect('property_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'properties/profile.html', {'form': form})

def property_list(request):
    properties = Property.objects.filter(status='available').order_by('-created_at')
    paginator = Paginator(properties, 9)  # Show 9 properties per page
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    return render(request, 'properties/property_list.html', {'properties': properties})

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property})

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            messages.success(request, 'Property listing created successfully!')
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm()
    return render(request, 'properties/property_form.html', {'form': form, 'action': 'Create'})

@login_required
def property_update(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if property.owner != request.user:
        messages.error(request, 'You are not authorized to edit this property.')
        return redirect('property_detail', pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property listing updated successfully!')
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm(instance=property)
    return render(request, 'properties/property_form.html', {'form': form, 'action': 'Update'})

@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if property.owner != request.user:
        messages.error(request, 'You are not authorized to delete this property.')
        return redirect('property_detail', pk=pk)
    
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property listing deleted successfully!')
        return redirect('property_list')
    return render(request, 'properties/property_confirm_delete.html', {'property': property})

@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'properties/my_properties.html', {'properties': properties})
