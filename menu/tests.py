import os
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import *
from .forms import *


#View
class ViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='zoidberg', password='test')
        self.ingredient1 = Ingredient(name='Beer')
        self.ingredient1.save()
        self.ingredient2 = Ingredient(name='Juice')
        self.ingredient2.save()
        self.item1 = Item(name='Purple Drink', description='blah', chef=self.user, standard=True)
        self.item1.save()
        self.item1.ingredients = [self.ingredient1, self.ingredient2]
        self.item1.save()
        self.item2 = Item(name='Beers', description='crunk', chef=self.user, standard=True)
        self.item2.save()
        self.item2.ingredients = [self.ingredient1]
        self.item2.save()
        self.menu1 = Menu(season="Startime", expiration_date=None)
        self.menu1.save()
        self.menu1.items = [self.item1, self.item2]
        self.menu1.save()
        self.menu2 = Menu(season="Say hello to the bad guy.",
                          expiration_date=datetime.date.today() - timedelta(days=1000))
        self.menu2.save()
        self.menu2.items = [self.item1]
        self.menu2.save()

    def test_menu_list(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.menu2, resp.context['menus'])
        self.assertIn(self.menu1, resp.context['menus'])

    def test_menu_detail(self):
        resp = self.client.get(reverse('menu_detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(self.menu2, resp.context['menu'])
        self.assertEqual(self.menu1, resp.context['menu'])
        resp = self.client.get(reverse('menu_detail', kwargs={'pk': 10000}))
        self.assertEqual(resp.status_code, 404)

    def test_item_detail(self):
        resp = self.client.get(reverse('item_detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(self.item2, resp.context['item'])
        self.assertEqual(self.item1, resp.context['item'])
        resp = self.client.get(reverse('item_detail', kwargs={'pk': 10000}))
        self.assertEqual(resp.status_code, 404)

    def test_create_new_menu(self):
        self.client.login(username='zoidberg', password='test')
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='zoidberg', password='test')
        response = self.client.post('/menu/new/', data={'season': "June",
                                                        'items': ["1"],
                                                        'expiration_date': datetime.date.today()})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Menu.objects.count(), 3)

    def test_edit_menu(self):
        self.client.login(username='zoidberg', password='test')
        response = self.client.get(reverse('menu_edit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Startime", response.content.decode('utf-8'))
        self.client.login(username='zoidberg', password='test')
        response = self.client.post('/menu/1/edit/', data={'season': "July",
                                                           'items': ["1"],
                                                           'expiration_date': datetime.date.today()})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Menu.objects.get(season="July").id, 1)

    def test_edit_item(self):
        self.client.login(username='zoidberg', password='test')
        response = self.client.get(reverse('item_edit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Purple Drink", response.content.decode('utf-8'))
        self.client.login(username='zoidberg', password='test')
        response = self.client.post('/menu/item/1/edit/', data={'name': "Booze",
                                                                'description': 'Get you drunk',
                                                                'chef': 1,
                                                                'standard': False,
                                                                'ingredients': ["1"]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.get(name="Booze").id, 1)


class FormTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='zoidberg', password='test')
        ingredient1 = Ingredient(name='Beer')
        ingredient1.save()
        ingredient2 = Ingredient(name='Juice')
        ingredient2.save()
        item1 = Item(name='Purple Drink',
                     description='blah',
                     chef=self.user,
                     standard=True)
        item1.save()
        item1.ingredients = [ingredient1, ingredient2]
        item1.save()
        item2 = Item(name='Beers',
                     description='crunk',
                     chef=self.user,
                     standard=True)
        item2.save()
        item2.ingredients = [ingredient1]
        item2.save()
        menus = Menu(season="Startime",
                     expiration_date=None)
        menus.save()
        menus.items = [item1, item2]
        menus.save()
        self.item = Item.objects.first()
        self.ingredient = Ingredient.objects.first()

    def test_menu_form(self):
        good_form = MenuForm({
            'season': "June",
            'items': [self.item],
            'expiration_date': datetime.date.today(),
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
        self.assertEqual(good_form.data['expiration_date'], datetime.date.today())

    def test_item_form(self):
        good_form = ItemForm({
            'name': "Booze",
            'description': 'Get you drunk',
            'chef': 1,
            'standard': True,
            'ingredients': [self.ingredient]
        })
        bad_form = ItemForm({
            'name': None,
            'description': 'Get you drunk',
            'chef': self.user,
            'standard': True,
            'ingredients': [self.ingredient, 'turkey']
        })
        self.assertTrue(good_form.is_valid())
        self.assertFalse(bad_form.is_valid())
        self.assertEqual(good_form.data['name'], "Booze")
        self.assertEqual(good_form.data['ingredients'][0], self.ingredient)
        self.assertIsInstance(good_form.data['ingredients'][0], Ingredient)

