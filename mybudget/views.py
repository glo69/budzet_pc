from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from .forms import EnterForm, DetailForm
from models import Baza_wydatkow, Typ_wydatku
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from django.contrib.auth import logout
from django.db.models import Sum
from datetime import date

# Create your views here.
### FUNKCJE WEWNETRZNE

def aktualny_okres():
#zmiana usunac funkcje domyslnie dodaje sie okres aktualny       
     wynik= 'aktualny'
     return wynik
    
def ilosc_dni():
    #zmiana domyslnie 30 dni
    days = 30
    return days  

def numer_dnia():
	dzis = datetime.datetime.now(timezone.utc)
	aktualny ='aktualny'	
	posts = Baza_wydatkow.objects.filter(data_utworzenia__lte=timezone.now()).exclude (okres = aktualny).latest('data_utworzenia')
	ostatni= posts.data_utworzenia
	nazwa_okresu = posts.okres
	numer = dzis - ostatni
	numer = int(numer.days)
	return numer 
	
def nazwa_nowego_okresu():
	dzis = datetime.datetime.now(timezone.utc)
	rok = dzis.strftime("%Y")
	aktualny ='aktualny'	
	posts = Baza_wydatkow.objects.filter(data_utworzenia__lte=timezone.now()).exclude (okres = 'aktualny').latest('data_utworzenia')
	nazwa_okresu = posts.okres
	nazwa_okresu_miesiac = int (nazwa_okresu [:2])
	nazwa_okresu_rok = 	nazwa_okresu [2:6]
	if rok == nazwa_okresu_rok:
		nazwa_okresu_miesiac = nazwa_okresu_miesiac + 1
		nazwa_okresu = '0' + str(nazwa_okresu_miesiac) + rok
	else:
	    nazwa_okresu_miesiac = '01' + rok
	    
	return nazwa_okresu
	

def period_table():
    daty = {}
    posts = Baza_wydatkow.objects.filter(data_utworzenia__lte=timezone.now()).order_by('-data_utworzenia')
    aktualny = aktualny_okres()
    for post in posts:
        if (post.okres not in daty):
            daty[post.okres] = post.okres
    return daty
    
def end_period(request):
	nowy_okres = nazwa_nowego_okresu()
	posts = Baza_wydatkow.objects.filter(okres='aktualny')
	i = 0
	for post in posts:
		post.okres = nowy_okres
		post.save()
		i = i + 1
	nazwa = nowy_okres
	if i > 0:
		return HttpResponse ('Zamknieto okres aktualny. Zostal zapisany pod nazwa: ' + nazwa + '''</br>
		<button onclick="window.location.href = '/period_list'">OK</button>''')
	else:
		return HttpResponse('''Brak wpisow w okresie aktualnym do zamkniecia </br>
		<button onclick="window.location.href = '/new'">Cofnij</button>''')
		
def details(request, ids):
    username = None
    if request.user.is_authenticated():
	detail = {}
        username = request.user.username
	instance = Baza_wydatkow.objects.get(id = ids)
	form = DetailForm(request.POST or None, instance = instance)
	detail = instance
	#detail["numer"] = ids
	if form.is_valid():
	    form = form.save(commit=False)
	    #dzis = datetime.datetime.now()
	    typ = request.POST.get('typ')
	    nowy_typ = request.POST.get('nowy_typ')
	    nowy_typ = int(nowy_typ)
	    typy = Typ_wydatku.objects.get(id = nowy_typ)
	    typy= str(typy.nazwa_wydatku)
	    if typ != typy:
		form.typ = typy
	    okres = request.POST.get('okres')
	    nowy_okres = request.POST.get('nowy_okres')
	    
	    #post.autor = request.user
            #post.rok = dzis.strftime("%Y")
            #post.tydzien = dzis.strftime("%W")
	    #post.miesiac = dzis.strftime("%m")
	    #post.dzien = dzis.strftime("%d")
	    #post.okres = aktualny_okres()
	    #post.save()
	    form.save()
	    return HttpResponseRedirect("/history")
	else:
	    
	    return render(request, 'details.html', {'form': form, 'detail': detail})
    else:
        return HttpResponseRedirect("/login")

def remove(request, ids):
    Baza_wydatkow.objects.filter(id = ids).delete()
    return HttpResponse('''Wpis usunieto <button onclick="window.location.href = '/period_list'">OK</button>''')		

###REQUESTY   

#wylogowanie    
def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/login")

