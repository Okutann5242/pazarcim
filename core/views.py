from django.shortcuts import render


# -------------------- HOME --------------------
def home(request):
    featured_courses = [
        {"title": "Ürün Nasıl Listelenir?", "level": "Başlangıç", "duration": "12 dk video"},
        {"title": "Satıcı Paneli Hızlı Tur", "level": "Orta Seviye", "duration": "8 dk video"},
        {"title": "Kargo ve İade Süreçleri", "level": "Başlangıç", "duration": "10 dk video"},
    ]

    popular_products = [
        {
            "id": 1,
            "name": "Akıllı Telefon Aksesuar Seti",
            "price": "₺299",
            "badge": "Hızlı teslimat",
            "image": "img/products/t.jpg"
        },
        {
            "id": 2,
            "name": "Minimalist Defter Paketi",
            "price": "₺149",
            "badge": "Eğitimlere uygun",
            "image": "img/products/defter.jpg"
        },
        {
            "id": 3,
            "name": "Fotoğraf Arka Plan Kiti",
            "price": "₺399",
            "badge": "Yeni başlayanlar için",
            "image": "img/products/foto.jpg"
        },
        {
            "id": 4,
            "name": "Kargo Paketleme Seti",
            "price": "₺199",
            "badge": "Kargo süreçleri için önerilen",
            "image": "img/products/kargo.jpg"
        },
    ]

    return render(request, "core/home.html", {
        "featured_courses": featured_courses,
        "popular_products": popular_products
    })


# -------------------- PRODUCT LIST --------------------
def product_list(request):
    products = [
        {"id": 1, "name": "Akıllı Telefon Aksesuar Seti", "price": "₺299", "badge": "Hızlı teslimat",
         "image": "img/products/t.jpg"},
        {"id": 2, "name": "Minimalist Defter Paketi", "price": "₺149", "badge": "Eğitimlere uygun",
         "image": "img/products/defter.jpg"},
        {"id": 3, "name": "Fotoğraf Arka Plan Kiti", "price": "₺399", "badge": "Yeni başlayanlar için",
         "image": "img/products/foto.jpg"},
        {"id": 4, "name": "Kargo Paketleme Seti", "price": "₺199", "badge": "Önerilen",
         "image": "img/products/kargo.jpg"},
    ]
    return render(request, "core/product_list.html", {"products": products})


# -------------------- PRODUCT DETAIL --------------------
def product_detail(request, id):
    products = [
        {
            "id": 1,
            "name": "Akıllı Telefon Aksesuar Seti",
            "price": "₺299",
            "badge": "Hızlı teslimat",
            "image": "img/products/t.jpg",
            "desc": "Telefon aksesuarları için başlangıç seti."
        },
        {
            "id": 2,
            "name": "Minimalist Defter Paketi",
            "price": "₺149",
            "badge": "Eğitimlere uygun",
            "image": "img/products/defter.jpg",
            "desc": "Not tutma ve planlama defter paketi."
        },
        {
            "id": 3,
            "name": "Fotoğraf Arka Plan Kiti",
            "price": "₺399",
            "badge": "Yeni başlayanlar için",
            "image": "img/products/foto.jpg",
            "desc": "Ürün fotoğraf çekimi için arka plan seti."
        },
        {
            "id": 4,
            "name": "Kargo Paketleme Seti",
            "price": "₺199",
            "badge": "Kargo süreçleri için önerilen",
            "image": "img/products/kargo.jpg",
            "desc": "Satıcılar için paketleme malzeme seti."
        },
    ]

    product = next((item for item in products if item["id"] == id), None)
    return render(request, "core/product_detail.html", {"product": product})


# -------------------- EDUCATION LIST --------------------
def education_list(request):
    courses = [
        {"id": 1, "title": "Ürün Nasıl Listelenir?", "desc": "Ürün ekleme adımları."},
        {"id": 2, "title": "Satıcı Paneli Rehberi", "desc": "Panel tanıtımı."},
        {"id": 3, "title": "Kargo & İade Süreçleri", "desc": "Kargo takibi ve iade."},
    ]
    return render(request, "core/education_list.html", {"courses": courses})


