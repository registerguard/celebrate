from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)
from .models import RegisterGuardMemory

class RegisterGuardMemoryAdmin(ModelAdmin):
    model = RegisterGuardMemory
    menu_label = 'RG memory'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False

modeladmin_register(RegisterGuardMemoryAdmin)
