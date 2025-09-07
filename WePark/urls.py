"""
URL configuration for WePark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from app import views
from WePark import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
#-----------------------------account urls--------------------------------------
    path('account/login',views.login,name="login"),
    #use django authentication for all login views in the urls/learn so that i can have login algorithm
    path('account/create-account',views.create_account,name="create_account"),
    # remember settings edits to do with email
    path('account/forgot-password',auth_views.PasswordResetView.as_view(template_name="accounts/forgot password.html"),name="forgot_password"),
    path('account/reset-password',auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset password message.html"),name="password_reset_done"),
    path('accounts/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset password"),name="password_reset_confirm"),
    path('accounts/reset-password-complete',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset password complete.html"),name="password_reset_complete"),
#-----------------------------parking urls--------------------------------------
    path('parking/rent-out-parking-space',views.rent_out_parking_space,name="rent_out_parking_spaces"),
    path('parking/upload-parking-space',views.upload_parking_space,name="upload_parking_space"),
    path('parking/update-parking-space/<int:pk>',views.update_parking_space,name="update_parking_space"),
    path('parking/manage-parking-spaces',views.manage_parking_spaces,name="manage_parking_spaces"),
    path('parking/delete-managed-parking-space/<int:pk>',views.delete_managed_parking_space,name="delete_managed_parking_space"),
    path('parking/bookmarked-parking',views.bookmarked_parking,name="bookmarked_parking"),
    path('parking/remove-bookmarked-parking-space/<int:pk>',views.remove_bookmarked_parking_space,name="remove_bookmarked_parking_space"),
    path('parking/top-rated-spaces',views.top_rated_spaces,name="top_rated_spaces"),
    path('parking-search/',views.search_parking_spaces,name='search_parking_spaces'),
    path('parking/space/<str:name>/<int:pk>',views.parking_space_information,name='parking_space_information')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# add parking functionality screens