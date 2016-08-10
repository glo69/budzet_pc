from django import forms
from django.utils import timezone
from .models import Baza_wydatkow, Typ_wydatku
from functools import partial
from django.forms import ModelChoiceField

def period_table():
    daty = {}
    posts = Baza_wydatkow.objects.filter(data_utworzenia__lte=timezone.now()).order_by('-data_utworzenia')
    aktualny = aktualny_okres()
    for post in posts:
        if (post.okres not in daty):
            daty[post.okres] = post.okres
    return daty
    
class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nazwa_wydatku

class EnterForm(forms.ModelForm):
	
    typ = forms.ModelChoiceField(label='Typ wydatku (*)', queryset=Typ_wydatku.objects.all())
    cena = forms.CharField(label='Zaplacono: (*)')
    komentarz = forms.CharField(label='Dodatkowy komentarz', required=False)
    class Meta:
        model = Baza_wydatkow
        fields = ('typ','cena','komentarz')
        
        
class DetailForm(forms.ModelForm):

    nowy_typ = forms.ModelChoiceField(label='Nowy typ wydatku', queryset=Typ_wydatku.objects.all())
    cena = forms.CharField(label='Zaplacono: (*)')
   
    nowy_okres = forms.CharField(label='Nowy okres:')
    komentarz = forms.CharField(label='Dodatkowy komentarz', required=False)
    class Meta:
        model = Baza_wydatkow
        fields = ('nowy_typ','cena','nowy_okres','komentarz')
        





