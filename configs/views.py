from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.contrib.auth.models import User
from .forms import FindByStageForm, FindByAuto, ChooseAutoForm
from .forms import S1ConfigForm, S2ConfigForm, S3ConfigForm, S3PlusConfigForm
from .models import Automobiles, Marks
from .models import Stage1Configs, Stage2Configs
from .models import Stage3Configs, Stage3PlusConfigs


def index(request):
    s1configs = []
    s2configs = []
    s3configs = []
    s4configs = []

    if request.method == 'GET':
        form1 = FindByStageForm()
        s1configs.append(Stage1Configs.objects.all())
        # configs = ()
        # configs += s1configs,

        form2 = FindByAuto()
        modelchoices = (('Default', 'Любая'),)
        generationchoices = (('Default', 'Любое'),)
        enginechoices = (('Default', 'Любой'),)
        form2.fields['model'] = forms.ChoiceField(label="Выберите модель автомобиля", choices=modelchoices, required=False)
        form2.fields['generation'] = forms.ChoiceField(label="Выберите поколение автомобиля", choices=generationchoices, required=False)
        form2.fields['engine'] = forms.ChoiceField(label="Выберите двигатель автомобиля", choices=enginechoices, required=False)

    if request.method == 'POST':
        form1 = FindByStageForm(request.POST)
        form2 = FindByAuto(request.POST)
        modelchoices = (('Default', 'Любая'),)
        generationchoices = (('Default', 'Любое'),)
        enginechoices = (('Default', 'Любой'),)
        form2.fields['model'] = forms.ChoiceField(label="Выберите модель автомобиля", choices=modelchoices, required=False)
        form2.fields['generation'] = forms.ChoiceField(label="Выберите поколение автомобиля", choices=generationchoices, required=False)
        form2.fields['engine'] = forms.ChoiceField(label="Выберите двигатель автомобиля", choices=enginechoices, required=False)
        # configs = ()
        isForm1 = False
        isForm2 = False
        print(request.POST)
        if request.POST['this'] == "form1":
            isForm1 = True
        elif request.POST['this'] == "form2":
            isForm2 = True
        else:
            isForm1 = False
            isForm2 = False

        if isForm1:
            if form1.is_valid():
                current_val1 = form1.cleaned_data['stage1']
                current_val2 = form1.cleaned_data['stage2']
                current_val3 = form1.cleaned_data['stage3']
                current_val4 = form1.cleaned_data['stage3plus']

                if current_val1 is True:
                    s1configs.append(Stage1Configs.objects.all())
                    # configs += s1configs,
                if current_val2 is True:
                    s2configs.append(Stage2Configs.objects.all())
                    # configs += s2configs,
                if current_val3 is True:
                    s3configs.append(Stage3Configs.objects.all())
                    # configs += s3configs,
                if current_val4 is True:
                    s4configs.append(Stage3PlusConfigs.objects.all())
                    # configs += s4configs,

        if isForm2:
            # if form2.is_valid():
                # processing data from form2
                make = form2.data['make']
                model = form2.data['model']
                generation = form2.data['generation']
                engine = form2.data['engine']
                print(make, model, generation, engine)

                if make == "Default":
                    automobiles = Automobiles.objects.all()
                elif model == "Default":
                    automobiles = Automobiles.objects.filter(make=make)
                elif generation == "Default":
                    automobiles = Automobiles.objects.filter(make=make).filter(model=model)
                elif engine == "Default":
                    automobiles = Automobiles.objects.filter(make=make).filter(model=model).filter(generation=generation)
                else:
                    automobiles = Automobiles.objects.filter(make=make).filter(model=model).filter(generation=generation).filter(engine=engine)

                for auto in automobiles:
                    s1configs.append(Stage1Configs.objects.filter(fk_automobile=auto.id))
                    s2configs.append(Stage2Configs.objects.filter(fk_automobile=auto.id))
                    s3configs.append(Stage3Configs.objects.filter(fk_automobile=auto.id))
                    s4configs.append(Stage3PlusConfigs.objects.filter(fk_automobile=auto.id))

                # configs += s1configs,
                # configs += s2configs,
                # configs += s3configs,
                # configs += s4configs,
                form2 = FindByAuto()
                modelchoices = (('Default', 'Любая'),)
                generationchoices = (('Default', 'Любое'),)
                enginechoices = (('Default', 'Любой'),)
                form2.fields['model'] = forms.ChoiceField(label="Выберите модель автомобиля", choices=modelchoices, required=False)
                form2.fields['generation'] = forms.ChoiceField(label="Выберите поколение автомобиля", choices=generationchoices, required=False)
                form2.fields['engine'] = forms.ChoiceField(label="Выберите двигатель автомобиля", choices=enginechoices, required=False)

    return render(request, 'configs/index.html', {
        'form1': form1, 'form2': form2, 's1configs': s1configs,
        's2configs': s2configs, 's3configs': s3configs, 's4configs': s4configs
    })


