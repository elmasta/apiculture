from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_option/', views.user_option, name="user_option"),
    path('user_signin/', views.user_signin, name="user_signin"),
    path('cours/<int:cours_id>', views.cours, name="cours"),
    path('cours_index/', views.cours_index, name="cours_index"),
    path('cours_creation/', views.cours_creation, name="cours_creation"),
    path('event_admin/', views.event_admin, name="event_admin"),
    path('event_creation/', views.event_creation, name="event_creation"),
    path('event_modif/<int:event_id>', views.event_modif, name="event_modif"),
    path('index_modif', views.index_modif, name="index_modif"),
    path('legal/', views.legal, name="legal"),
]
