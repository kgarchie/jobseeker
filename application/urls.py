from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search, name='search'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),

    path('details/<int:id>/', views.details, name='job-details'),
    path('jobs/', views.jobs, name='jobs'),
    path('details/<int:id>/apply/', views.apply, name='apply'),
    path('update_pic/', views.update_pic, name='update_pic'),

    path('profile/', views.profile, name='profile'),
    path('update-details/', views.update_details, name='update'),
    path('profile/applied/', views.applied_jobs, name='applied'),

    path('about/', views.about, name='about'),
]
