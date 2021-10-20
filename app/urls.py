from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout, name='logout'),
    path('registration', views.registration_user, name='registration'),
    path('<username>/<password>', views.index, name='index'),
    path('calender', views.MonthWithFormsCalendar.as_view(), name='month_with_forms'),
    path('month_with_forms/<int:year>/<int:month>/', views.MonthWithFormsCalendar.as_view(), name='month_with_forms'),
    path('month', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
]
