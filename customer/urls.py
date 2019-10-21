

from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'customer'

urlpatterns=[
url(r'^view_profile$', views.view_profile, name='view_profile'),
url(r'^edit_profile$', views.edit_profile, name='edit_profile'),
url(r'^show_doctor$', views.show_doctor, name='show_doctor'),
url(r'^book_slot/(?P<id>[0-9]+)/(?P<date>\d{4}-\d{2}-\d{2})?$', views.book_slot, name='book_slot'),
url(r'^book_particular_slot/(?P<id>[0-9]+)$', views.book_particular_slot, name='book_particular_slot'),
url(r'^cancel_particular_slot/(?P<id>[0-9]+)$', views.cancel_particular_slot, name='cancel_particular_slot'),
url(r'^get_booked_slots/(?P<date>\d{4}-\d{2}-\d{2})?$', views.get_booked_slots, name='get_booked_slots'),
]