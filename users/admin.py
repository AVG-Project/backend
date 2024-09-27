from django.contrib import admin
from users import models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


users_models = [models.Offer, models.Benefit]
admin.site.register(users_models)

### CustomUser
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)
### CustomUser


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


