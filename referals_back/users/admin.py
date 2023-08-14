from django.contrib import admin
from .models import Referal, User, SmsCode
from django.db import models
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea


# базовая админка
class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at'] 


# настройка пользовательского интерфеса в админке
class UserAdminConfig(UserAdmin):
    model = User

    search_fields = ('phone', 'email', 'first_name', 'last_name', 'user_ref')
    list_filter = ('phone', 'email', 'user_ref', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('phone', 'email', 'user_ref', 'first_name', 'last_name', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'first_name','last_name', 'user_ref')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        (None, {'fields': ('id', 'date_joined',)}),
    )
    
    readonly_fields=('id', 'date_joined', 'user_ref')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


# админка для sms
class SmsCodeModelAdmin(admin.ModelAdmin):
    readonly_fields = ('code', )


admin.site.register(SmsCode, SmsCodeModelAdmin)

admin.site.register(User, UserAdminConfig)

admin.site.register(Referal, BaseModelAdmin)
