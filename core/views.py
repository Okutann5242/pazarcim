from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from checkout.models import Order
from products.forms import ProductForm
from products.models import Category, Product, ProductVariationOption, ProductVariationType

from accounts.models import UserProfile

from .forms import (
    DiscountForm,
    RefundRequestForm,
    ShippingMethodForm,
    StoreMediaForm,
    StoreProfileForm,
    VariationOptionForm,
    VariationTypeForm,
)
from .models import DiscountCode, Payout, RefundRequest, ShippingMethod, StoreProfile, VariationOption, VariationType


def is_seller(user):
    # Satıcı paneli erişim kuralı:
    # - Django admin/staff kullanıcıları
    # - veya accounts.UserProfile.role == seller
    if not user.is_authenticated:
        return False
    if getattr(user, "is_staff", False):
        return True
    profile = getattr(user, "profile", None)
    return bool(profile and profile.role == UserProfile.Role.SELLER)


seller_required = user_passes_test(is_seller, login_url="accounts:login")


def _sync_product_variations(product: Product, request):
    type_ids = [int(x) for x in request.POST.getlist("variation_type_ids") if str(x).isdigit()]
    ProductVariationType.objects.filter(product=product).exclude(variation_type_id__in=type_ids).delete()
    for tid in type_ids:
        ProductVariationType.objects.get_or_create(product=product, variation_type_id=tid)

    option_ids = [int(x) for x in request.POST.getlist("variation_option_ids") if str(x).isdigit()]
    ProductVariationOption.objects.filter(product=product).exclude(option_id__in=option_ids).delete()
    for oid in option_ids:
        raw = (request.POST.get(f"extra_price_{oid}") or "0").replace(",", ".")
        try:
            extra = float(raw)
        except Exception:
            extra = 0
        obj, _ = ProductVariationOption.objects.get_or_create(product=product, option_id=oid)
        obj.extra_price = extra
        obj.save(update_fields=["extra_price"])


# -------------------- HOME --------------------

def home(request):
    popular_products = Product.objects.filter(is_active=True).order_by("-created_at")[:4]
    stats = {
        "active_sellers": StoreProfile.objects.count(),
        "active_products": Product.objects.filter(is_active=True).count(),
        "total_orders": Order.objects.count(),
    }
    return render(request, "core/home.html", {"popular_products": popular_products, "stats": stats})


# -------------------- PUBLIC STORE FRONT --------------------
def store_front(request, slug: str):
    store = get_object_or_404(StoreProfile, slug=slug)
    qs = Product.objects.filter(is_active=True, seller=store.owner).select_related("category").order_by("-created_at")
    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(name__icontains=q)
    return render(request, "core/store_front.html", {"store": store, "products": qs, "q": q})


def store_product_detail(request, store_slug: str, product_slug: str):
    store = get_object_or_404(StoreProfile, slug=store_slug)
    product = get_object_or_404(Product, seller=store.owner, slug=product_slug, is_active=True)
    from products.models import ProductVariationType, ProductVariationOption
    return render(
        request,
        "products/detail.html",
        {
            "item": product,
            "store": store,
            "from_storefront": True,
            "variation_types": ProductVariationType.objects.filter(product=product).select_related("variation_type"),
            "variation_options": ProductVariationOption.objects.filter(product=product).select_related("option", "option__variation_type"),
        },
    )


# -------------------- HELP CENTER --------------------
def help_center(request):
    faq_items = [
        {"question": "Site nasıl çalışır?", "answer": "Katalogtan ürün seçip sepete ekleyebilir, ödeme akışını tamamlayabilirsiniz."},
        {"question": "Satıcı paneli kimler için?", "answer": "Personel (is_staff) kullanıcılar için yönetim panelidir."},
        {"question": "Eğitimler nerede?", "answer": "Eğitimler menüsünden PDF kütüphanesine erişebilirsiniz."},
    ]
    return render(request, "core/help_center.html", {"faq_items": faq_items})


