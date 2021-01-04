from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# from django.contrib import admin
# from django.contrib.auth.models import Group

# admin.site.unregister(Group)
# admin.site.register(UserProfile)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields': (
                    'usertype',
                    'approved',
                )
            }
        ),
        ('Security',
         {
             'fields': (
                 'securityquestion',
                 'securityanswer',
             )
         }),

        ('Deactive days',
         {
             'fields': (
                 'is_suspended',
                 'deactivetimestart',
                 'deactivetimeend',
             )
         }),

        ('Address',
         {
             'fields': (
                 'address',
             )
         }),

    )


admin.site.register(CustomUser, CustomUserAdmin)
