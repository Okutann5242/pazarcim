from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("yardim/", views.help_center, name="help_center"),
    path("magaza/<slug:slug>/", views.store_front, name="store_front"),
    path("magaza/<slug:store_slug>/urun/<slug:product_slug>/", views.store_product_detail, name="store_product_detail"),

    # --------- SATICI PANELİ ----------
    path("panel/", views.dashboard, name="dashboard"),

    # Ürünler
    path("panel/urunler/", views.panel_products_list, name="panel_products_list"),
    path("panel/urun/yeni/", views.panel_products_new, name="panel_products_new"),
    path("panel/urun/<int:pk>/duzenle/", views.panel_products_edit, name="panel_products_edit"),
    path("panel/urun/<int:pk>/sil/", views.panel_products_delete, name="panel_products_delete"),

    # Siparişler
    path("panel/siparisler/", views.panel_orders, name="panel_orders"),
    path("panel/siparis/<int:order_id>/", views.panel_order_detail, name="panel_order_detail"),

    # Tahsilatlar
    path("panel/tahsilatlar/", views.panel_payouts, name="panel_payouts"),
    path("panel/tahsilatlar/fatura/", views.panel_invoice, name="panel_invoice"),

    # İadeler
    path("panel/iadeler/olustur/", views.panel_refund_create, name="panel_refund_create"),
    path("panel/iadeler/", views.panel_refunds, name="panel_refunds"),

    # İndirimler
    path("panel/indirimler/", views.panel_discounts, name="panel_discounts"),
    path("panel/indirim/<int:pk>/sil/", views.panel_discount_delete, name="panel_discount_delete"),

    # Dükkan
    path("panel/dukkan/ayarlar/", views.panel_store_settings, name="panel_store_settings"),
    path("panel/dukkan/logo-banner/", views.panel_store_logo, name="panel_store_logo"),
    path("panel/dukkan/kategoriler/", views.panel_category_settings, name="panel_category_settings"),
    path("panel/dukkan/kategori/<int:pk>/sil/", views.panel_category_delete, name="panel_category_delete"),
    path("panel/dukkan/varyasyonlar/", views.panel_variation_settings, name="panel_variation_settings"),
    path("panel/dukkan/varyasyon-tipi/<int:pk>/sil/", views.panel_variation_type_delete, name="panel_variation_type_delete"),
    path("panel/dukkan/varyasyon-secenegi/<int:pk>/sil/", views.panel_variation_option_delete, name="panel_variation_option_delete"),
    path("panel/dukkan/kargo/", views.panel_courier_settings, name="panel_courier_settings"),
    path("panel/dukkan/kargo/<int:pk>/sil/", views.panel_courier_delete, name="panel_courier_delete"),

    # Entegrasyonlar
    path("panel/entegrasyonlar/uygulamalar/", views.panel_apps, name="panel_apps"),
    path("panel/entegrasyonlar/osb/", views.panel_osb, name="panel_osb"),

    # Hesap
    path("panel/hesap/guvenlik/", views.panel_account_security, name="panel_account_security"),
    path("panel/hesap/kullanicilar/", views.panel_account_users, name="panel_account_users"),
]
