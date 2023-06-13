from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator

from mitglieder.models import Mitglied, MitgliedMail, MitgliedAmt
from aemter.models import Organisationseinheit, Unterbereich, Funktion, Recht, FunktionRecht
from checklisten.models import Checkliste, ChecklisteAufgabe, ChecklisteRecht
from django.contrib.auth.models import User
from django.db.models import Q

def list(request):
    """
    Diese View wird aufgerufen, wenn der Nutzer über einen Link erstmalig die Historie aufruft (z.B. aus dem Menü heraus).
    
    Folgende Aufgaben werden von dieser übernommen:

    * Bereitstellung von Daten: Es werden alle Historien-Einträge für alle Tabs geholt, anschließend in Seiten je 15 Elemente aufgeteilt und jeweils die erste Seite an die View übergeben.
    * Zugriffsbeschränkung: Zugriff wird nur gewährt, wenn der Nutzer angemeldet UND Administrator ist.
    * Rendern des Templates der gesamten Seite.

    :param request: Die HTML-Request, welche den Aufruf der View ausgelöst hat.
    :return: Die gerenderte View.
    """
    # Access restrictions
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")
    if not request.user.is_superuser:
        messages.error(request, "Du musst Admin sein, um diese Seite aufrufen zu können.")
        return redirect("/mitglieder")

    # Fetch all entries
    mitglieder = Mitglied.history.all()
    mitgliederMails = MitgliedMail.history.all()
    mitgliederAemter = MitgliedAmt.history.all()

    referate = Organisationseinheit.history.all()
    unterbereiche = Unterbereich.history.all()
    aemter = Funktion.history.all()
    rechte = Recht.history.all()
    aemterRechte = FunktionRecht.history.all()

    checklisten = Checkliste.history.all()
    checklistenRechte = ChecklisteRecht.history.all()
    checklistenAufgaben = ChecklisteAufgabe.history.all()

    users = User.history.all()

    # Paginate results
    page_number = 1

    mitgliederPaginator = Paginator(mitglieder, 15)
    mitgliederMailsPaginator = Paginator(mitgliederMails, 15)
    mitgliederAemterPaginator = Paginator(mitgliederAemter, 15)

    referatePaginator = Paginator(referate, 15)
    unterbereichePaginator = Paginator(unterbereiche, 15)
    aemterPaginator = Paginator(aemter, 15)
    rechtePaginator = Paginator(rechte, 15)
    aemterRechtePaginator = Paginator(aemterRechte, 15)

    checklistenPaginator = Paginator(checklisten, 15)
    checklistenRechtePaginator = Paginator(checklistenRechte, 15)
    checklistenAufgabenPaginator = Paginator(checklistenAufgaben, 15)

    usersPaginator = Paginator(users, 15)

    # Get first page for each tab
    mitgliederPage = mitgliederPaginator.get_page(page_number)
    mitgliederMailsPage = mitgliederMailsPaginator.get_page(page_number)
    mitgliederAemterPage = mitgliederAemterPaginator.get_page(page_number)

    referatePage = referatePaginator.get_page(page_number)
    unterbereichePage = unterbereichePaginator.get_page(page_number)
    aemterPage = aemterPaginator.get_page(page_number)
    rechtePage = rechtePaginator.get_page(page_number)
    aemterRechtePage = aemterRechtePaginator.get_page(page_number)

    checklistenPage = checklistenPaginator.get_page(page_number)
    checklistenRechtePage = checklistenRechtePaginator.get_page(page_number)
    checklistenAufgabenPage = checklistenAufgabenPaginator.get_page(page_number)

    usersPage = usersPaginator.get_page(page_number)

    return render(request=request,
                  template_name="historie/list.html",
                  context={"mitglieder": mitgliederPage,
                           "mitgliederMails": mitgliederMailsPage,
                           "mitgliederAemter": mitgliederAemterPage,
                           "referate": referatePage,
                           "unterbereiche": unterbereichePage,
                           "aemter": aemterPage,
                           "rechte": rechtePage,
                           "aemterRechte": aemterRechtePage,
                           "checklisten": checklistenPage,
                           "checklistenRechte": checklistenRechtePage,
                           "checklistenAufgaben": checklistenAufgabenPage,
                           "users": usersPage})

