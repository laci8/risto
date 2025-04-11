from django.db import models

# crea la tua tabella per il database sqlite

class Menu(models.Model):
    immagine = models.ImageField() #inserisce l'immagine
    name = models.CharField(max_length=50)
    description = models.TextField() #inserire più valori di string
    price = models.FloatField() #inserire un prezzo in decimale

    
    def __str__(self): # Aggiungi questa riga per il metodo __str__
        return self.name # Ritorna il nome del piatto
