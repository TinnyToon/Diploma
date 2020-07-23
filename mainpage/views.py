from django.shortcuts import render
# from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from configs.models import Stage1Configs, Stage2Configs
from configs.models import  Stage3Configs, Stage3PlusConfigs
# from django.urls import reverse
import datetime

from .forms import RegisterForm, UserDeleteForm, ChangeUserProfile
# from django.http import HttpResponse


def index(request):
    return render(request, 'mainpage/index.html')


def contact(request):
    return render(request, 'mainpage/basic.html')


def new_user_register(request):
    # Если данный запрос типа POST, тогда
    user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

    if request.method == 'POST':

        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RegisterForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            # (здесь мы просто присваиваем их полю due_back)
            # user.due_back = form.cleaned_data['renewal_date']
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['surname']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            clearPass = form.cleaned_data['password1']
            # HashPass = make_password(clearPass, None, 'md5')
            user.set_password(clearPass)
            user.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect('/accounts/login/')

    # Если это GET (или какой-либо еще), создать форму по умолчанию.
    else:
        user.delete()
        user = ''
        form = RegisterForm()

    return render(request, 'mainpage/new_user_register.html', {'form': form, 'user':user})


def delete_user(request, pk):
    if request.method == 'POST':
        form = UserDeleteForm(request.POST)

        if form.is_valid():
            user = User.objects.get(pk=pk)
            user.delete()

        return HttpResponseRedirect("/")

    else:
        form = UserDeleteForm()

    return render(request, 'mainpage/user_account.html', {'form': form})


def user_profile_change(request, pk):
    if request.method == 'POST':
        form = ChangeUserProfile(request.POST)
        form.set_pk(pk)
        form = form.get_fields()

        if form.is_valid():
            user = User.objects.get(pk=pk)
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['surname']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()

        return HttpResponseRedirect("/")

    else:
        form = ChangeUserProfile()
        form.set_pk(pk)
        form = form.get_fields()

    return render(request, 'mainpage/user_profile_change.html', {'form': form})


def check_user_configs(request, pk):
    if request.method == "GET":
        s1configs = []
        s2configs = []
        s3configs = []
        s4configs = []
        isempty = False
        s1query = Stage1Configs.objects.filter(fk_userid=pk)
        s2query = Stage2Configs.objects.filter(fk_userid=pk)
        s3query = Stage3Configs.objects.filter(fk_userid=pk)
        s4query = Stage3PlusConfigs.objects.filter(fk_userid=pk)
        if (not s1query) and (not s2query) and (not s3query) and (not s4query):
            isempty = True
        else:
            isempty = False

        s1configs.append(s1query)
        s2configs.append(s2query)
        s3configs.append(s3query)
        s4configs.append(s4query)

        report = request.META.get('HTTP_REFERER')

    if request.method == "POST":
        config = request.POST['config']
        config_id = request.POST['id']

        if config == "stage1":
            stage1 = Stage1Configs.objects.get(id=config_id)
            stage1.delete()
        elif config == "stage2":
            stage2 = Stage2Configs.objects.get(id=config_id)
            stage2.delete()
        elif config == "stage3":
            stage3 = Stage3Configs.objects.get(id=config_id)
            stage3.delete()
        elif config == "stage3plus":
            stage3plus = Stage3PlusConfigs.objects.get(id=config_id)
            stage3plus.delete()
        url = "http://127.0.0.1:8000/" + str(pk)
        return HttpResponseRedirect(url)

    return render(request, "mainpage/user_configs.html", {
        's1configs': s1configs, 's2configs': s2configs, 's3configs': s3configs, 's3plusconfigs': s4configs, 'isempty': isempty, 'report': report
    })


def check_user_exist(request):
    if request.method == "GET":
        user = request.GET['username']
        err = True
        try:
            User.objects.get(username=user)
        except User.DoesNotExist:
            err = False
        response = HttpResponse()
        if not err:
            response.write("ok")
        else:
            response.write("error")
        return response
    else:
        pass
