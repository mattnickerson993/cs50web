from django.shortcuts import render

from . import util


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
