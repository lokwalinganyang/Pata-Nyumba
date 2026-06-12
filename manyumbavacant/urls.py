from django.urls import path
from . import views

app_name = 'manyumbavacant'
urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('search/', views.search_properties, name='search'),
    path('locations/', views.browse_by_location, name='browse_locations'),
    
    # Landlord Authentication (new)
    path('landlord/register/', views.landlord_register, name='landlord_register'),
    path('landlord/login/', views.landlord_login, name='landlord_login'),
    path('landlord/logout/', views.landlord_logout, name='landlord_logout'),
    
    # Legacy session‑based registration (optional – keep for existing links)
    path('landlord/start/', views.landlord_start, name='landlord_start'),
    
    # Property management
    path('landlord/add/', views.add_property, name='add_property'),
    path('landlord/thanks/<int:prop_id>/', views.property_thanks, name='property_thanks'),
    
    # Dashboard & property editing
    path('dashboard/', views.landlord_dashboard, name='landlord_dashboard'),
    path('dashboard/property/<int:property_id>/edit/', views.landlord_edit_property, name='landlord_edit_property'),
    path('dashboard/property/<int:property_id>/toggle/', views.landlord_toggle_active, name='landlord_toggle_active'),
    path('dashboard/property/<int:property_id>/delete/', views.landlord_delete_property, name='landlord_delete_property'),
    
    # Property details & reports
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/<int:pk>/report/', views.report_property, name='report_property'),
    
    # Ad clicks
    path('ad/<int:ad_id>/click/', views.ad_click, name='ad_click'),
]