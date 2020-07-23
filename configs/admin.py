from django.contrib import admin
from configs.models import Automobiles, Stage1Configs, Stage2Configs
from configs.models import Stage3Configs, Stage3PlusConfigs, Marks

admin.site.register(Automobiles)
admin.site.register(Stage1Configs)
admin.site.register(Stage2Configs)
admin.site.register(Stage3Configs)
admin.site.register(Stage3PlusConfigs)
admin.site.register(Marks)
