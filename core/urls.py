from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('logout',views.Logout,name='logout'),
    path('settings',views.Settings,name='settings')

    

]
