from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from . import views

urlpatterns = [
    url(r'^$', views.menu_list, name='menu_list'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'sign_in/$', views.sign_in, name='sign_in'),
    url(r'sign_out/$', views.sign_out, name='sign_out'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.edit_menu, name='menu_edit'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/new/$', views.create_new_menu, name='menu_new'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'^menu/item/(?P<pk>\d+)/edit/$', views.edit_item, name='item_edit'),
    url(r'^__debug__/', include(debug_toolbar.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
