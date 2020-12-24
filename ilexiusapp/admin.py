from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.is_active:
            return ('login_count','employee_id', )
        else:
            return ('login_count',)

def login_user(sender, request, user, **kwargs):
    user.userprofile.login_count = user.userprofile.login_count + 1
    user.userprofile.save()

user_logged_in.connect(login_user)

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ("username","email","first_name","last_name","is_staff","employee_id")
    change_form_template = "../templates/change_form.html"

    def employee_id(self, obj):
        return obj.userprofile.employee_id

    def change_view(self, request, object_id, form_url='', extra_context=None,):
        user = User.objects.get(pk=object_id)
        context = {}
        context.update(extra_context or {})
        context.update({ 'user': user if user.is_superuser else None,})
        return super(UserAdmin, self).change_view(request, object_id, form_url, context)
        
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
