from django.shortcuts import render

from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_page(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "contents" : util.get_entry(title),
            "title" : title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "contents" : "Error: Requested page was not found",
            "title": "ERROR"
        })

def search(request):
    if request.method == 'POST':
        search_item = request.POST.__getitem__("q")
        if util.get_entry(search_item):
            return HttpResponseRedirect(reverse("display_page", args=(search_item,)))

        else:
            entries = util.list_entries()
            items = []
            for entry in entries:
                if search_item.lower() in entry.lower():
                    items.append(entry)
            return render(request, "encyclopedia/search.html", {
                "items": items,
                "search_item": search_item,
                "entries": entries
            })

