from django.conf import settings
from django.db import models


class Automobiles(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    generation = models.CharField(max_length=30)
    engine = models.CharField(max_length=30)
    power = models.PositiveIntegerField()
    torque = models.PositiveIntegerField()

    def __str__(self):
        return (
            self.make + ' ' + self.model + ' ' + self.generation + ' ' + self.engine
        )

    def get_make(self):
        return self.make

    def get_model(self):
        return self.model

    def get_generation(self):
        return self.generation

    def get_engine(self):
        return self.engine


class Stage1Configs(models.Model):
    fk_userid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    fk_automobile = models.OneToOneField(
        'Automobiles',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    new_power = models.PositiveIntegerField()
    new_torque = models.PositiveIntegerField()

    def __str__(self):
        return(
            'Конфигурация 1-ой стадии ' + self.fk_automobile.__str__()
        )

    def get_name(self):
        return self.name


class Stage2Configs(models.Model):
    fk_userid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    fk_stage1 = models.OneToOneField(
        'Stage1Configs',
        on_delete=models.CASCADE,
    )
    fk_automobile = models.OneToOneField(
        'Automobiles',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    new_power = models.PositiveIntegerField()
    new_torque = models.PositiveIntegerField()
    intake_system = models.CharField(max_length=50)
    exhaust_system = models.CharField(max_length=50)

    def __str__(self):
        return(
            'Конфигурация 2-ой стадии ' + self.fk_automobile.__str__()
        )

    def get_name(self):
        return self.name

    def get_intake_system(self):
        return self.intake_system

    def get_exhaust_system(self):
        return self.exhaust_system


class Stage3Configs(models.Model):
    fk_userid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    fk_stage2 = models.OneToOneField(
        'Stage2Configs',
        on_delete=models.CASCADE,
    )
    fk_automobile = models.OneToOneField(
        'Automobiles',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    new_power = models.PositiveIntegerField()
    new_torque = models.PositiveIntegerField()
    turbocharger = models.CharField(max_length=50)

    def __str__(self):
        return(
            'Конфигурация 3-ей стадии ' + self.fk_automobile.__str__()
        )

    def get_name(self):
        return self.name

    def get_turbocharger(self):
        return self.turbocharger


class Stage3PlusConfigs(models.Model):
    fk_userid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    fk_stage3 = models.OneToOneField(
        'Stage3Configs',
        on_delete=models.CASCADE,
    )
    fk_automobile = models.OneToOneField(
        'Automobiles',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    new_power = models.PositiveIntegerField()
    new_torque = models.PositiveIntegerField()
    details = models.TextField()

    def __str__(self):
        return(
            'Конфигурация 3+ стадии ' + self.fk_automobile.__str__()
        )

    def get_name(self):
        return self.name


class Marks(models.Model):
    fk_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    fk_stage1 = models.ForeignKey(
        'Stage1Configs',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    fk_stage2 = models.ForeignKey(
        'Stage2Configs',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    fk_stage3 = models.ForeignKey(
        'Stage3Configs',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    fk_stage3plus = models.ForeignKey(
        'Stage3PlusConfigs',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    charact_mark = models.DecimalField(max_digits=1, decimal_places=0)
    reliability_mark = models.DecimalField(max_digits=1, decimal_places=0)

    def __str__(self):
        return 'Оценка конфигурации от ' + self.fk_user.username
