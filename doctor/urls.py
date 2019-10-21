
from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'doctor'

urlpatterns=[
url(r'^view_doc_profile$', views.view_doc_profile, name='view_doc_profile'),
url(r'^edit_doc_profile$', views.edit_doc_profile, name='edit_doc_profile'),
url(r'^add_slot/(?P<message>.*)$', views.add_slot, name='add_slot'),
url(r'^view_slot/(?P<date>\d{4}-\d{2}-\d{2})?$', views.view_slot, name='view_slot'),
url(r'^edit_slot/(?P<id>[0-9]+)/(?P<message>.*)$', views.edit_slot, name='edit_slot'),
url(r'^delete_slot/(?P<id>[0-9]+)$', views.delete_slot, name='delete_slot'),
# url(r'^view_slot/(?P<date>\d{4}-\d{2}-\d{2})$', views.view_slot_date, name='view_slot_date'),
]