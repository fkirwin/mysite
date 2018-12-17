import os

import sqlite3
from sqlite3 import Error

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import *
from .forms import *

user = get_user_model().objects.create_user('zoidberg')
ingredient1 = Ingredient('Beer')
ingredient2 = Ingredient('Juice')
item1 = Item()
item2 = Item()
menus = Menu()

#Model
class ModelTests(TestCase):

    def test_new_menu_success(self):
        """lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')"""
        pass

    def test_new_menu_failure(self):
        pass

    def test_update_menu_item_success(self):
        pass

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

    def sign_in(self):
        pass

    def sign_up(self):
        pass

    def sign_out(self):
        pass


#Form
class FormTests(TestCase):

    def setUp(self):
        #self.user = get_user_model().objects.create_user('zoidberg')
        #self.item = Item.objects.first()
        #print(self.item)


    def test_valid_menu_data(self):
        form = MenuForm({
            'season': "June",
            'items': self.item,
            'expiration_date': None,
        })
        self.assertTrue(form.is_valid())
        menu = form.save()
        self.assertEqual(menu.season, "June")
        self.assertEqual(menu.items, self.item)
        self.assertIsInstance(menu.items[0], Item)
        self.assertEqual(menu.expiration_date, None)


    def test_blank_menu_data(self):
        pass
        '''
        form = CommentForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['required'],
            'email': ['required'],
            'body': ['required'],
        })

    def test_valid_item_data(self):
        form = CommentForm({
            'name': "Turanga Leela",
            'email': "leela@example.com",
            'body': "Hi there",
        }, entry=self.entry)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, "Turanga Leela")
        self.assertEqual(comment.email, "leela@example.com")
        self.assertEqual(comment.body, "Hi there")
        self.assertEqual(comment.entry, self.entry)

    def test_blank_item_data(self):
        form = CommentForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['required'],
            'email': ['required'],
            'body': ['required'],
        })

'''