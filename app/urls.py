from django.urls import path
from django.contrib import admin
from . import views

app_name = 'app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login_user, name='login'),
    path('logout', views.logout, name='logout'),
    path('registration', views.registration_user, name='registration'),
    path('delete/<int:pk>', views.delete_schedule.as_view(), name='delete'),
    path('<username>/<password>', views.index, name='index'),
    path('calendar', views.MyCalendar.as_view(), name='mycalendar'),
    path('mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'),  
    path('month_with_forms', views.MonthWithFormsCalendar.as_view(), name='month_with_forms'),
    path('month_with_forms/<int:year>/<int:month>/', views.MonthWithFormsCalendar.as_view(), name='month_with_forms'),
    path('month', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),  
]