def question(request):
    return render(request, 'question.html')

#nowy wydatek              
def post_new(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        if request.method == "POST":
            form = EnterForm(request.POST)
            if form.is_valid():
		wartosc = request.POST.get('kolejny_wpis')
                dzis = datetime.datetime.now()
                post = form.save(commit=False)
                post.autor = request.user
                post.rok = dzis.strftime("%Y")
                post.tydzien = dzis.strftime("%W")
                post.miesiac = dzis.strftime("%m")
                post.dzien = dzis.strftime("%d")
                post.okres = aktualny_okres()
		post.save()
		if wartosc == 'on':
		    return HttpResponseRedirect("/new")
		else:
		    return HttpResponseRedirect("/history/lista_krotka")
        else:
            form = EnterForm()
	    post = Baza_wydatkow.objects.all().last()
            return render(request, 'nowy_wydatek.html', {'form': form, 'post':post})
    else:
        return HttpResponseRedirect("/login")

#wybor historii        
def period_list(request):
    daty = {}
    posts = Baza_wydatkow.objects.filter(data_utworzenia__lte=timezone.now()).order_by('-data_utworzenia')
    aktualny = aktualny_okres()
    for post in posts:
        if (post.okres not in daty) and (post.okres != aktualny):
            daty[post.okres] = post.okres
    return render(request, 'historia.html', {'daty': daty})
    qw2
    
#wyswietlnienie wybranego okresu
# aktualny, lista_krotka, none, okres 
def post_actual_period2(request, wybrany_okres=None):
    username = None
    if request.user.is_authenticated():
	if wybrany_okres == None:
	    aktualny = 0
	    aktualny_status = False
	elif wybrany_okres == 'aktualny':
	    aktualny = aktualny_okres()
	    aktualny_status = True
	elif wybrany_okres == 'lista_krotka':
	    aktualny = aktualny_okres()
	    aktualny_status = True
	else:
	    aktualny = wybrany_okres
	    aktualny_status = False 
	    	   
        if aktualny != 0:
	    lista_okresow = period_table()
	    if aktualny not in lista_okresow:
	        return HttpResponse('''Brak danych dla tego okresu - dodaj nowy wpis aby utworzyc okres rozliczeniowy 
		<button onclick="window.location.href = '/new'">OK</button>''')
	username = request.user.username
	dane = {}
        wynik = {}
	tablica = []
	tablica2 = []
	suma = 0
        typy = Typ_wydatku.objects.all()
	if aktualny != 0:
	    for opis in typy:
	        dane [opis.nazwa_skrocona] = str(Baza_wydatkow.objects.filter(okres= aktualny).filter(typ = opis.nazwa_wydatku).aggregate(Sum('cena')).values()[0])
	else:
	    for opis in typy:
	        dane [opis.nazwa_skrocona] = str(Baza_wydatkow.objects.filter(typ = opis.nazwa_wydatku).aggregate(Sum('cena')).values()[0])
	for key, value in dane.iteritems():
            if value == 'None':
	        value = 0
	    temp = float(value)
	    suma = suma + temp
	    tablica2.append(temp)
	    tablica.append (key)
	dane_wykres = { 'categories' : tablica , 'cat': tablica2}
	wynik["Okres"] = aktualny
	dane["Suma"] = suma
               		
        if wybrany_okres == 'aktualny':
	    posts=Baza_wydatkow.objects.filter(okres= aktualny).order_by('-id')
	    wynik["ilosc_dni"] = ilosc_dni()
	    wynik["numer_dnia"] = numer_dnia()
            wynik["sredni_wydatek"] = int (dane["Suma"] / int(wynik["ilosc_dni"]))
            wynik["sredni_wydatek_w_okresie_do_dzis"] = int (dane["Suma"] / int(wynik["numer_dnia"]))
            wynik["przewidywane_wydatki_w_okresie"] = int (dane["Suma"] / (wynik["numer_dnia"])*(wynik["ilosc_dni"]))
	    return render(request, 'lista_wydatkow.html', {'posts': posts, 'dane': dane, 'wynik':wynik, 'dane_wykres':dane_wykres })
	elif wybrany_okres == 'lista_krotka':
	    wynik["ilosc_dni"] = ilosc_dni()
	    wynik["numer_dnia"] = numer_dnia()
            wynik["sredni_wydatek"] = int (dane["Suma"] / int(wynik["ilosc_dni"]))
            wynik["sredni_wydatek_w_okresie_do_dzis"] = int (dane["Suma"] / int(wynik["numer_dnia"]))
            wynik["przewidywane_wydatki_w_okresie"] = int (dane["Suma"] / (wynik["numer_dnia"])*(wynik["ilosc_dni"]))
	    return render(request, 'lista_wydatkow_krotka.html', {'dane': dane, 'wynik':wynik, 'dane_wykres':dane_wykres })
	elif wybrany_okres == None:
	    posts=Baza_wydatkow.objects.all().order_by('-id')
	    return render(request, 'lista_wydatkow_historia.html', {'posts': posts, 'dane': dane, 'wynik':wynik, 'dane_wykres':dane_wykres })
	else:
	    posts=Baza_wydatkow.objects.filter(okres= aktualny).order_by('-id')
	    return render(request, 'lista_wydatkow_historia.html', {'posts': posts, 'dane': dane, 'wynik':wynik, 'dane_wykres':dane_wykres })
    else:
        return HttpResponseRedirect("/login")

def range_date(request):
    name1= 'start_date'
    start_date = request.POST.get(name1)
    end_date = request.POST.get('end_date')
    if start_date =="" or end_date =="":
        return HttpResponse("Podano nieprawidlowe dane")
	
    end_date = end_date + " 23:59:59"
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")  
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S") 
    if start_date > end_date:
	temp = end_date
	end_date = start_date
	start_date = temp
    posts = Baza_wydatkow.objects.filter(data_utworzenia__range=(start_date, end_date))
    dane = {}
    wynik = {}
    tablica = []
    tablica2 = []
    suma = 0
    typy = Typ_wydatku.objects.all()
    for opis in typy:
	dane [opis.nazwa_skrocona] = str(Baza_wydatkow.objects.filter(data_utworzenia__range=(start_date, end_date)).filter(typ = opis.nazwa_wydatku).aggregate(Sum('cena')).values()[0])
    for key, value in dane.iteritems():
	if value == 'None':
	    value = 0
	temp = float(value)
	suma = suma + temp
	tablica2.append(temp)
	tablica.append (key)
    dane_wykres = { 'categories' : tablica , 'cat': tablica2}
    wynik["Okres"] = str(start_date) +" - "+ str(end_date)
    dane["Suma"] = suma
    return render(request, 'lista_wydatkow_historia.html', {'posts': posts, 'dane': dane, 'wynik':wynik, 'dane_wykres':dane_wykres })
    
def range_date3(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    start_date1 = request.POST.get('start_date1')
    end_date1 = request.POST.get('end_date1')
    if start_date == "" or end_date == "":
	start_date = 'pusty'
        return HttpResponse("Podano nieprawidlowe dane")
    end_date = end_date + " 23:59:59"
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")  
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S") 
    if start_date > end_date:
	    temp = end_date
	    end_date = start_date
	    start_date = temp  
    if start_date1 != "" or end_date1 != "":
	    if start_date1 > end_date1:
	        temp = end_date1
	        end_date1 = start_date1
	        start_date1 = temp  
	    end_date1 = end_date1 + " 23:59:59"
            start_date1 = datetime.datetime.strptime(start_date1, "%Y-%m-%d")  
            end_date1 = datetime.datetime.strptime(end_date1, "%Y-%m-%d %H:%M:%S") 
	    typy = Typ_wydatku.objects.all()
	    dane = {}
	    dane1 = {}
            wynik = {}
            tablica = []
            tablica2 = []
	    tablica3 = []
	    suma = 0
	    for opis in typy:
	        dane [opis.nazwa_skrocona] = str(Baza_wydatkow.objects.filter(data_utworzenia__range=(start_date, end_date)).filter(typ = opis.nazwa_wydatku).aggregate(Sum('cena')).values()[0])
                dane1 [opis.nazwa_skrocona] = str(Baza_wydatkow.objects.filter(data_utworzenia__range=(start_date1, end_date1)).filter(typ = opis.nazwa_wydatku).aggregate(Sum('cena')).values()[0])
	    for key, value in dane.iteritems():
                if value == 'None':
	            value = 0
		temp = float(value)
		suma = suma + temp
	        tablica2.append(temp)
	        tablica.append (key)
	    suma = 0
	    for key, value in dane1.iteritems():
                if value == 'None':
	            value = 0
		temp = float(value)
		suma = suma + temp
	        tablica3.append(temp)
	    dane_wykres = { 'categories' : tablica , 'cat': tablica2, 'cat2': tablica3}
	    wynik["Okres"] = str(start_date) + " " + str(end_date) + " do: " + str(start_date1) + " " + str(end_date1)
            return render(request, 'lista_wydatkow_historia_porownanie.html', {'dane': dane, 'dane1': dane1, 'wynik':wynik, 'dane_wykres':dane_wykres })
    else: 
	return HttpResponse("Podano nieprawidlowe dane")
	    
   


############################################333
#wyswietlenie wszystkich okresow     
#usunac!!!!   
def post_all_list(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        posts=Baza_wydatkow.objects.all().order_by('id')
        dane = {}
        wynik = {}
	tablica = []
	tablica2 = []
	suma = 0
        typy = Typ_wydatku.objects.all()
        for opis in typy:
            dane [opis.nazwa_skrocona] = str(Baza_wydatkow.objects.filter(typ = opis.nazwa_wydatku).aggregate(Sum('cena')).values()[0])
        for key, value in dane.iteritems():
            if value == 'None':
	        value = 0
	    temp = float(value)
	    suma = suma + temp
	    tablica2.append(temp)
	    tablica.append (key)
        dane_wykres = { 'categories' : tablica , 'cat': tablica2}
	wynik["Okres"] = 'wszystkie zarejstrowane wydatki'
        dane["Suma"] = suma
        return render(request, 'lista_wydatkow_historia.html', {'posts': posts, 'dane': dane, 'wynik':wynik, 'dane_wykres':dane_wykres })
    else:
        return HttpResponse('Prosze sie zalogowac!!')



#wyswietlnienie wybranego okresu - lista krotka
def post_actual_period_short(request):
    username = None
    if request.user.is_authenticated():
	aktualny = aktualny_okres()
	lista_okresow = period_table()
	if aktualny not in lista_okresow:
	    return HttpResponse('Brak danych dla tego okresu lub dodaj nowy wpis aby utworzyc okres rozliczeniowy')
	username = request.user.username
        #posts=Baza_wydatkow.objects.filter(okres= aktualny).order_by('-id')
        dane = {}
        wynik = {}
	tablica = []
	tablica2 = []
	suma = 0
        typy = Typ_wydatku.objects.all()
        for opis in typy:
	    dane [opis.nazwa_skrocona] = str(Baza_wydatkow.objects.filter(okres= aktualny).filter(typ = opis.nazwa_wydatku).aggregate(Sum('cena')).values()[0])
	for key, value in dane.iteritems():
            if value == 'None':
	        value = 0
	    temp = float(value)
	    suma = suma + temp
	    tablica2.append(temp)
	    tablica.append (key)
	    
        dane_wykres = { 'categories' : tablica , 'cat': tablica2}
	wynik["Okres"] = aktualny
	dane["Suma"] = suma
        wynik["ilosc_dni"] = ilosc_dni()
	wynik["numer_dnia"] = numer_dnia()
        wynik["sredni_wydatek"] = int (dane["Suma"] / int(wynik["ilosc_dni"]))
        wynik["sredni_wydatek_w_okresie_do_dzis"] = int (dane["Suma"] / int(wynik["numer_dnia"]))
        wynik["przewidywane_wydatki_w_okresie"] = int (dane["Suma"] / (wynik["numer_dnia"])*(wynik["ilosc_dni"]))
        return render(request, 'lista_wydatkow_krotka.html', {'dane': dane, 'wynik':wynik, 'dane_wykres':dane_wykres })
    else:
        return HttpResponse('Prosze sie zalogowac!!')

#requesty testowe
def charts(request):
    dane = {}
    dane2 = {}
    tablica = []
    tablica2 = []
    typy = Typ_wydatku.objects.all()
    
    for opis in typy:
        dane2 [opis.nazwa_skrocona] = str(Baza_wydatkow.objects.filter(okres= aktualny_okres()).filter(typ = opis.nazwa_wydatku).aggregate(Sum('cena')).values()[0])
    for key, value in dane2.iteritems():
        if value == 'None':
	    value = 0
	temp = float(value)
	tablica2.append(temp)
	tablica.append (key)
    dane = { 'categories' : tablica , 'cat': tablica2}
    return render(request, 'charts.html', dane)



def test(request):
    wartosc = request.POST.get('your_name')
    wartosc2 = request.POST.get('your_name2')
    wynik = wartosc + wartosc2
    return HttpResponse(wynik)
    
def set_date(request):
    return HttpRedirect("/name")
    

