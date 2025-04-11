from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Menu
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User

def ristorante(request):
    ristorante = Menu.objects.all()  # recupera tutti gli oggetti della tabella Menu
    return render(request, 'ristorante/ristorante.html',{"ristorante": ristorante})  


# pagina contattaci

def contattaci(request):
    return render(request, 'ristorante/contattaci.html')

# pagina aggiungi al carrello
def aggiungi_al_carrello(request: HttpRequest,piatto_id ):
    # recupera l'id del piatto cliccato sul bottone acquista
    piatto = Menu.objects.get(id=piatto_id)
    # attiva la sessione avviando una lista con il nome carello 
    carrello = request.session.get('carrello', []) 
    
    # recupera tutte le info del piatto cliccato e le salva nelle chiavi
    # metodo append per aggiungere altri piatti
    carrello.append(  {
            'id': piatto.id,
            'immagine': piatto.immagine.url,
            'nome': piatto.name,
            'price': piatto.price
        }) 
    
    # aggiorna la sessione carrello con quelllo che ha memoirizzato nel metodo append()
    request.session['carrello'] = carrello  # aggiorna il carrello nella sessione

    # forza il save della sessione
    request.session.modified = True  # segna la sessione come modificata
    messages.success(request, f"{piatto.name} aggiunto al carrello!")  # messaggio di successo
    # ritorna alla pagina home
    return redirect('home')  

#bottone ordina subito
def visualizza_carrello(request: HttpRequest):
    # estrae tutti i piatti dal carrello(session)
    carrello = request.session.get('carrello',[])
    totale = sum(piatto['price'] for piatto in carrello)  # calcola il totale 
    return render(request, 'ristorante/ordini.html', {'carrello': carrello, 'totale': totale})  

# bottone paga presente nella pagina ordini.html
def paga(request: HttpRequest):
    
    # verifica se la sessione contiene la voce carrello
    if 'carrello' in request.session:
        # svuota il carrello dalla sessione
        del request.session['carrello'] 

    messages.success(request, 'Grazie per aver acquistato! \nIl tuo carrello è vuoto!')  
    return redirect('home')  # reindirizza alla home page dopo il pagamento


""" ------------------ pagine per la registrazione - login - logout ------------------ """




def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # creazione del campo unique per l'email
        email = request.POST.get('email') # recupera l'email dal client in fase di registrazione 

        if User.objects.filter(email=email).exists(): 
            # se esiste invia l errore al form dicendo che l'utente esiste
            form.add_error( 'email','Email già in uso.')
        elif form.is_valid():
            user = form.save() # # salva l'utente creato
            login(request, user) # chiama la pagina di login
            return redirect('home')  # reindirizza alla home page dopo la registrazione
    else:
            form = RegisterForm()  
        # se ottieni degli erroro, vengono salvati nell oggetto form 
        # e vengono visualizzati nella pagina register.html 
    return render(request, 'ristorante/register.html', {'form': form})

def user_login(request: HttpRequest):    # sulla guida non c'è 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) # # login dell'utente
            return redirect('home') # passa alla home page
        else:
            messages.error(request, 'username e password non validi')
    
    return render(request, 'ristorante/login.html', {'login':login}) # se non è un post, torna alla pagina di login


def user_logout(request):
    logout(request) # metodo di logout di django
    return redirect('home') # reindirizza alla home page dopo il logout


"-------- pagina per impostare la nuova password --------"
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm

#il cliente chiede il reset della password 
#mostra il messaggio di inserire la mail per inviare il reset
class CustomPasswordResetView(PasswordResetView):
    #tamplate per richiedere il reset
    template_name = "ristorante/reset_password.html"  
    # redirect verso la pagina di reset password done
    success_url = reverse_lazy('password_reset_done')  # URL di reindirizzamento dopo il successo

    email_template_name = "ristorante/reset_password_email.html"  

    form_class = PasswordResetForm  
# mostra il messaggio che la mail è stata inviata una mail per il reset 
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "ristorante/reset_password_done.html"

#chiede di inserire la nuova password
class CustomPasswordResetConfirmView(PasswordResetConfirmView):

    template_name = "ristorante/reset_password_confirm.html"
    # redirect verso la pagina password reset complete
    success_url = reverse_lazy('password_reset_complete')  

# conferma del cambio password 

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "ristorante/reset_password_complete.html"