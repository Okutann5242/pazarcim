from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # Vitrin / eğitim / ürünler
    path("", views.home, name="home"),

    path("egitimler/", views.education_list, name="education_list"),
    path("egitim/<int:id>/", views.education_detail, name="education_detail"),

    path("urunler/", views.product_list, name="product_list"),
    path("urun/<int:id>/", views.product_detail, name="product_detail"),

    path("satinal/<int:id>/", views.checkout, name="checkout"),
    path("odeme/", views.payment, name="payment"),

    path("yardim/", views.help_center, name="help_center"),

    # --------- SATICI PANELİ ----------
    path("panel/", views.dashboard, name="dashboard"),

    # Ürünler
    path("panel/urun/yeni/", views.panel_products_new, name="panel_products_new"),
    path("panel/urunler/", views.panel_products_list, name="panel_products_list"),

    # Siparişler
    path("panel/siparisler/", views.panel_orders, name="panel_orders"),

    # Tahsilatlar
    path("panel/tahsilatlar/", views.panel_payouts, name="panel_payouts"),
    path("panel/tahsilatlar/fatura/", views.panel_invoice, name="panel_invoice"),

    # İadeler
    path("panel/iadeler/olustur/", views.panel_refund_create, name="panel_refund_create"),
    path("panel/iadeler/", views.panel_refunds, name="panel_refunds"),

    # İndirimler
    path("panel/indirimler/", views.panel_discounts, name="panel_discounts"),

    # Dükkan
    path("panel/dukkan/ayarlar/", views.panel_store_settings, name="panel_store_settings"),
    path("panel/dukkan/logo-banner/", views.panel_store_logo, name="panel_store_logo"),
    path("panel/dukkan/kategoriler/", views.panel_category_settings, name="panel_category_settings"),
    path("panel/dukkan/varyasyonlar/", views.panel_variation_settings, name="panel_variation_settings"),
    path("panel/dukkan/kargo/", views.panel_courier_settings, name="panel_courier_settings"),

    # Entegrasyonlar
    path("panel/entegrasyonlar/uygulamalar/", views.panel_apps, name="panel_apps"),
    path("panel/entegrasyonlar/osb/", views.panel_osb, name="panel_osb"),

    # Hesap
    path("panel/hesap/guvenlik/", views.panel_account_security, name="panel_account_security"),
    path("panel/hesap/kullanicilar/", views.panel_account_users, name="panel_account_users"),
]
