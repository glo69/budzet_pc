from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Baza_wydatkow(models.Model):
    autor = models.ForeignKey('auth.User')
    rok = models.IntegerField()
    miesiac = models.IntegerField()
    tydzien = models.IntegerField()
    dzien = models.IntegerField()
    okres = models.CharField(max_length = 8) 
    typ = models.CharField(max_length = 128)
    cena = models.DecimalField(max_digits = 9, decimal_places = 2)
    komentarz = models.CharField(max_length = 256)
    data_utworzenia = models.DateTimeField(default=timezone.now)
    #wydatek_jednorazowy = models.BooleanField(default = False)
    #wydatek_jednorazowy = models.CharField(max_length = 3)
    
    def __str__(self):
		return self.typ
		
class Typ_wydatku(models.Model):
	nazwa_wydatku = models.CharField(max_length = 128)
	nazwa_skrocona = models.CharField(max_length = 128)
	
	def __str__(self):
		return self.nazwa_wydatku

class Lista_okresow(models.Model):
	nazwa_okresu = models.CharField(max_length = 8)
	wplywy_w_okresie = models.DecimalField(max_digits = 9, decimal_places = 2)
	poczatek_okresu = models.DateTimeField()
	koniec_okresu = models.DateTimeField()
	komentarz = models.CharField(max_length = 256)
	ilosc_dni = models.IntegerField()
	autor = models.ForeignKey('auth.User')
	
	def __str__(self):
		return self.nazwa_wydatku
