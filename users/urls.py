from django.urls import path
from .views import home, profile, RegisterView,dog_profile,dog_profile_edit,delete_dog_profile

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('dog_profile/', dog_profile, name='dog-profile'),
    path('edit_dog_profile/', dog_profile_edit, name='dog-profile-edit'),
    path('delete_dog_profile/',delete_dog_profile,name='delete_dog_profile'),
]
