from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name= "home"),
    path('<str:ref_by>', views.home, name= "home"),
    path('search/', views.search, name= "search"),
    path('search/<str:ref_by>', views.search, name= "search"),
    path('info/<int:pk>/<str:ref_by>', views.info, name= "info"),
    path('info/<int:pk>/', views.info, name= "info"),
    path('add-product/', views.AddProduct.as_view(), name= "add-product"),
    path('edit-product/<int:pk>', views.EditProduct.as_view(), name= "edit-product"),
    path('delete-product/<int:pk>', views.DelProduct.as_view(), name= "delete-product"),
    path('info/<int:pk>/offer-info/<int:pk2>', views.offer_info, name= "offer-info"),
    path('add-offer/', views.AddOffer.as_view(), name= "add-offer"),
    path('edit-offer/<int:pk>', views.EditOffer.as_view(), name= "edit-offer"),
    path('delete-offer/<int:pk>', views.DelOffer.as_view(), name= "delete-offer"),
    path('profile/', views.profile, name= "profile"),
    path('profile-edit/<int:pk>', views.ProfileEdit.as_view(), name= "profile-edit"),
    path('paystack-keys/', views.paystack_keys, name= "paystack-keys"),
    path('add-pk/', views.AddPK.as_view(), name= "add-pk"),
    path('edit-pk/<int:pk>', views.EditPK.as_view(), name= "edit-pk"),
    path('add-bank/', views.add_bank, name= "add-bank" ),
    path('edit-bank/<int:pk>', views.EditBank.as_view(), name= "edit-bank"),
    path('delete-bank/<int:pk>', views.DeleteBank.as_view(), name= "delete-bank"),
    path('bank-details/', views.bank_details_upload, name= "bank-details"),
    path('bank-edit/<int:pk>', views.BankEdit.as_view(), name= "bank-edit"),
    path('bank-delete/<int:pk>', views.BankDelete.as_view(), name= "bank-delete"),
    path('withdraw/<int:pk>', views.withdraw, name= "withdraw"),
    path('withdraw-history/', views.withdrawal_history, name= "withdraw-history"),
    path('add-cat/', views.AddCat.as_view(), name= "add-cat"),
    path('edit-cat/', views.EditCat.as_view(), name= "edit-cat"),
    path('delete-cat/', views.DelCat.as_view(), name= "delete-cat"),
    path('trans-hist/', views.transaction_history, name="trans-hist"),
    path('init-payment/<int:pk>', views.initialize_payment, name= "init-payment"),
    path('verify-payment/<str:ref>', views.verify_payment, name= "verify-payment"),
    path('contact/', views.contact, name= "contact"),
    path('add-contact/', views.AddContact.as_view(), name= "add-contact"),
    path('edit-contact/<int:pk>', views.EditContact.as_view(), name="edit-contact"),
    path('email/', views.email_notifications, name= "email")
]