def check_make(request):
    if request.method == 'GET':
        make = request.GET["make"]
        auto = Automobiles.objects.filter(make=make).order_by('model')
        models = ()
        response = HttpResponse()
        for field in auto:
            if not (field.model, field.model) in models:
                models += (field.model, field.model),
                response.write(field.model)
                response.write("__br__")
        return response
    else:
        pass


def check_model(request):
    if request.method == 'GET':
        make = request.GET["make"]
        model = request.GET["model"]
        auto = Automobiles.objects.filter(make=make).filter(model=model).order_by('generation')
        generations = ()
        response = HttpResponse()
        for field in auto:
            if not (field.generation, field.generation) in generations:
                generations += (field.generation, field.generation),
                response.write(field.generation)
                response.write("__br__")
        return response
    else:
        pass


def check_generation(request):
    if request.method == 'GET':
        make = request.GET["make"]
        model = request.GET["model"]
        generation = request.GET["generation"]
        auto = Automobiles.objects.filter(make=make).filter(model=model).filter(generation=generation).order_by('engine')
        engines = ()
        response = HttpResponse()
        for field in auto:
            if not (field.engine, field.engine) in engines:
                engines += (field.engine, field.engine),
                response.write(field.engine)
                response.write("__br__")
        return response
    else:
        pass


def rate_stage1(request):
    if request.method == "GET":
        rate_charact = request.GET['rate_charact']
        rate_reliability = request.GET['rate_reliability']
        user_id = request.GET['user']
        config_id = request.GET['config']
        user = User.objects.get(id=user_id)
        config = Stage1Configs.objects.get(id=config_id)
        err = True
        response = HttpResponse()
        try:
            Marks.objects.filter(fk_stage1=config).get(fk_user=user)
        except Marks.DoesNotExist:
            print("error Marks.DoesNotExist")
            err = False
        if not err:
            mark = Marks(
                fk_user=user, fk_stage1=config, charact_mark=rate_charact, reliability_mark=rate_reliability
            )
            mark.save()
            marks_count = Marks.objects.filter(fk_stage1=config).count()
            charact_count = Marks.objects.filter(fk_stage1=config).aggregate(Avg('charact_mark'))
            charact_count = float(charact_count['charact_mark__avg'])
            reliability_count = Marks.objects.filter(fk_stage1=config).aggregate(Avg('reliability_mark'))
            reliability_count = float(reliability_count['reliability_mark__avg'])
            response.write("__acc__")
            response.write(marks_count)
            response.write("__br__")
            response.write(charact_count)
            response.write("__br__")
            response.write(reliability_count)
        else:
            err_msg = "Вы уже делали оценку данной конфигурации!"
            response.write("__err__")
            response.write(err_msg)
        return response
    else:
        pass


def rate_stage2(request):
    if request.method == "GET":
        rate_charact = request.GET['rate_charact']
        rate_reliability = request.GET['rate_reliability']
        user_id = request.GET['user']
        config_id = request.GET['config']
        user = User.objects.get(id=user_id)
        config = Stage2Configs.objects.get(id=config_id)
        err = True
        response = HttpResponse()
        try:
            Marks.objects.filter(fk_stage2=config).get(fk_user=user)
        except Marks.DoesNotExist:
            print("error Marks.DoesNotExist")
            err = False
        if not err:
            mark = Marks(
                fk_user=user, fk_stage2=config, charact_mark=rate_charact, reliability_mark=rate_reliability
            )
            mark.save()
            marks_count = Marks.objects.filter(fk_stage2=config).count()
            charact_count = Marks.objects.filter(fk_stage2=config).aggregate(Avg('charact_mark'))
            charact_count = float(charact_count['charact_mark__avg'])
            reliability_count = Marks.objects.filter(fk_stage2=config).aggregate(Avg('reliability_mark'))
            reliability_count = float(reliability_count['reliability_mark__avg'])
            response.write("__acc__")
            response.write(marks_count)
            response.write("__br__")
            response.write(charact_count)
            response.write("__br__")
            response.write(reliability_count)
        else:
            err_msg = "Вы уже делали оценку данной конфигурации!"
            response.write("__err__")
            response.write(err_msg)
        return response
    else:
        pass