def fetch_entries(request):
    """
    Mit dieser View kann eine Liste von Historien-Einträgen mitsamt passender Pagination angefordert werden, welche die Einträge enthält, die...

    * ...zum angegeben Tab bzw. Model gehören.
    * ...in denen die angegebenen Suchbegriffe vorkommen.
    * ...zur angeforderten Seite gehören.

    Folgende Aufgaben werden durch diese übernommen:

    * Zugriffsbeschränkung: Zugriff wird nur gewährt, wenn der Nutzer angemeldet UND Administrator ist.
    * Bereitstellung von Daten: Die View stellt die gewünschte Seite der Historien-Einträge bereit, welche für das gewünschte Model zu den angegebenen Suchbegriffen gefunden wurden.
    * Rendern der Liste mit den passenden Historien-Einträgen und der zugehörigen Pagination.

    Je nachdem, ob in der `request` Suchbegriffe mitgegeben wurden, werden entweder alle Einträge oder die nach den Suchbegriffen
    gefilterten Einträge bereitgestellt. Die Filterung funktioniert dabei folgendermaßen:
    
    * Das gewünschte Model wird dahingehend untersucht, ob die wichtigsten Felder eines Eintrags (bei Mitgliedern z.B. ID, Vorname und Name) die Suchbegriffe enthalten.
    * Hierfür werden die in Django integrierten `Q Objects` verwendet.
    * Alle gefundenen Einträge werden in einem QuerySet zusammengefasst, welches anschließend an ``render`` übergeben wird.

    :param request: Die HTML-Request, welche den Aufruf der View ausgelöst hat. 
        Enthält stets die gewünschte Seitenzahl, den Namen des Tabs und damit Models, zu dem das Ergebnis geliefert werden soll und optional Suchbegriffe, nach denen das Model durchsucht werden soll.
    :return: Die gerenderte Liste mit den entsprechenden Historien-Einträgen und der zugehörigen Pagination.
    """
    # Access restrictions
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")
    
    # Get data from request
    searchterm = request.GET.get('search')
    page_number = request.GET.get('page')
    selected_tab = request.GET.get('tab')

    # Get indvidiual search terms
    searchterms = None
    if searchterm:
        searchterms = searchterm.split(' ')
        for term in searchterms:
            term = term.strip()
    
    if not searchterm:
        searchterms = [""]
    
    # Get data for selected tab and search terms
    data = None
    if selected_tab == "Mitglied":
        data = Mitglied.history.none()
        for term in searchterms:
            data = data | Mitglied.history.filter(Q(id__icontains=term) | Q(vorname__icontains=term) | Q(name__icontains=term))
    if selected_tab == "MitgliedMail":
        data = MitgliedMail.history.none()
        for term in searchterms:
            data =  data | MitgliedMail.history.filter(Q(mitglied__id__icontains=term) | Q(mitglied__vorname__icontains=term) | Q(mitglied__name__icontains=term) | Q(email__icontains=term))
    if selected_tab == "MitgliedAmt":
        data = MitgliedAmt.history.none()
        for term in searchterms:
            data = data | MitgliedAmt.history.filter(Q(mitglied__id__icontains=term) | Q(mitglied__vorname__icontains=term) | Q(mitglied__name__icontains=term) 
                | Q(funktion__id__icontains=term) | Q(funktion__bezeichnung__icontains=term) 
                | Q(funktion__organisationseinheit__bezeichnung__icontains=term)
                | Q(funktion__unterbereich__bezeichnung__icontains=term))

  
    if selected_tab == "Organisationseinheit":
        data = Organisationseinheit.history.none()
        for term in searchterms:
            data = data | Organisationseinheit.history.filter(Q(id__icontains=term) | Q(bezeichnung__icontains=term))
    if selected_tab == "Unterbereich":
        data = Unterbereich.history.none()
        for term in searchterms:
            data = data | Unterbereich.history.filter(Q(id__icontains=term) | Q(bezeichnung__icontains=term) | Q(organisationseinheit__id__icontains=term) | Q(organisationseinheit__bezeichnung__icontains=term))
    if selected_tab == "Amt":
        data = Funktion.history.none()
        for term in searchterms:
            data = data | Funktion.history.filter(Q(id__icontains=term) | Q(bezeichnung__icontains=term)
                | Q(organisationseinheit__id__icontains=term) | Q(organisationseinheit__bezeichnung__icontains=term)
                | Q(unterbereich__id__icontains=term) | Q(unterbereich__bezeichnung__icontains=term))
    if selected_tab == "Recht":
        data = Recht.history.none()
        for term in searchterms:
            data = data | Recht.history.filter(Q(id__icontains=term) | Q(bezeichnung__icontains=term))
    if selected_tab == "AmtRecht":
        data = FunktionRecht.history.none()
        for term in searchterms:
            data = data | FunktionRecht.history.filter(Q(funktion__id__icontains=term) | Q(funktion__bezeichnung__icontains=term)
                | Q(funktion__organisationseinheit__bezeichnung__icontains=term)
                | Q(funktion__unterbereich__bezeichnung__icontains=term)
                | Q(recht__id__icontains=term) | Q(recht__bezeichnung__icontains=term))
    
    if selected_tab == "Checkliste":
        data = Checkliste.history.none()
        for term in searchterms:
            data = data | Checkliste.history.filter(Q(id__icontains=term) 
                | Q(mitglied__id__icontains=term) | Q(mitglied__vorname__icontains=term) | Q(mitglied__name__icontains=term) 
                | Q(amt__funktion__id__icontains=term) | Q(amt__funktion__bezeichnung__icontains=term) 
                | Q(amt__funktion__organisationseinheit__bezeichnung__icontains=term)
                | Q(amt__funktion__unterbereich__bezeichnung__icontains=term))
    if selected_tab == "ChecklisteRecht":
        data = ChecklisteRecht.history.none()
        for term in searchterms:
            data = data | ChecklisteRecht.history.filter(Q(checkliste__id__icontains=term) 
                | Q(recht__id__icontains=term) | Q(recht__bezeichnung__icontains=term)
                | Q(checkliste__mitglied__id__icontains=term) | Q(checkliste__mitglied__vorname__icontains=term) | Q(checkliste__mitglied__name__icontains=term) 
                | Q(checkliste__amt__funktion__id__icontains=term) | Q(checkliste__amt__funktion__bezeichnung__icontains=term) 
                | Q(checkliste__amt__funktion__organisationseinheit__bezeichnung__icontains=term)
                | Q(checkliste__amt__funktion__unterbereich__bezeichnung__icontains=term))
    if selected_tab == "ChecklisteAufgabe":
        data = ChecklisteAufgabe.history.none()
        for term in searchterms:
            data = data | ChecklisteAufgabe.history.filter(Q(checkliste__id__icontains=term) 
                | Q(aufgabe__id__icontains=term) | Q(aufgabe__bezeichnung__icontains=term)
                | Q(checkliste__mitglied__id__icontains=term) | Q(checkliste__mitglied__vorname__icontains=term) | Q(checkliste__mitglied__name__icontains=term) 
                | Q(checkliste__amt__funktion__id__icontains=term) | Q(checkliste__amt__funktion__bezeichnung__icontains=term) 
                | Q(checkliste__amt__funktion__organisationseinheit__bezeichnung__icontains=term)
                | Q(checkliste__amt__funktion__unterbereich__bezeichnung__icontains=term))

    if selected_tab == "User":
        data = User.history.none()
        for term in searchterms:
            data = data | User.history.filter(Q(username__icontains=term) | Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(email__icontains=term))

    # Paginate results
    paginator = Paginator(data, 15)
    data_page = paginator.get_page(page_number)

    return render(request=request,
                  template_name="historie/row.html",
                  context={"data": data_page})

