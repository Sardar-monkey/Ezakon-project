from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name="main_page" ),
    path('chat_ai/', views.chat_page, name="chat_page" ),
    path('chat_with_ai/', views.chat_with_ai, name="chat_with_ai" ),
    path('all_laws/', views.all_laws_page, name="all_laws_page"),
    path('all_desc/', views.laws_desc_page, name="laws_desc_page"),
    path('profile/', views.profile_page, name="profile_page"),
    path('Lawyers/', views.lawyers_page, name="lawyers_page"),
    path('LawyerProfile/<int:pk>/', views.lawyer_profile_page, name="LawyerProfile_page"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_act, name="logout_act"),
    path('sorry/', views.sorry, name="sorry"),
    path('comments/<int:pk>/', views.comments_page, name="comments_page"),

]