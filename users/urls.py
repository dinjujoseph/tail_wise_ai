from django.urls import path
from .views import home, profile, RegisterView,dog_profile,dog_profile_edit,delete_dog_profile,watch_my_dog,get_dog_status,send_mail_nofitication

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('dog_profile/', dog_profile, name='dog-profile'),
    path('edit_dog_profile/', dog_profile_edit, name='dog-profile-edit'),
    path('delete_dog_profile/',delete_dog_profile,name='delete_dog_profile'),
    path('send_mail_nofitication',send_mail_nofitication,name='send_mail_nofitication'),
    path('watch_my_dog/',watch_my_dog,name='watch_my_dog'),
    path('get_dog_status',get_dog_status),
]
