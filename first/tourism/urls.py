from django.contrib import admin
from django.urls import path
from tourism import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main pages
    path('', views.home_page, name='home_page'),
    path('register/', views.register_page, name='register_page'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),
    path('galary/', views.galary_page, name='galary_page'),
    path('tourist/', views.tourist_page, name='tourist_page'),
    path('card/<int:city_id>/', views.card_page, name='card_page'),
    path('hostel/<int:city_id>/', views.hostel_view, name='hostel_view'),
    path('hostel/', views.hostel_page, name='hostel_page'),
    path('islamabad/', views.islamabad_page, name='islamabad_page'),
    path('lahore/', views.lahore_page, name='lahore_page'),
    path('booking/<int:hotel_id>/', views.booking_page, name='booking_page'),
    path('pay', views.initiate_payment, name='initiate_payment'),
    path('stripe/success/', views.stripe_success, name='stripe_success'),
    path('stripe/cancel/', views.stripe_cancel, name='stripe_cancel'),
    path('receipt/<int:payment_id>/', views.payment_receipt, name='payment_receipt'),
    path('booking/cart/', views.booking_cart_page, name='booking_cart_page'),
    path('booking/delete/<int:booking_id>/', views.delete_page, name='delete_page'),
    path('receipt/download/<str:trx_id>/',views.download_receipt, name='download_receipt'),
    path('receipt-preview/<str:trx_id>/', views.receipt_preview, name='receipt_preview'),
    path('dashboard/transactions/', views.admin_transactions, name='admin_transactions'),
    path('payment/card-session/', views.start_card_payment, name='start_card_payment'),
     path('karachi/', views.karachi_page, name='karachi_page'),
    path('peshawar/', views.peshawar_page, name='peshawar_page'),
    path('quetta/', views.quetta_page, name='quetta_page'),
    path('gilgit/', views.gilgit_page, name='gilgit_page'),
    path('skardu/', views.skardu_page, name='skardu_page'),
    path('hunza/', views.hunza_page, name='hunza_page'),
    path('murree/', views.murree_page, name='murree_page'),
    path('swat/', views.swat_page, name='swat_page'),
    path('multan/', views.multan_page, name='multan_page'),
    path('bahawalpur/', views.bahawalpur_page, name='bahawalpur_page'),
    path('kashmir/', views.kashmir_page, name='kashmir_page'),
    path('naran/', views.naran_page, name='naran_page'),
    path('kaghan/', views.kaghan_page, name='kaghan_page'),
    path('shigar/', views.shigar_page, name='shigar_page'),
    path('chatgpt/', views.chatbot_page, name='chatbot_page'),
    path('chatbot-api/', views.chatbot_api, name='chatbot_api'),
    path("chat/", views.chat_list, name="chat_list"),
    path("chat/<int:user_id>/", views.chat_page, name="chat_page"),
    path("chat/send/", views.send_message, name="send_message"),
    path("message/<int:pk>/edit/", views.edit_message, name="edit_message"),
    path("message/<int:pk>/delete/", views.delete_message, name="delete_message"),
    path("chat/<int:receiver_id>/fetch/", views.fetch_messages, name="fetch_messages"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
