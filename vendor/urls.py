from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('dashboard/<int:vid>/',views.dashboard, name="TiffinServicePool"),
    path('<int:vid>/', views.vendor, name="vendor"),
    path('deliver_order/<int:oid>/<int:vid>/', views.deliver, name="deliver_order"),
    path('cancel_order/<int:oid>/<int:vid>/', views.cancel_order, name="cancel_order"),
]
