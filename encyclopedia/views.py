from django.shortcuts import redirect, render
from django import forms
from . import util
from django.urls import reverse
from random import randint
import markdown2

class NewForm(forms.Form):
    text = forms.CharField(label='', widget=forms.TextInput(attrs={'class':"search", 'style': 'margin: 5px;', 'type':"text", 'name':"q", 'placeholder':"Search Encyclopedia"}))

class NewEntry(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Title...'}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class':"someclass", 'placeholder':'Text...'}))

def index(request):
    if request.method == 'POST':
        form = NewForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            if util.get_entry(text) != None:
                return redirect(f'/wiki/{text}')
            
            else:
                entries = util.list_entries()
                forShow = []

                for i in entries:
                    if text in i:
                        forShow.append(i)
                
                return render(request, "encyclopedia/index.html", {
                    "entries": forShow,
                    'form': form
                })          

        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                'form': form
            })            

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form': NewForm
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, 'encyclopedia/entry.html')

    entry = markdown2.markdown(entry)
    return render(request, 'encyclopedia/entry.html', {
        'entry':entry,
        'title':title,
        'form': NewForm        
    })

def create(request):
    if request.method == 'POST':
        form = NewEntry(request.POST)
        if form.is_valid():
            if util.get_entry(form.cleaned_data['title']) == None:
                title = form.cleaned_data['title']
                text = form.cleaned_data['text']

                with open(f'./entries/{title}.md', 'w') as f:
                    f.write(f'# {title} \n\n' + text)
                
                return redirect(reverse('index'))
            else:
                print('sth')
                return render(request, 'encyclopedia/create.html', {
                    'form':NewForm,
                    'createForm':NewEntry,
                    'error':'There is the post with same title :)'
                })
        
        else:
            return render(request, 'encyclopedia/create.html', {
                'form':NewForm,
                'createForm':NewEntry,
                'error':'Not valid form :)'
            })     

    return render(request, 'encyclopedia/create.html', {
        'form':NewForm,
        'createForm':NewEntry,
        'error':''
    })

def edit(request, title):

    entry = util.get_entry(title)
    if entry == None:
        return render(request, 'encyclopedia/entry.html')

    if request.method == 'POST':
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']

            if title in text[:len(title)+2]:
                text = text.replace(f'# {title}', '')

            with open(f'./entries/{title}.md', 'w') as f:
                f.write(f'# {title} \n\n' + text)
            
            return redirect(f'/wiki/{title}')
        else:
            return redirect(f'/wiki/{title}')

    return render(request, 'encyclopedia/edit.html', {
        'form':NewForm,
        'createForm':NewEntry(None, initial={'title':title, 'text':entry}),
        'error':'',
        'title':title
    })

def rentry(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries) - 1)]
    return redirect(f'/wiki/{title}')
