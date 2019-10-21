"""snapmed URL Configuration

1. /admin ---> For the django-admin
2. /doctor ---> For the doctor side of the website
3. /customer ---> For the user/patient/customer side of the website
4. / ---> For the home page


"""
from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('UserAuth.urls', namespace='UserAuth')),
    url(r'^doctor/', include('doctor.urls', namespace='doctor')),
    url(r'^customer/', include('customer.urls', namespace='customer')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
