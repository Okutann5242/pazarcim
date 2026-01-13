from django import forms

from .models import (
    DiscountCode,
    IntegrationSetting,
    RefundRequest,
    ShippingMethod,
    StoreProfile,
    VariationOption,
    VariationType,
)

INPUT = {"class": "input"}


class StoreProfileForm(forms.ModelForm):
    class Meta:
        model = StoreProfile
        fields = ["store_name", "description", "support_email", "support_phone"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "input", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            if isinstance(f.widget, forms.widgets.Textarea):
                continue
            f.widget.attrs.update(INPUT)


class StoreMediaForm(forms.ModelForm):
    class Meta:
        model = StoreProfile
        fields = ["logo", "banner"]


class DiscountForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = ["code", "percent", "is_active", "starts_at", "ends_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update(INPUT)


class ShippingMethodForm(forms.ModelForm):
    class Meta:
        model = ShippingMethod
        fields = ["name", "flat_fee", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update(INPUT)


class VariationTypeForm(forms.ModelForm):
    class Meta:
        model = VariationType
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update(INPUT)


class VariationOptionForm(forms.ModelForm):
    class Meta:
        model = VariationOption
        fields = ["variation_type", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update(INPUT)


class IntegrationSettingForm(forms.ModelForm):
    class Meta:
        model = IntegrationSetting
        fields = ["key", "value", "is_enabled"]
        widgets = {"value": forms.Textarea(attrs={"class": "input", "rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            if isinstance(f.widget, forms.widgets.Textarea):
                continue
            f.widget.attrs.update(INPUT)


class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        fields = ["order_id", "customer_email", "reason", "status"]
        widgets = {"reason": forms.Textarea(attrs={"class": "input", "rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            if isinstance(f.widget, forms.widgets.Textarea):
                continue
            f.widget.attrs.update(INPUT)
