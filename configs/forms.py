from django import forms
from .models import Automobiles


class FindByStageForm(forms.Form):
    stage1 = forms.BooleanField(label="Конфигурации 1-ой стадии", initial=True, required=False)
    stage2 = forms.BooleanField(label="Конфигурации 2-ой стадии", required=False)
    stage3 = forms.BooleanField(label="Конфигурации 3-ей стадии", required=False)
    stage3plus = forms.BooleanField(label="Конфигурации 3+ стадии", required=False)


class FindByAuto(forms.Form):
    automobiles = Automobiles.objects.all().order_by('make').distinct()
    makechoices = (('Default', 'Любая'),)
    for field in automobiles:
        if not (field.make, field.make) in makechoices:
            makechoices += (field.make, field.make),
    make = forms.ChoiceField(label="Выберите марку автомобиля", choices=makechoices, required=False)
    model = None
    generation = None
    engine = None


class ChooseAutoForm(forms.Form):
    automobiles = Automobiles.objects.all().order_by('make').distinct()
    makechoices = (('Default', '-'),)
    for field in automobiles:
        if not (field.make, field.make) in makechoices:
            makechoices += (field.make, field.make),
    make = forms.ChoiceField(label="Выберите марку автомобиля", choices=makechoices, required=False)
    model = None
    generation = None
    engine = None


class S1ConfigForm(forms.Form):
    name = forms.CharField(label="Название конфигурации", max_length=50)
    description = forms.CharField(label="Описание конфигурации", widget=forms.Textarea)
    new_power = forms.IntegerField(label="Новая мощность")
    new_torque = forms.IntegerField(label="Новый крутящий момент")


class S2ConfigForm(forms.Form):
    fk_stage1 = None
    name = forms.CharField(label="Название конфигурации", max_length=50)
    description = forms.CharField(label="Описание конфигурации", widget=forms.Textarea)
    intake_system = forms.CharField(label="Новая система впуска", max_length=50)
    exhaust_system = forms.CharField(label="Новая система выпуска", max_length=50)
    new_power = forms.IntegerField(label="Новая мощность")
    new_torque = forms.IntegerField(label="Новый крутящий момент")


class S3ConfigForm(forms.Form):
    fk_stage2 = None
    name = forms.CharField(label="Название конфигурации", max_length=50)
    description = forms.CharField(label="Описание конфигурации", widget=forms.Textarea)
    turbocharger = forms.CharField(label="Новая турбина/Новый компрессор", max_length=50)
    new_power = forms.IntegerField(label="Новая мощность")
    new_torque = forms.IntegerField(label="Новый крутящий момент")


class S3PlusConfigForm(forms.Form):
    fk_stage3 = None
    name = forms.CharField(label="Название конфигурации", max_length=50)
    description = forms.CharField(label="Описание конфигурации", widget=forms.Textarea)
    details = forms.CharField(label="Список деталей, необходимых для реализации конфигурации", widget=forms.Textarea)
    new_power = forms.IntegerField(label="Новая мощность")
    new_torque = forms.IntegerField(label="Новый крутящий момент")
