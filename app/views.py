from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User

from .forms import RegistrationForm, LoginForm

from django.db.models import Q

from django.contrib.auth import authenticate, login, logout as django_logout
from django.core.paginator import Paginator
from django.core.validators import ValidationError

from django.views import generic
from . import mixins

import base64

import datetime
from .forms import BS4ScheduleForm
from .forms import SimpleScheduleForm
from .models import Schedule

from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.views import APIView

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

def login_user(request):
    params = {
        'login_form': LoginForm(),
    }
    if request.method == 'POST':
        params['login_form'] = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        username = request.POST['username']
        password = request.POST['password']
        username2 = base64.b64encode(username.encode())
        password2 = base64.b64encode(password.encode())
        if user is not None:
            login(request, user)
            return redirect('index', username=username2, password=password2)
        else:
            params['login_form'].add_error(None, "ユーザ名またはパスワードが異なります")
            return render(request, 'app/login.html', params)
    return render(request, 'app/login.html', params)
    #アカウントとパスワードが合致したら、その人専用の投稿画面に遷移する
    #アカウントとパスワードが合致しなかったら、エラーメッセージ付きのログイン画面に遷移する

def registration_user(request):
    params = {
        'registration_form': RegistrationForm(),
    }
    if request.method == 'POST':
        params['registration_form'] = RegistrationForm(request.POST)
        if request.POST['email'].rsplit('@',1)[1] != 's.tsukuba.ac.jp' and request.POST['email'].rsplit('@',1)[1] != 'alumuni.tsukuba.ac.jp':
            params['registration_form'].add_error('email', "筑波大学のemailアカウントを使用してください。\n\n使用できるメールアドレス: sアド, alumuni")
        if params['registration_form'].has_error('email'):
            return render(request, 'app/registration.html', params)
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        return redirect('login')
    return render(request, 'app/registration.html', params)

def index(request, username, password):
    username_index = username.split("'")
    username = username_index[1]
    username3 = base64.b64decode(username).decode()

    password_index = password.split("'")
    password = password_index[1]
    password3 = base64.b64decode(password).decode()

    user = authenticate(username=username3, password=password3)
    params = {
        'user': user,
    }
    if user is None:
        return redirect('login')
    return render(request, 'app/index.html', params)

def logout(request):
    django_logout(request)
    return render(request, 'app/logout.html')

""" @require_POST """
class delete_schedule(DeleteView):
    template_name = 'app/delete.html'
    model = Schedule

    date = datetime.date.today()
    success_url = reverse_lazy('mycalendar')

""" def delete(request, schedule_id):
    schedule = get_object_or_404(Schedule, id = schedule_id)
    schedule.delete()
    return redirect('calendar')
 """

class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'app/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class MyCalendar(mixins.MonthCalendarMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'app/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    """ def get(self, request, **kwargs):
        if "query_param" in request.GET:
            param_value = request.GET.get("query_param")
            return param_value
        else:
            context = self.get_month_calendar()
            return render(request, self.template_name, context) """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('mycalendar', year=date.year, month=date.month, day=date.day)

class MonthWithFormsCalendar(mixins.MonthWithFormsMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_forms.html'
    model = Schedule
    date_field = 'date'
    form_class = SimpleScheduleForm

    def get(self, request, **kwargs):
        context = self.get_month_calendar()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_month_calendar()
        formset = context['month_formset']
        if formset.is_valid():
            formset.save()
            return redirect('month_with_forms')

        return render(request, self.template_name, context)
