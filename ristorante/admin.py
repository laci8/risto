from django.contrib import admin
from .models import Menu


# importa la tabella creata per renderla visibile nel pannello di amministrazione

admin.site.register(Menu)
#     #passo i dati alla pagina html