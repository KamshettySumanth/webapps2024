from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('all/admins/', views.admins, name="admins"),
    path('add/admin/', views.add_admin, name="add-admin"),
    path('delete/<uuid:user>/admin/', views.delete_admin, name="delete-admin")
]
