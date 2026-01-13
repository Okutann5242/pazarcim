from django.contrib import admin

from .models import (
    DiscountCode,
    IntegrationSetting,
    Payout,
    RefundRequest,
    ShippingMethod,
    StoreProfile,
    VariationOption,
    VariationType,
)


@admin.register(StoreProfile)
class StoreProfileAdmin(admin.ModelAdmin):
    list_display = ("store_name", "owner")
    search_fields = ("store_name", "owner__username", "owner__email")


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "percent", "is_active", "starts_at", "ends_at")
    list_filter = ("is_active",)
    search_fields = ("code",)


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "flat_fee", "is_active")
    list_filter = ("is_active",)


@admin.register(VariationType)
class VariationTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(VariationOption)
class VariationOptionAdmin(admin.ModelAdmin):
    list_display = ("variation_type", "name")
    list_filter = ("variation_type",)
    search_fields = ("name",)


@admin.register(IntegrationSetting)
class IntegrationSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "is_enabled")
    list_filter = ("is_enabled",)
    search_fields = ("key",)


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ("order_id", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("order_id", "customer_email")


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ("reference", "amount", "created_at")
    search_fields = ("reference",)
