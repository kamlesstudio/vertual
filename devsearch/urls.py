
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from payments import views
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url

from django.conf import settings

from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('projects.urls')),
    path('vendors/',include('users.urls')),
    path('pay/', views.home,name='pay'),
    path('pay/payment', views.payment,name='payment'),
    path('response/', (views.response)),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="reset_password.html"),name="reset_password"),
    path('response/', views.response),
   
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),name="password_reset_complete"),
     url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

  url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
