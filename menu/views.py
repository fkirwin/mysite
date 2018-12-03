from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from django.forms.models import model_to_dict
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import *
from .forms import *

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
    return render(request, 'menu/detail_item.html', {'item': item})

def create_new_menu(request):
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

def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    items = Item.objects.all()
    if request.method == "POST":
        menu.season = request.POST.get('season', '')
        menu.expiration_date = datetime.strptime(request.POST.get('expiration_date', ''), '%m/%d/%Y')
        menu.items = request.POST.get('items', '')
        menu.save()

    return render(request, 'menu/change_menu.html', {
        'menu': menu,
        'items': items,
        })