def rate_stage3(request):
    if request.method == "GET":
        rate_charact = request.GET['rate_charact']
        rate_reliability = request.GET['rate_reliability']
        user_id = request.GET['user']
        config_id = request.GET['config']
        user = User.objects.get(id=user_id)
        config = Stage3Configs.objects.get(id=config_id)
        err = True
        response = HttpResponse()
        try:
            Marks.objects.filter(fk_stage3=config).get(fk_user=user)
        except Marks.DoesNotExist:
            print("error Marks.DoesNotExist")
            err = False
        if not err:
            mark = Marks(
                fk_user=user, fk_stage3=config, charact_mark=rate_charact, reliability_mark=rate_reliability
            )
            mark.save()
            marks_count = Marks.objects.filter(fk_stage3=config).count()
            charact_count = Marks.objects.filter(fk_stage3=config).aggregate(Avg('charact_mark'))
            charact_count = float(charact_count['charact_mark__avg'])
            reliability_count = Marks.objects.filter(fk_stage3=config).aggregate(Avg('reliability_mark'))
            reliability_count = float(reliability_count['reliability_mark__avg'])
            response.write("__acc__")
            response.write(marks_count)
            response.write("__br__")
            response.write(charact_count)
            response.write("__br__")
            response.write(reliability_count)
        else:
            err_msg = "Вы уже делали оценку данной конфигурации!"
            response.write("__err__")
            response.write(err_msg)
        return response
    else:
        pass


def rate_stage3plus(request):
    if request.method == "GET":
        rate_charact = request.GET['rate_charact']
        rate_reliability = request.GET['rate_reliability']
        user_id = request.GET['user']
        config_id = request.GET['config']
        user = User.objects.get(id=user_id)
        config = Stage3PlusConfigs.objects.get(id=config_id)
        err = True
        response = HttpResponse()
        try:
            Marks.objects.filter(fk_stage3plus=config).get(fk_user=user)
        except Marks.DoesNotExist:
            print("error Marks.DoesNotExist")
            err = False
        if not err:
            mark = Marks(
                fk_user=user, fk_stage3plus=config, charact_mark=rate_charact, reliability_mark=rate_reliability
            )
            mark.save()
            marks_count = Marks.objects.filter(fk_stage3plus=config).count()
            charact_count = Marks.objects.filter(fk_stage3plus=config).aggregate(Avg('charact_mark'))
            charact_count = float(charact_count['charact_mark__avg'])
            reliability_count = Marks.objects.filter(fk_stage3plus=config).aggregate(Avg('reliability_mark'))
            reliability_count = float(reliability_count['reliability_mark__avg'])
            response.write("__acc__")
            response.write(marks_count)
            response.write("__br__")
            response.write(charact_count)
            response.write("__br__")
            response.write(reliability_count)
        else:
            err_msg = "Вы уже делали оценку данной конфигурации!"
            response.write("__err__")
            response.write(err_msg)
        return response
    else:
        pass


def check_stage1(request, pk):
    stage1 = Stage1Configs.objects.get(id=pk)
    auto = stage1.fk_automobile
    user = stage1.fk_userid
    marks_count = Marks.objects.filter(fk_stage1=stage1).count()
    charact_count = Marks.objects.filter(fk_stage1=stage1).aggregate(Avg('charact_mark'))
    try:
        charact_count = float(charact_count['charact_mark__avg'])
    except TypeError:
        charact_count = "0.0"
    reliability_count = Marks.objects.filter(fk_stage1=stage1).aggregate(Avg('reliability_mark'))
    try:
        reliability_count = float(reliability_count['reliability_mark__avg'])
    except TypeError:
        reliability_count = "0.0"
    return render(request, "configs/stage1.html", {
        'stage1': stage1, 'auto': auto, 'name_user': user.username,
        'marks_count': marks_count, 'charact_count': charact_count,
        'reliability_count': reliability_count
    })


