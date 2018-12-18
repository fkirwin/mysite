import os

import sqlite3
from sqlite3 import Error

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import *
from .forms import *


#View
class ViewTests(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user('zoidberg')

    def test_menu_list(self):
        pass

    def test_menu_detail(self):
        pass

    def item_detail(self):
        pass


    def create_new_menu(self):
        pass

    def edit_menu(self):
        pass


    def edit_item(self):
        pass


#Form
class FormTests(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user('zoidberg')
        self.user = user
        ingredient1 = Ingredient(name='Beer')
        ingredient1.save()
        ingredient2 = Ingredient(name='Juice')
        ingredient2.save()
        item1 = Item(name='Purple Drink',
                     description='blah',
                     chef=user,
                     standard=True)
        item1.save()
        item1.ingredients=[ingredient1, ingredient2]
        item1.save()
        item2 = Item(name='Beers',
                     description='crunk',
                     chef=user,
                     standard=True)
        item2.save()
        item2.ingredients=[ingredient1]
        item2.save()
        menus = Menu(season="Startime",
                     expiration_date=None)
        menus.save()
        menus.items=[item1, item2]
        menus.save()
        self.item = Item.objects.first()
        self.ingredient = Ingredient.objects.first()


    def test_menu_form(self):
        good_form = MenuForm({
            'season': "June",
            'items': [self.item],
            'expiration_date': None,
        })
        bad_form = MenuForm({
            'season': None,
            'items': [self.item],
            'expiration_date': datetime.date.day,
        })
        self.assertTrue(good_form.is_valid())
        self.assertFalse(bad_form.is_valid())
        self.assertEqual(good_form.data['season'], "June")
        self.assertEqual(good_form.data['items'][0], self.item)
        self.assertIsInstance(good_form.data['items'][0], Item)
        self.assertEqual(good_form.data['expiration_date'], None)
        client = Client()
        response = client.post('/menu/new/', {
            'season': "June",
            'items': [self.item],
            'expiration_date': None,
        })
        self.assertEqual(response.status_code, 302)


    def test_item_form(self):
        good_form = ItemForm({
            'name': "Booze",
            'description': 'Get you drunk',
            'chef':1,
            'standard':True,
            'ingredients':[self.ingredient]
        })
        bad_form = ItemForm({
            'name': None,
            'description': 'Get you drunk',
            'chef':self.user,
            'standard':True,
            'ingredients':[self.ingredient, 'turkey']
        })
        print(good_form.errors)
        print(good_form.__dict__)
        self.assertTrue(good_form.is_valid())
        self.assertFalse(bad_form.is_valid())
        self.assertEqual(good_form.data['name'], "Booze")
        self.assertEqual(good_form.data['ingredients'][0], self.ingredient)
        self.assertIsInstance(good_form.data['ingredients'][0], Ingredient)
        client = Client()
        response = client.post('/menu/item/1/edit/', {
            'name': "Booze",
            'description': 'Get you drunk',
            'chef':1,
            'standard':False,
            'ingredients':[self.ingredient]
        })
        self.assertEqual(response.status_code, 302)

