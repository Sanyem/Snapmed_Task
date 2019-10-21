"""
UserAuth URL Configuration

1. /doc_signup ---> For the Doctor Signup
2. /doc_login ---> For the Doctor Login
3. /user_signup ---> For the user/patient/customer Signup
4. /user_login ---> For the user/patient/customer Login
5. /logout ---> For logging out a user. (Logout Button is present after logging in)

"""
from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'UserAuth'

urlpatterns=[
url(r'^doc_signup/(?P<message>.*)$', views.doc_signup, name='doc_signup'),
url(r'^doc_login/(?P<message>.*)$', views.doc_login, name='doc_login'),
url(r'^user_signup/(?P<message>.*)$', views.user_signup, name='user_signup'),
url(r'^user_login/(?P<message>.*)$', views.user_login, name='user_login'),
url(r'^logout$', views.logout, name='logout'),
url(r'^$', views.home, name='home'),
]