def check_stage2(request, pk):
    stage2 = Stage2Configs.objects.get(id=pk)
    stage1 = stage2.fk_stage1
    auto = stage2.fk_automobile
    user = stage2.fk_userid
    marks_count = Marks.objects.filter(fk_stage2=stage2).count()
    charact_count = Marks.objects.filter(fk_stage2=stage2).aggregate(Avg('charact_mark'))
    try:
        charact_count = float(charact_count['charact_mark__avg'])
    except TypeError:
        charact_count = "0.0"
    reliability_count = Marks.objects.filter(fk_stage2=stage2).aggregate(Avg('reliability_mark'))
    try:
        reliability_count = float(reliability_count['reliability_mark__avg'])
    except TypeError:
        reliability_count = "0.0"
    return render(request, "configs/stage2.html", {
        'stage2': stage2, 'stage1': stage1, 'auto': auto,
        'name_user': user.username, 'marks_count': marks_count,
        'charact_count': charact_count, 'reliability_count': reliability_count
    })


def check_stage3(request, pk):
    stage3 = Stage3Configs.objects.get(id=pk)
    stage2 = stage3.fk_stage2
    stage1 = stage2.fk_stage1
    auto = stage3.fk_automobile
    user = stage3.fk_userid
    marks_count = Marks.objects.filter(fk_stage3=stage3).count()
    charact_count = Marks.objects.filter(fk_stage3=stage3).aggregate(Avg('charact_mark'))
    try:
        charact_count = float(charact_count['charact_mark__avg'])
    except TypeError:
        charact_count = "0.0"
    reliability_count = Marks.objects.filter(fk_stage3=stage3).aggregate(Avg('reliability_mark'))
    try:
        reliability_count = float(reliability_count['reliability_mark__avg'])
    except TypeError:
        reliability_count = "0.0"
    return render(request, "configs/stage3.html", {
        'stage3': stage3, 'stage2': stage2, 'stage1': stage1,
        'auto': auto, 'name_user': user.username, 'marks_count': marks_count,
        'charact_count': charact_count, 'reliability_count': reliability_count
    })


def check_stage3plus(request, pk):
    stage3plus = Stage3PlusConfigs.objects.get(id=pk)
    stage3 = stage3plus.fk_stage3
    stage2 = stage3.fk_stage2
    stage1 = stage2.fk_stage1
    auto = stage3plus.fk_automobile
    user = stage3plus.fk_userid
    marks_count = Marks.objects.filter(fk_stage3plus=stage3plus).count()
    charact_count = Marks.objects.filter(fk_stage3plus=stage3plus).aggregate(Avg('charact_mark'))
    try:
        charact_count = float(charact_count['charact_mark__avg'])
    except TypeError:
        charact_count = "0.0"
    reliability_count = Marks.objects.filter(fk_stage3plus=stage3plus).aggregate(Avg('reliability_mark'))
    try:
        reliability_count = float(reliability_count['reliability_mark__avg'])
    except TypeError:
        reliability_count = "0.0"
    return render(request, "configs/stage3plus.html", {
        'stage3plus': stage3plus, 'stage3': stage3, 'stage2': stage2,
        'stage1': stage1, 'auto': auto, 'name_user': user.username,
        'marks_count': marks_count, 'charact_count': charact_count,
        'reliability_count': reliability_count
    })


def new_config_one(request, pk):
    if request.method == "GET":
        form = ChooseAutoForm()
        modelchoices = (('Default', '-'),)
        generationchoices = (('Default', '-'),)
        enginechoices = (('Default', '-'),)
        form.fields['model'] = forms.ChoiceField(label="Выберите модель автомобиля", choices=modelchoices, required=False)
        form.fields['generation'] = forms.ChoiceField(label="Выберите поколение автомобиля", choices=generationchoices, required=False)
        form.fields['engine'] = forms.ChoiceField(label="Выберите двигатель автомобиля", choices=enginechoices, required=False)

    if request.method == "POST":
        form = ChooseAutoForm(request.POST)
        make = form.data['make']
        model = form.data['model']
        generation = form.data['generation']
        engine = form.data['engine']
        auto = Automobiles.objects.get(
            make=make, model=model, generation=generation, engine=engine
        )
        url = "http://127.0.0.1:8000/configs/new_config/phase2/" + str(pk) + "/" + str(auto.id)
        return redirect(url)

    return render(request, 'configs/choose_auto.html', {
        'form': form
    })


