from django.contrib import admin
# from django.urls import url
from django.urls import path

from django.conf import settings # for imgae/media
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from Login_app import views
app_name = 'Login_app'


urlpatterns = [
    path('',views.home, name='home',),
    path('register/', views.register, name='register'),
    path('login_page/', views.login_page, name='login_page'),
    path('user_login/', views.user_login, name='user_login'),

    path('logout/', views.user_logout, name='logout')

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
