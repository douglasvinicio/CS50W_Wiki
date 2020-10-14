from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Show single wiki page passing an name argument
def showPage(request, name):

    page = util.get_entry(name)

    markdowner = markdown2.Markdown()
    page = markdowner.convert(page)

    return render(request, "encyclopedia/show_page.html", {
        "page" : page, "file_name": name
    })

#Edit / Update entry page
def edit(request, name):
    if 'content' and 'title' in request.POST:
        content = request.POST['content']
        title = request.POST['title']

        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("showPage", kwargs={'name': title}))

    else:
        return render(request, "encyclopedia/edit.html", {
            "pageContent":util.get_entry(name), "pageTitle": name
        })


#Create new page
def create(request):
    if 'content' and 'title' in request.POST:
        content = request.POST['content']
        title = request.POST['title']

        #Checking if there's an entry with the same title
        if title in util.list_entries():
            return render(request, "encyclopedia/create.html",{
                "error_msg":"There's already a encyclopedia with this title. Try a different title or try to edit the already existent one."
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("showPage", kwargs={'name': title}))
    else:
        return render(request, "encyclopedia/create.html")



def search(request):
    if 'searchField' in request.GET:
        searchField = request.GET['searchField']
        if searchField == "":
            return render(request, "encyclopedia/results.html",{
                "blankSearch" : "Please, fill up the form with the entry name you're looking for.."
            })
        ''' If page exists open up  '''
        if util.get_entry(searchField):
            return showPage(request,searchField)
        
        #Create function to list similar search results here
        else:
            # Getting all wiki entries
            subSearch = util.list_entries()
            # Using list comprehension to get string with substring
            result = [i for i in subSearch if searchField in i]

            return render(request, "encyclopedia/results.html", {
                "result":result
        })

    #If trying to hardcode the adress in browser show error message
    else:
        return render(request, "encyclopedia/results.html", {
            "errorMessage":"Please try again! Something didn't worked out well."
        })


def randomPage(request):
    entriesList = util.list_entries()
    randomChoice = random.choice(entriesList)

    return HttpResponseRedirect(reverse("showPage", kwargs={'name': randomChoice}))