from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, name):
    #necesito el NAME porque asi busco que quiero mostrar, basicamente en el path yo pongo str:name y el name del titulo va a ser lo que yo busque con al funcion
    markdown = util.get_entry(name)
    print(markdown)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })