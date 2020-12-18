from django.shortcuts import render

from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
from markdown2 import Markdown


class NameForm(forms.Form):
    form_title = forms.CharField(label="Page Title", min_length=1, max_length=100, initial='Enter new page title')
    form_content = forms.CharField(widget=forms.Textarea, label="Page Content", initial="Enter markdown content for new page")



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_page(request, title):

    if util.get_entry(title):
        markdowner = Markdown()
        converted_content = markdowner.convert(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "contents" : converted_content,
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

def new_page(request):

    if request.method == 'GET':
        return render(request, "encyclopedia/new_page.html", {
            "form": NameForm()
        })
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            form_title = form.cleaned_data["form_title"]
            form_content = form.cleaned_data["form_content"]
            
            if util.get_entry(form_title):
                return render(request, "encyclopedia/new_page.html", {
                    "error": 'Error: this page already exists',
                    "form" : form
                })
            else:
                util.save_entry(form_title, form_content)
                return HttpResponseRedirect(reverse("display_page", args=(form_title,)))

def edit_content(request, title):
    if request.method == 'GET' and util.get_entry(title):
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_content.html", {
            "title": title,
            "content": content
        })
        
    if request.method == 'POST':
        new_content = request.POST.__getitem__("content-area")
        if new_content:
            util.save_entry(title, new_content)
            return HttpResponseRedirect(reverse("display_page", args=(title,)))

def random_page(request):
    entries = util.list_entries()
    num = random.randint(0, len(entries)-1)
    title = entries[num]
    markdowner = Markdown()
    converted_content = markdowner.convert(util.get_entry(title))

    return render(request, "encyclopedia/entry.html", {
            "contents" : converted_content,
            "title" : title
        })