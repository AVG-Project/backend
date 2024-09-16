from django.contrib import admin
from users import models


users_models = [models.Profile, models.Offer, models.Benefit]

admin.site.register(users_models)



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