def new_config_two(request, user_pk, auto_pk):
    if request.method == "GET":
        form1 = S1ConfigForm()
        form2 = S2ConfigForm()
        form3 = S3ConfigForm()
        form4 = S3PlusConfigForm()

        s1choices = (('Default', '-'),)
        s2choices = (('Default', '-'),)
        s3choices = (('Default', '-'),)
        s1configs = Stage1Configs.objects.filter(fk_automobile=auto_pk)
        s2configs = Stage2Configs.objects.filter(fk_automobile=auto_pk)
        s3configs = Stage3Configs.objects.filter(fk_automobile=auto_pk)
        for config in s1configs:
            s1choices += (config.name, config.name),
        for config in s2configs:
            s2choices += (config.name, config.name),
        for config in s3configs:
            s3choices += (config.name, config.name),
        form2.fields['fk_stage1'] = forms.ChoiceField(label="Выберите предыдущую конфигурацию", choices=s1choices)
        form3.fields['fk_stage2'] = forms.ChoiceField(label="Выберите предыдущую конфигурацию", choices=s2choices)
        form4.fields['fk_stage3'] = forms.ChoiceField(label="Выберите предыдущую конфигурацию", choices=s3choices)

    if request.method == "POST":
        form1 = S1ConfigForm(request.POST)
        form2 = S2ConfigForm(request.POST)
        form3 = S3ConfigForm(request.POST)
        form4 = S3PlusConfigForm(request.POST)
        user = User.objects.get(id=user_pk)
        auto = Automobiles.objects.get(id=auto_pk)
        isForm1 = False
        isForm2 = False
        isForm3 = False
        isForm4 = False

        if request.POST['this'] == "form1":
            isForm1 = True
        elif request.POST['this'] == "form2":
            isForm2 = True
        elif request.POST['this'] == "form3":
            isForm3 = True
        elif request.POST['this'] == "form4":
            isForm4 = True
        else:
            isForm1 = False
            isForm2 = False
            isForm3 = False
            isForm4 = False

        if isForm1:
            name = form1.data['name']
            description = form1.data['description']
            new_power = form1.data['new_power']
            new_torque = form1.data['new_torque']
            s1 = Stage1Configs(
                fk_userid=user, fk_automobile=auto, name=name, description=description, new_power=new_power, new_torque=new_torque
            )
            s1.save()

        if isForm2:
            name = form2.data['name']
            description = form2.data['description']
            intake_system = form2.data['intake_system']
            exhaust_system = form2.data['exhaust_system']
            new_power = form2.data['new_power']
            new_torque = form2.data['new_torque']
            fk_stage1 = form2.data['fk_stage1']
            stage1 = Stage1Configs.objects.get(name=fk_stage1)
            s2 = Stage2Configs(
                fk_userid=user, fk_stage1=stage1, fk_automobile=auto, name=name, description=description, intake_system=intake_system, exhaust_system=exhaust_system, new_power=new_power, new_torque=new_torque
            )
            s2.save()

        if isForm3:
            name = form3.data['name']
            description = form3.data['description']
            turbocharger = form3.data['turbocharger']
            new_power = form3.data['new_power']
            new_torque = form3.data['new_torque']
            fk_stage2 = form3.data['fk_stage2']
            stage2 = Stage2Configs.objects.get(name=fk_stage2)
            s3 = Stage3Configs(
                fk_userid=user, fk_stage2=stage2, fk_automobile=auto, name=name, description=description, turbocharger=turbocharger, new_power=new_power, new_torque=new_torque
            )
            s3.save()

        if isForm4:
            name = form3.data['name']
            description = form3.data['description']
            details = form3.data['details']
            new_power = form3.data['new_power']
            new_torque = form3.data['new_torque']
            fk_stage3 = form3.data['fk_stage3']
            stage3 = Stage3Configs.objects.get(name=fk_stage3)
            s3plus = Stage3PlusConfigs(
                fk_userid=user, fk_stage3=stage3, fk_automobile=auto, name=name, description=description, details=details, new_power=new_power, new_torque=new_torque
            )
            s3plus.save()

        url = "http://127.0.0.1:8000/" + str(user_pk)
        return redirect(url)

    return render(request, 'configs/new_config.html', {
        'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4
    })