# -------------------- EDUCATION DETAIL --------------------
def education_detail(request, id):
    course_data = {
        1: {"title": "Ürün Nasıl Listelenir?", "content": "Ürün listeleme adımlarının anlatımı."},
        2: {"title": "Satıcı Paneli Rehberi", "content": "Panel sekmelerinin kullanımı."},
        3: {"title": "Kargo & İade Süreçleri", "content": "İade – kargo akış adımları."},
    }

    return render(request, "core/education_detail.html", {
        "course": course_data.get(id)
    })


# -------------------- HELP CENTER --------------------
def help_center(request):
    faq_items = [
        {"question": "Pazarcım nedir?", "answer": "Shopier mantığında eğitim odaklı bir prototip."},
        {"question": "Gerçek sistem mi?", "answer": "Hayır, tamamen ödev amaçlıdır."},
        {"question": "Ürün nasıl eklenir?", "answer": "Eğitimler bölümünden öğrenebilirsiniz."},
    ]
    return render(request, "core/help_center.html", {"faq_items": faq_items})


# -------------------- CHECKOUT (SATIN ALMA SAYFASI) --------------------
def checkout(request, id):
    products = {
        1: {"name": "Akıllı Telefon Aksesuar Seti", "price": "₺299"},
        2: {"name": "Minimalist Defter Paketi", "price": "₺149"},
        3: {"name": "Fotoğraf Arka Plan Kiti", "price": "₺399"},
        4: {"name": "Kargo Paketleme Seti", "price": "₺199"},
    }

    product = products.get(id, None)

    return render(request, "core/checkout.html", {"product": product})


# -------------------- PAYMENT PAGE (Shopier tarzı) --------------------
def payment(request):
    return render(request, "core/payment.html")


# -------------------- SATICI PANELİ: BASE DASHBOARD --------------------
def dashboard(request):
    return render(request, "core/panel/dashboard.html")


# -------------------- PANEL: ÜRÜNLER --------------------
def panel_products_new(request):
    return render(request, "core/panel/product_create.html")


def panel_products_list(request):
    return render(request, "core/panel/products_list.html")


# -------------------- PANEL: SİPARİŞLER --------------------
def panel_orders(request):
    return render(request, "core/panel/orders_empty.html")


# -------------------- PANEL: TAHSİLATLAR --------------------
def panel_payouts(request):
    return render(request, "core/panel/payouts.html")


def panel_invoice(request):
    return render(request, "core/panel/invoice.html")


# -------------------- PANEL: İADELER --------------------
def panel_refund_create(request):
    return render(request, "core/panel/refund_create.html")


def panel_refunds(request):
    return render(request, "core/panel/refunds_empty.html")


# -------------------- PANEL: İNDİRİMLER --------------------
def panel_discounts(request):
    return render(request, "core/panel/discounts.html")


# -------------------- PANEL: DÜKKAN AYARLARI --------------------
def panel_store_settings(request):
    return render(request, "core/panel/store_settings.html")


def panel_store_logo(request):
    return render(request, "core/panel/store_logo.html")


def panel_category_settings(request):
    return render(request, "core/panel/category_settings.html")


def panel_variation_settings(request):
    return render(request, "core/panel/variation_settings.html")


def panel_courier_settings(request):
    return render(request, "core/panel/courier_settings.html")


# -------------------- PANEL: ENTEGRASYONLAR --------------------
def panel_apps(request):
    return render(request, "core/panel/apps.html")


def panel_osb(request):
    return render(request, "core/panel/osb.html")


# -------------------- PANEL: HESAP --------------------
def panel_account_security(request):
    return render(request, "core/panel/account_security.html")


def panel_account_users(request):
    return render(request, "core/panel/account_users.html")
