from django.contrib import admin
from models import Baza_wydatkow, Typ_wydatku, Lista_okresow
# Register your models here.


class Baza_wydatkow_admin(admin.ModelAdmin):
	list_display = ('autor','rok','miesiac','tydzien','dzien','okres','typ','cena','komentarz','data_utworzenia')

class Typ_wydatku_admin(admin.ModelAdmin):
	list_display = ('id','nazwa_wydatku','nazwa_skrocona')	
	
class Lista_okresow_admin(admin.ModelAdmin):
	list_display = ('id','nazwa_okresu','poczatek_okresu','koniec_okresu','ilosc_dni','wplywy_w_okresie','komentarz','autor')	
admin.site.register(Baza_wydatkow, Baza_wydatkow_admin)
admin.site.register(Typ_wydatku, Typ_wydatku_admin)
admin.site.register(Lista_okresow, Lista_okresow_admin)

