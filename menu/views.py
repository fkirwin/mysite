from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import *
from .forms import *


#TODO: Test coverage is at or above 75%.


def menu_list(request):
    """
    Returns all of the menu items without an expiration date or with an expiration date that is greater than the
    current date.
    :param request: boilerplate Django request param.
    :return: view of all menu items that meet the criteria.
    """
    menus = Menu.objects.prefetch_related('items') \
        .filter(Q(expiration_date__gte=datetime.datetime.now(timezone.get_current_timezone())) | Q(expiration_date__isnull=True)) \
        .order_by('expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})

def menu_detail(request, pk):
    """
    Gets the details for a chosen menu.
    :param request: boilerplate Django request param.
    :param pk: The menu id.
    :return: a view with the menu details.
    """
    try:
        menu = Menu.objects.prefetch_related('items').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """
    Gets the details for a chosen item.
    :param request: boilerplate Django request param.
    :param pk: The menu id.
    :return: a view with the item details.
    """
    try: 
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/item_detail.html', {'item': item})


@login_required
def create_new_menu(request):
    """
    Creates a new menu with options available from the DB.
    :param request:  Django request object
    :return: Redirect to menu detail.
    """
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            form.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


@login_required
def edit_menu(request, pk):
    """
    Allows for existing menus to be edited.
    :param request:  Django request object
    :return: Redirect to menu detail.
    """
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(initial=model_to_dict(menu))
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.pk = pk
            menu.save()
            form.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    return render(request, 'menu/menu_edit.html', {'form': form, 'pk': pk})


@login_required
def edit_item(request, pk):
    """
    Allows for existing items to be edited.
    :param request:  Django request object
    :return: Redirect to menu detail.
    """
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pk = pk
            item.save()
            form.save_m2m()
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(initial=model_to_dict(item))
    return render(request, 'menu/item_edit.html', {'form': form, 'pk': pk})


def sign_in(request):
    """Signs user in.  Uses default Django forms and models."""
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return redirect('menu_list')
                else:
                    messages.error(request, "That user account has been disabled.")
            else:
                messages.error(request, "Username or password is incorrect.")
    return render(request, 'menu/sign_in.html', {'form': form})


def sign_up(request):
    """Used for user registration.  Uses default forms and models from Django."""
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(request, "You're now a user! You've been signed in, too.")
            return redirect('menu_list')
    return render(request, 'menu/sign_up.html', {'form': form})


def sign_out(request):
    """Default sign out view."""
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return redirect('menu_list')
