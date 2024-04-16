from django.contrib import admin
from django.urls import path
from.import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from .views import booking_page, confirm_and_pay
from .views import paymenthandler
from .views import manage_guide_approvals
from .views import add_service, view_services,service_details,delete_service,edit_service_details,view_guides,delete_guide,guest_service_display
from staydemoapp import candy
 
urlpatterns = [
    *candy.path('',views.index,name="home"),
    *candy.path('login/',views.login,name="login"),
    *candy.path('registration/',views.registration,name="registration"),
    *candy.path('registerproperty/',views.registerproperty,name="registerproperty"),
    *candy.path('guide_registration/',views.guide_registration,name="guide_registration"),

    
    path('host_dashboard/',views.host_dashboard,name="host_dashboard"),
    path('guest_dashboard/',views.guest_dashboard,name="guest_dashboard"),
    path('guide_dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('logout/',views.logout,name="logout"),
    # path('services/', views.services, name='services'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('view_hosts/', views.view_hosts, name='view_hosts'),
    path('view_guests/', views.view_guests, name='view_guests'),
    path('delete_guest/<int:guest_id>/', views.delete_guest, name='delete_guest'),
    path('delete_host/<int:host_id>/', views.delete_host, name='delete_host'),
    path('delete_guide/<int:guide_id>/', delete_guide, name='delete_guide'),

    path('edit-host-profile/', views.edit_host_profile, name='edit_host_profile'),
    path('edit-guest-profile/', views.edit_guest_profile, name='edit_guest_profile'),
    path('host/profile/', views.host_profile, name='host_profile'),
    path('guest_profile/', views.guest_profile, name='guest_profile'),
    path('edit_guide_profile/', views.edit_guide_profile, name='edit_guide_profile'),
    path('view_guide_profile/', views.view_guide_profile, name='view_guide_profile'),

    path('add_property/', views.add_property, name='add_property'),
    path('view_property/<int:property_id>/', views.view_property, name='view_property'),
    path('edit_property/<int:property_id>/', views.edit_property, name='edit_property'),

    path('manage_host_approvals/', views.manage_host_approvals, name='manage_host_approvals'),    
    path('manage_guide_approvals/', views.manage_guide_approvals, name='manage_guide_approvals'),
    

    path('add_service/', add_service, name='add_service'),
    path('view_services/', view_services, name='view_services'),
    path('service_details/<path:service_id>/', service_details, name='service_details'),
    path('delete_service/', delete_service, name='delete_service'),
    path('edit_service/<str:service_id>/', edit_service_details, name='edit_service_details'),
    path('guide_display/', views.guide_display, name='guide_display'),
    path('view_guides/', view_guides, name='view_guides'),
    path('guest_service_display/<int:guide_id>/', guest_service_display, name='guest_service_display'),

    path('guest_service_view/<path:service_id>/', views.guest_service_view, name='guest_service_view'),
    path('get_user_reviews/', views.get_user_reviews, name='get_user_reviews'),
    
    path('service_booking/<str:service_id>/', views.service_booking, name='service_booking'),

    path('booking_status/<str:booking_id>/', views.booking_status, name='booking_status'),
    path('view_servicebookings/', views.view_servicebookings, name='view_servicebookings'),
    path('guide_service_booking/', views.guide_service_booking, name='guide_service_booking'),
    path('viewmyservices/', views.viewmyservices, name='viewmyservices'),
    path('add_review/<int:service_id>/', views.add_review, name='add_review'),

    path('add_availability/<int:property_id>/', views.add_availability, name='add_availability'),

    path('property/<int:property_id>/', views.guest_property_details, name='guest_property_details'),
    path('payment_success/<int:booking_id>/', views.payment_success, name='payment_success'),


    path('search/', views.search_properties, name='search_properties'),
    
    path('add_to_wishlist/<int:property_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('remove_from_wishlist/<int:property_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('book/<int:property_id>/', views.booking_page, name='booking_page'),

    path('property/<int:property_id>/book/', booking_page, name='booking_page'),
    
    path('confirm_and_pay/<int:property_id>/', views.confirm_and_pay, name='confirm_and_pay'),
    #path('make_payment/', make_payment, name='make_payment'),
    path('confirm_and_pay/<int:property_id>/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('booking_updates/', views.booking_updates, name='booking_updates'),
    path('activate_property/<int:property_id>/', views.activate_property, name='activate_property'),
    path('deactivate_property/<int:property_id>/', views.deactivate_property, name='deactivate_property'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    
]


