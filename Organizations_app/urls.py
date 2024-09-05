from django.urls import path
from .import views

urlpatterns = [
    path('',views.sign_up,name="sign_up"),
    path('sign_in/',views.sign_in,name="sign_in"),
    path('forgetpassword/',views.forgetpassword,name="forgetpassword"),
    path('invitemember/<str:email>/',views.invitemember, name='invitemember'),
    path('updatememeber/',views.updatememeber,name="updatememeber"),
    
    path('signup/', views.SignUpView, name='signup'),
    path('signin/', views.SignInView, name='signin'),
    path('forget-password/', views.ResetPasswordRequest, name='forget-password'),
    path('reset-password/<uidb64>/<token>/', views.ResetPasswordConfirm, name='reset-password-confirm'),
    path('InviteMemberView/', views.InviteMemberView, name='InviteMemberView'),
    path('update-member-role/<int:user_id>/<int:org_id>/', views.UpdateMemberRole, name='update-member-role'),
    path('delete-member/<int:user_id>/<int:org_id>/', views.delete, name='delete-member'),
]