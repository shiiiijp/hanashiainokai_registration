from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout, name='logout'),
    path('registration', views.registration_user, name='registration'),
    path('<username>/<password>', views.index, name='index'),
    path('calender', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
]