# -------------------- SELLER PANEL: DASHBOARD --------------------
@seller_required
def dashboard(request):
    seller_products = Product.objects.filter(seller=request.user)
    orders_qs = Order.objects.filter(items__product__seller=request.user).distinct().select_related("address")

    store = StoreProfile.objects.filter(owner=request.user).first()

    stats = {
        "products": seller_products.count(),
        "orders": orders_qs.count(),
        "refunds": RefundRequest.objects.filter(
    order_id__in=orders_qs.values_list("id", flat=True)
).count(),

        "revenue_30d": 0,
    }

    from django.utils import timezone
    today = timezone.localdate()
    start = today - timezone.timedelta(days=29)

    daily_sales = []
    for i in range(30):
        d = start + timezone.timedelta(days=i)
        total = (
            orders_qs.filter(created_at__date=d)
            .exclude(status=Order.Status.CANCELED)
            .aggregate(models.Sum("total_amount"))["total_amount__sum"]
            or 0
        )
        daily_sales.append({"date": d.strftime("%d.%m"), "total": float(total)})

    # 30 günlük ciro
    stats["revenue_30d"] = float(sum([x["total"] for x in daily_sales]))

    recent_orders = orders_qs.order_by("-created_at")[:10]

    onboarding = {
        "has_store": bool(store),
        "has_logo": bool(store and store.logo),
        "has_banner": bool(store and store.banner),
        "has_product": seller_products.exists(),
    }

    status_counts = {key: orders_qs.filter(status=key).count() for key, _ in Order.Status.choices}

    return render(
        request,
        "core/panel/dashboard.html",
        {
            "stats": stats,
            "daily_sales": daily_sales,
            "status_counts": status_counts,
            "recent_orders": recent_orders,
            "store": store,
            "onboarding": onboarding,
        },
    )


# -------------------- PANEL: PRODUCTS --------------------
@seller_required
def panel_products_list(request):
    qs = Product.objects.filter(seller=request.user).order_by("-created_at")

    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(name__icontains=q)

    category_id = request.GET.get("category") or ""
    if category_id.isdigit():
        qs = qs.filter(category_id=int(category_id))

    active = request.GET.get("active")
    if active in ("0", "1"):
        qs = qs.filter(is_active=(active == "1"))

    from django.core.paginator import Paginator
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    categories = Category.objects.order_by("name")
    return render(
        request,
        "core/panel/products_list.html",
        {"products": page_obj, "page_obj": page_obj, "categories": categories, "filters": {"q": q, "category": category_id, "active": active}},
    )


@seller_required
def panel_products_new(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.seller = request.user
        obj.save()

        _sync_product_variations(obj, request)

        messages.success(request, "Ürün oluşturuldu.")
        return redirect("core:panel_products_list")

    return render(
        request,
        "core/panel/product_create.html",
        {
            "form": form,
            "mode": "create",
            "variation_types": VariationType.objects.order_by("name").prefetch_related("options"),
            "selected_type_ids": [],
            "selected_option_map": {},
        },
    )


@seller_required
def panel_products_edit(request, pk: int):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        obj = form.save()
        _sync_product_variations(obj, request)
        messages.success(request, "Ürün güncellendi.")
        return redirect("core:panel_products_list")

    selected_type_ids = list(ProductVariationType.objects.filter(product=product).values_list("variation_type_id", flat=True))
    selected_option_map = {p.option_id: str(p.extra_price) for p in ProductVariationOption.objects.filter(product=product)}

    return render(
        request,
        "core/panel/product_create.html",
        {
            "form": form,
            "mode": "edit",
            "product": product,
            "variation_types": VariationType.objects.order_by("name").prefetch_related("options"),
            "selected_type_ids": selected_type_ids,
            "selected_option_map": selected_option_map,
        },
    )


@seller_required
def panel_products_delete(request, pk: int):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Ürün silindi.")
        return redirect("core:panel_products_list")
    return render(request, "core/panel/product_delete_confirm.html", {"product": product})


# -------------------- PANEL: ORDERS --------------------
@seller_required
def panel_orders(request):
    orders = Order.objects.select_related("user", "address").prefetch_related("items", "items__product").order_by("-created_at")
    return render(request, "core/panel/orders_list.html", {"orders": orders})


@seller_required
def panel_order_detail(request, order_id: int):
    order = get_object_or_404(Order.objects.select_related("user", "address").prefetch_related("items", "items__product"), pk=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in {c[0] for c in Order.Status.choices}:
            order.status = new_status
            order.save(update_fields=["status"])
            messages.success(request, "Sipariş durumu güncellendi.")
            return redirect("core:panel_order_detail", order_id=order.id)
    return render(request, "core/panel/order_detail.html", {"order": order, "status_choices": Order.Status.choices})


# -------------------- PANEL: PAYOUTS --------------------
@seller_required
def panel_payouts(request):
    payouts = Payout.objects.all()
    return render(request, "core/panel/payouts.html", {"payouts": payouts})


@seller_required
def panel_invoice(request):
    return render(request, "core/panel/invoice.html")


# -------------------- PANEL: REFUNDS --------------------
@seller_required
def panel_refunds(request):
    refunds = RefundRequest.objects.all()
    return render(request, "core/panel/refunds_list.html", {"refunds": refunds})


@seller_required
def panel_refund_create(request):
    form = RefundRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "İade talebi oluşturuldu.")
        return redirect("core:panel_refunds")
    return render(request, "core/panel/refund_create.html", {"form": form})


# -------------------- PANEL: DISCOUNTS --------------------
@seller_required
def panel_discounts(request):
    discounts = DiscountCode.objects.order_by("-id")
    form = DiscountForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "İndirim kodu oluşturuldu.")
        return redirect("core:panel_discounts")
    return render(request, "core/panel/discounts.html", {"discounts": discounts, "form": form})


