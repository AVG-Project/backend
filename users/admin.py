from django.contrib import admin
from users import models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, CustomUserChangeForm


from django.contrib.auth import get_user_model
User = get_user_model()

users_models = [models.Offer, models.Benefit]
admin.site.register(users_models)

## UserAdmin
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    # change_password_form = AdminPasswordChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'phone', 'is_staff')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Персональная информация', {'fields': ('last_name', 'first_name', 'patronymic', 'birth_date',
                                                'mailing', 'personal_data_processing')}),
        ('Уровни допуска', {'fields': ('is_superuser', 'is_staff', 'is_active', 'is_verified')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)

## UserAdmin


### Loyalty
class LoyaltyBenefitInline(admin.TabularInline):
    model = models.LoyaltyBenefit

class LoyaltyOfferInline(admin.TabularInline):
    model = models.LoyaltyOffer

@admin.register(models.Loyalty)
class LoyaltyAdmin(admin.ModelAdmin):
    model = models.Loyalty
    list_display = ['user', 'user_id', 'code', 'card_number', 'balance', 'show_all_offers']
    inlines = [LoyaltyBenefitInline, LoyaltyOfferInline]
### Loyalty


