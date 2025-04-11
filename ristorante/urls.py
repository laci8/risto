from django.urls import path
from ristorante import views

urlpatterns = [
    # collegamento alla prima pagina (Home)
    path('', views.ristorante, name='home'),
    # collegamento alla pagina contattaci
    path('contattaci/', views.contattaci, name='contattaci'),
    
    # collegamento alla pagina registrazione
    path('register/', views.register, name='register'),
    
    # collegamento alla pagina di login
    
    path('login/', views.user_login, name='login'),

    # collegamento alla pagina di logout
    path('logout/', views.user_logout, name='logout'),

    # collegamento alla pagina aggiungi al carrello
    path('aggiungi_al_carrello/<int:piatto_id>/',views.aggiungi_al_carrello, name='aggiungi_al_carrello'),

    # collegamento alla pagina visualizza carrello
    path('visualizza_carrello/', views.visualizza_carrello, name='visualizza_carrello'),

    # collegamento al bottone paga presente nella pagina visulizza_carrello.html
    path('paga/', views.paga, name='paga'),

    # ----------------- Reset Password
    path('reset_password/', views.CustomPasswordResetView.as_view(), name='reset_password'), 
    path('ristorante/reset_password_done', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # ----------------- Reset Password
    


]