@seller_required
def panel_discount_delete(request, pk: int):
    obj = get_object_or_404(DiscountCode, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "İndirim kodu silindi.")
        return redirect("core:panel_discounts")
    return render(request, "core/panel/discount_delete_confirm.html", {"discount": obj})


# -------------------- PANEL: STORE SETTINGS --------------------
def _get_store_profile(user):
    profile, _ = StoreProfile.objects.get_or_create(owner=user)
    return profile


@seller_required
def panel_store_settings(request):
    profile = _get_store_profile(request.user)
    form = StoreProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Dükkan ayarları güncellendi.")
        return redirect("core:panel_store_settings")
    return render(request, "core/panel/store_settings.html", {"form": form, "profile": profile})


@seller_required
def panel_store_logo(request):
    profile = _get_store_profile(request.user)
    form = StoreMediaForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Logo / banner güncellendi.")
        return redirect("core:panel_store_logo")
    return render(request, "core/panel/store_logo.html", {"form": form, "profile": profile})


# -------------------- PANEL: CATEGORY SETTINGS --------------------
@seller_required
def panel_category_settings(request):
    categories = Category.objects.order_by("name")
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        if name:
            slug = (request.POST.get("slug") or "").strip()
            if not slug:
                from django.utils.text import slugify
                slug = slugify(name)
            Category.objects.create(name=name, slug=slug)
            messages.success(request, "Kategori eklendi.")
            return redirect("core:panel_category_settings")
    return render(request, "core/panel/category_settings.html", {"categories": categories})


@seller_required
def panel_category_delete(request, pk: int):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        cat.delete()
        messages.success(request, "Kategori silindi.")
        return redirect("core:panel_category_settings")
    return render(request, "core/panel/category_delete_confirm.html", {"category": cat})


# -------------------- PANEL: VARIATIONS --------------------
@seller_required
def panel_variation_settings(request):
    types = VariationType.objects.order_by("name")
    options = VariationOption.objects.select_related("variation_type").order_by("variation_type__name", "name")
    type_form = VariationTypeForm(request.POST or None, prefix="t")
    option_form = VariationOptionForm(request.POST or None, prefix="o")
    if request.method == "POST":
        if "create_type" in request.POST and type_form.is_valid():
            type_form.save()
            messages.success(request, "Varyasyon tipi eklendi.")
            return redirect("core:panel_variation_settings")
        if "create_option" in request.POST and option_form.is_valid():
            option_form.save()
            messages.success(request, "Varyasyon seçeneği eklendi.")
            return redirect("core:panel_variation_settings")
    return render(
        request,
        "core/panel/variation_settings.html",
        {"types": types, "options": options, "type_form": type_form, "option_form": option_form},
    )


@seller_required
def panel_variation_type_delete(request, pk: int):
    obj = get_object_or_404(VariationType, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Varyasyon tipi silindi.")
        return redirect("core:panel_variation_settings")
    return render(request, "core/panel/variation_type_delete_confirm.html", {"obj": obj})


@seller_required
def panel_variation_option_delete(request, pk: int):
    obj = get_object_or_404(VariationOption, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Varyasyon seçeneği silindi.")
        return redirect("core:panel_variation_settings")
    return render(request, "core/panel/variation_option_delete_confirm.html", {"obj": obj})


# -------------------- PANEL: COURIER SETTINGS --------------------
@seller_required
def panel_courier_settings(request):
    methods = ShippingMethod.objects.order_by("name")
    form = ShippingMethodForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Kargo yöntemi eklendi.")
        return redirect("core:panel_courier_settings")
    return render(request, "core/panel/courier_settings.html", {"methods": methods, "form": form})


@seller_required
def panel_courier_delete(request, pk: int):
    obj = get_object_or_404(ShippingMethod, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Kargo yöntemi silindi.")
        return redirect("core:panel_courier_settings")
    return render(request, "core/panel/courier_delete_confirm.html", {"obj": obj})


# -------------------- PANEL: INTEGRATIONS --------------------
@seller_required
def panel_apps(request):
    # Basit bir placeholder: gerçek entegrasyon için IntegrationSetting kullanılabilir.
    return render(request, "core/panel/apps.html")


@seller_required
def panel_osb(request):
    return render(request, "core/panel/osb.html")


# -------------------- PANEL: ACCOUNT --------------------
@seller_required
def panel_account_security(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Şifreniz güncellendi. Tekrar giriş yapmanız gerekebilir.")
        return redirect("core:panel_account_security")
    return render(request, "core/panel/account_security.html", {"form": form})


@seller_required
def panel_account_users(request):
    return render(request, "core/panel/account_users.html")
# TEST COMMIT - Ahmetcan core app
