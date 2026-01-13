from django.conf import settings
from django.db import models


class StoreProfile(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="store_profile")
    store_name = models.CharField(max_length=150, default="Mağazam")
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField(blank=True)
    support_email = models.EmailField(blank=True)
    support_phone = models.CharField(max_length=40, blank=True)
    logo = models.ImageField(upload_to="store/logo/", blank=True, null=True)
    banner = models.ImageField(upload_to="store/banner/", blank=True, null=True)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            base = slugify(self.store_name) or f"magaza-{self.owner_id}"
            slug = base
            n = 1
            while StoreProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Dükkan Profili"
        verbose_name_plural = "Dükkan Profilleri"

    def __str__(self) -> str:
        return f"{self.store_name} (owner={self.owner_id})"


class DiscountCode(models.Model):
    code = models.CharField(max_length=40, unique=True)
    percent = models.PositiveIntegerField(help_text="0-100 arası indirim yüzdesi")
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.code


class ShippingMethod(models.Model):
    name = models.CharField(max_length=120)
    flat_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class VariationType(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self) -> str:
        return self.name


class VariationOption(models.Model):
    variation_type = models.ForeignKey(VariationType, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=60)

    class Meta:
        unique_together = ("variation_type", "name")

    def __str__(self) -> str:
        return f"{self.variation_type}: {self.name}"


class IntegrationSetting(models.Model):
    key = models.CharField(max_length=80, unique=True)
    value = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.key


class RefundRequest(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Açık"
        APPROVED = "approved", "Onaylandı"
        REJECTED = "rejected", "Reddedildi"
        CLOSED = "closed", "Kapandı"

    order_id = models.PositiveIntegerField()
    customer_email = models.EmailField(blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Refund(order={self.order_id}, status={self.status})"


class Payout(models.Model):
    reference = models.CharField(max_length=120, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.reference
