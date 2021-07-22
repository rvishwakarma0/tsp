from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.index, name="TiffinServicePool"),
    path('checkout/',views.checkout, name="checkout"),
    path('cart/',views.cart, name="cart"),
    path('update_item/',views.UpdateItem, name="update_item"),
    path('process_order/',views.ProcessOrder, name="process_order"),
    path('user_logout/',views.userLogout, name = "user_logout"),
    path('login_register/', views.loginOrRegister,name="login_register"),
    #path('tiffin/<int:tid>', views.tiffin, name="tiffin"),
    #path('vendor/<int:vid>/', views.vendor, name="vendor"),
    path('my_orders/', views.myOrders, name="myOrders"),
    path('my_orders/<int:id>/', views.my_order_details, name="my_order_details"),
    path('my_account/', views.my_account, name="my_account"),
    path('cancel_order/<int:oid>/', views.cancel_order, name="cancel_order"),

    path('rating/<str:vot>/<int:id>/', views.rating, name="rating"),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

]
