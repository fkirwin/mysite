from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from . import views

urlpatterns = [
    url(r'^$', views.menu_list, name='menu_list'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.edit_menu, name='menu_edit'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/new/$', views.create_new_menu, name='menu_new'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'^__debug__/', include(debug_toolbar.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)