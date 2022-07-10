from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.user_logout, name='user_logout'),
    path('cours/<int:cours_id>', views.cours, name="cours"),
    path('cours_index/', views.cours_index, name="cours_index"),
    path('cours_creation/', views.cours_creation, name="cours_creation"),
    # not used
    # path('shop/', views.shop, name="shop"),
]
