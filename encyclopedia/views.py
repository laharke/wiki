from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, name):
    #necesito el NAME porque asi busco que quiero mostrar, basicamente en el path yo pongo str:name y el name del titulo va a ser lo que yo busque con al funcion
    if util.get_entry(name):
        markdown = util.get_entry(name)
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown,
            'title': name
        })
    else:
        messages.error(request, 'Entry not found')
        return redirect('/')

def search(request):
    if request.GET['q'] == '':
        messages.error(request, 'Type something in the search bar')
        return redirect('/')
    if request.method == "GET":
        #si es get y no vacio puede ser dos cosas, o existe y muestro la pagina, o no existe y muestro resultados similares
        #misma funcion que antes para pouplar la pagina y buscar la info
        entry = request.GET['q'].lower()
        if util.get_entry(entry):
            markdown = util.get_entry(entry)
            print(markdown)
            return render(request, "encyclopedia/entry.html", {
                "entry": markdown,
                'title': entry
        })
        #si no se encontro nada, muestro simialres
        else:
            #Primero, agarro una lista ENTERA de todas las entry que tengo con la funcion auxiliar
            list = util.list_entries()
            similarList = []
            # ahora tendria que loopear por esta lista, viendo si entry esta dentro de algunos de los elemetnos
            for item in list:
                itemLower = item.lower()
                if entry in itemLower:
                    print(entry, item)
                    #ya tengo las similares, lo unico quetengo que hacer es meterlas en una lista para enviar al html SERACH
                    similarList.append(item)
            print(similarList)
            messages.error(request, 'Acá hay similares')
            return render(request, "encyclopedia/search.html", {
                "entries": similarList,
        })

class NewEntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())

def new_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            #Si el titulo ya existe, hay que devolver un error
            entries = util.list_entries()
            if title in entries:
                messages.error(request, 'That entry alredy exists')
                return redirect('/')
            #ya guarde la info, call function to save to the computer
            util.save_entry(title, content)
            #ya se creo la entry, ahora redirect the user to the entry itself
            #aca lo que hag oes un redirect a la view entry_page y le paso el title como el name, arriba hice otra cosa porque no me salia en al funcion search, fixear maybe
            return redirect("entry_page", name=title)



    else:
        #render form to user so he can complete it and save the new entry
        return render(request, "encyclopedia/newpage.html", {
            "form": NewEntryForm()
        })
