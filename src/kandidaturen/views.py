from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Kandidatur, KandidaturAmt, KandidaturMail
from aemter.models import Funktion, Organisationseinheit, Unterbereich
from mitglieder.models import Mitglied, MitgliedAmt, MitgliedMail
import datetime
import simplejson, json
import re
from .funktions import *



# Anzahl der Aemter bzw. E-Mails die gespeichert werden muessen
aemternum = 0
emailnum = 0

def main_screen(request):
    """
    Zeigt eine Tabelle mit Kandidaturen an und ermöglicht die Suche nach Kandidaturen mit bestimmten Namen.
    Admins wird zusätzlich das Löschen von einem oder mehreren Kandidaturen sowie das Wechseln zur View zum Erstellen oder zum Bearbeiten ermöglicht.

    Aufgaben:

    * Bereitstellung der Daten: Die View holt sämtliche Kandidaturen-Einträge aus der Datenbank und stellt diese als Kontext bereit.
    * Rendern des Templates
    * Rechteeinschränkung: Nur Admins können Kandidaturen erstellen, bearbeiten und löschen.

    :param request: Die HTML-Request, welche den Aufruf der View ausgelöst hat.
    :return: Die gerenderte View.
    """
    
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")

    if not request.user.is_superuser:
        messages.error(request, "Du hast keine Berechtigung für diesen Zugriff!")
        return redirect("/")

    # Paginate data
    queryset = Kandidatur.objects.order_by(Lower('vorname'), Lower('name'))

    paginator = Paginator(queryset, 15) # Show 15 entries per page
    queryset_page = paginator.get_page(1) # Get entries for the first page

    return render(
        request=request,
        template_name="kandidaturen/kandidaturen.html",
        context={"data": queryset_page
                 })

@user_passes_test(lambda u: u.is_superuser, login_url="/")
def kandidaturErstellenView(request):
    """
    View zum Erstellen einer Kandidatur.

    Stellt Textfelder, Dropwdowns und Buttons zum Hinzufügen der Attribute bereit. Anfangs steht jeweils genau ein Eingabebereich für ein Amt und eine E-Mail-Adresse zur Verfügung. Über Buttons können weitere dieser hinzugefügt oder bereits bestehende entfernt werden.

    Mit Betätigung des Speichern-Buttons wird überprüft, ob Name, Vorname, Ämter und E-Mail-Adressen ausgefüllt wurden und ob alle E-Mail-Adressen gültig sind. 
    Bei erfolgreicher Prüfung wird die Kandidatur gespeichert und der Nutzer zu main_screen umgeleitet, ansonsten werden Felder mit fehlenden oder fehlerhaften Eingaben rot markiert.

    Aufgaben:

    * Zugriffsbeschränkung: Zugriff wird nur gewährt, wenn der Nutzer angemeldet UND Administrator ist.
    * Rendern des Templates
    * Speichern der Kandidatur in der Datenbank

    :param request: Die HTML-Request, welche den Aufruf der View ausgelöst hat.
    :return: Die gerenderte View.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")
    # beim Erstellen existiert anfangs jeweils ein Feld fuer Funktion und E-Mail
    global aemternum, emailnum
    aemternum = emailnum = 1
    # Laden aller Referate
    referate = Organisationseinheit.objects.order_by('bezeichnung')
    # Anzahl von E-Mails, Aemtern sowie Referate werden an Frontend gesendet
    return render(
        request=request,
        template_name="kandidaturen/kandidatur_erstellen_bearbeiten.html",
        context={'referate':referate, 'amtid': aemternum, 'emailid': emailnum
                 })


# Kandidatur erstellen
def erstellen(request):

    """
    Speichert eine neue Kandidatur in der Datenbank.

    Aufgaben:

    * Speichern der Daten: Die Daten werden aus request gelesen und in die Datenbank eingefügt.
    * Weiterleitung zur Kandidaturenansicht.
    * Rechteeinschränkung: Nur Admins können die Funktion auslösen.

    :param request: Die POST-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält alle Daten zu einer Kandidatur.
    :return: Weiterleitung zur Kandidaturenansicht.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    global aemternum, emailnum
    if request.method == 'POST':
        # Kandidatur
        vorname = request.POST['vorname']
        nachname = request.POST['nachname']
        spitzname = request.POST['spitzname']
        wahldatum_str = request.POST['wahldatum']
        wahldatum = datetime.datetime.strptime(wahldatum_str, "%d.%m.%Y").date()
        beschlussnummer = request.POST['beschlussnummer']
        kandidatur = Kandidatur(name=nachname, vorname=vorname, spitzname=spitzname, wahldatum=wahldatum, beschlussnummer=beschlussnummer)
        kandidatur.save()

        # E-Mail
        for i in range(1, emailnum+1):
            email = request.POST['email'+str(i)]
            kandidaturmail = KandidaturMail(email=email, kandidatur=kandidatur)
            kandidaturmail.save()

        # Funktion
        for i in range(1, aemternum+1):
            amt_id = request.POST['selectamt'+str(i)]
            funktion = Funktion.objects.get(pk=amt_id)

            kandidaturamt = KandidaturAmt(funktion=funktion, kandidatur=kandidatur)
            kandidaturamt.save()

        return HttpResponseRedirect(reverse('kandidaturen:homepage'))
    else:
        return HttpResponseRedirect('/kandidaturen/erstellen')


@user_passes_test(lambda u: u.is_superuser, login_url="/")
def kandidaturBearbeitenView(request, kandidatur_id):
    """
    View zum Bearbeiten einer Kandidatur.

    Stellt Textfelder, Dropwdowns und Buttons zum Bearbeiten der Attribute bereit, welche mit derzeitigen Attributen der Kandidatur befüllt sind. Über Buttons können weitere Ämter und E-Mail-Adressen hinzugefügt oder bereits bestehende entfernt werden.

    Mit Betätigung des Speichern-Buttons wird überprüft, ob Name, Vorname, Ämter und E-Mail-Adressen ausgefüllt wurden und ob alle E-Mail-Adressen gültig sind. Bei erfolgreicher Prüfung wird die Kandidatur gespeichert und der
    Nutzer zu main_screen umgeleitet, ansonsten werden Felder mit fehlenden oder fehlerhaften Eingaben rot markiert.

    Aufgaben:

    * Zugriffsbeschränkung: Zugriff wird nur gewährt, wenn der Nutzer angemeldet UND Administrator ist.
    * Bereitstellung der Daten: Die View holt Attribute einer Kandidatur aus der Datenbank und zeigt diese an.
    * Rendern des Templates
    * Speichern der Kandidatur in der Datenbank

    :param request: Die HTML-Request, welche den Aufruf der View ausgelöst hat.
    :param kandidatur_id: ID der Kandidatur, die bearbeitet werden soll
    :return: Die gerenderte View.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        print("redirect")
        return redirect("/")
    global aemternum, emailnum

    kandidatur = Kandidatur.objects.get(pk=kandidatur_id)
    aemternum = kandidatur.kandidaturamt_set.all().count()
    emailnum = kandidatur.kandidaturmail_set.all().count()
    referate = Organisationseinheit.objects.order_by('bezeichnung')
    funktionen = kandidatur.kandidaturamt_set

    return render(
        request=request,
        template_name="kandidaturen/kandidatur_erstellen_bearbeiten.html",
        context={
            'kandidatur': kandidatur,
            'funktionen': funktionen,
            'referate': referate
                 })

#bearbeitete Kandidatur speichern
def speichern(request, kandidatur_id):
    """
    Speichert eine bearbeitete Kandidatur in der Datenbank.

    Aufgaben:

    * Speichern der Daten: Die Daten werden aus request gelesen und in der Datenbank gespeichert. Ämter und E-Mails werden gespeichert, indem zunächst alle bereits vorhandenen Instanzen gelöscht werden
      und anschließend alle Ämter und E-Mails aus request gespeichert werden.
    * Weiterleitung zur Kandidaturenanischt.
    * Rechteeinschränkung: Nur Admins können die Funktion auslösen.

    :param request: Die POST-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält alle Daten zu einer Kandidatur.
    :param kandidatur_id: Die ID der Kandidatur, die bearbeitet wurde.
    :return: Weiterleitung zur Kandidaturenansicht.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    if request.method == 'POST':
        kandidatur = Kandidatur.objects.get(id=kandidatur_id)
        kandidatur.vorname = getValue(request, 'vorname')
        kandidatur.name = getValue(request, 'nachname')
        kandidatur.spitzname = getValue(request, 'spitzname')
        kandidatur.save()

        # alle Aemter der Kandidatur loeschen
        kandidatur.kandidaturamt_set.all().delete()

        for i in range(1, aemternum + 1):
            amt_id = request.POST['selectamt' + str(i)]
            # print(amt_id)
            funktion = Funktion.objects.get(pk=amt_id)
            # print(funktion)

            kandidaturamt = KandidaturAmt(funktion=funktion, kandidatur=kandidatur)
            kandidaturamt.save()

        # alle Mails loeschen und im Formular angegebene Mails angeben
        kandidatur.kandidaturmail_set.all().delete()
        for i in range(1, emailnum + 1):
            email = request.POST['email' + str(i)]
            kandidaturmail = KandidaturMail(email=email, kandidatur=kandidatur)
            kandidaturmail.save()

    return HttpResponseRedirect(reverse('kandidaturen:homepage'))


def kandidatur_laden(request):
    """
    Rendert ein Modal mit allen Daten einer aus der Tabelle gewählten Kandidatur.
    Aufgaben:
    * Bereitstellung der Daten: Die Kandidatur-ID wird aus request gelesen und extrahieren aller Daten zur Kandidatur mit dieser ID
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können das gerenderte Template anfordern.
    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält die Id der Kandidatur, dessen Daten angezeigt werden sollen.
    :return: Das gerenderte Modal, das mit Daten der angeforderten Kandidatur ausgefüllt wurde
    """

    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    # Extrahieren der Kandidatur-Id aus der GET-Request
    kandidatur_id = simplejson.loads(request.GET.get('kandidaturid'))
    # Daten zur Kandidatur mit dieser Id an Frontend senden
    kandidatur = Kandidatur.objects.get(pk=kandidatur_id)
    funktionen = kandidatur.kandidaturamt_set.all()

    return render(
        request=request,
        template_name='kandidaturen/modal.html',
        context={
            'kandidatur': kandidatur,
            'funktionen': funktionen,
        })


# Entfernen von Kandidaturen aus der Datenbank
def kandidaturen_loeschen(request):
    """
    Löscht ausgewählte Kandidaturen aus der Datenbank.

    Aufgaben:

    * Entfernen der Daten: Alle Daten der Kandidaturen werden aus der Datenbank entfernt.
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können Löschvorgänge auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält die IDs der Kandidaturen, die entfernt werden sollen
    :return: HTTP Response
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")
    # Extrahieren der Liste aller Kandidaturen-Ids und Entfernen der Kandidaturen aus Datenbank
    kandidaturenids = request.POST.get('kandidaturen')
    kandidaturenids = json.loads(kandidaturenids)
    for kandidaturenid in kandidaturenids:
        Kandidatur.objects.get(pk=kandidaturenid).delete()
    return HttpResponse()


# Unterbereiche eines Referats an das Frontend senden
def bereiche_laden(request):
    """
    Rendert ein Dropdown mit allen Bereichen eines bestimmten Referats beim dazugehörigen Amt, nachdem ein Referat bei der Kandidaturenerstellung oder -bearbeitung ausgewählt wurde.

    Aufgaben:

    * Bereitstellung der Daten: Alle Bereiche eines Referats werden aus der Datenbank entnommen.
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können den Vorgang auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält den Namen des ausgewählten Referats sowie die Nummer des Amts einer Kandidatur.
    :return: Das gerenderte Dropdown.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")

    global aemternum
    referat_id = request.GET.get('organisationseinheit')
    amtnum = request.GET.get('amtnum')
    bereiche = Organisationseinheit.objects.get(pk=referat_id).unterbereich_set.all()
    funktionen_ohne_unterbereich_count = Organisationseinheit.objects.get(pk=referat_id).funktionen_ohne_unterbereich_count

    return render(
        request=request,
        template_name='kandidaturen/bereich_dropdown_list_options.html',
        context={
            'bereiche': bereiche,
            'amtid': amtnum,
            'funktionen_ohne_unterbereich_count': funktionen_ohne_unterbereich_count
        })


# Aemter eines Bereichs an das Frontend senden
def funktionen_laden(request):
    """
    Rendert ein Dropdown mit allen Ämtern eines bestimmten Bereich beim dazugehörigen Amt, nachdem ein Bereich bei der Kandidaturenerstellung oder -bearbeitung ausgewählt wurde.

    Aufgaben:

    * Bereitstellung der Daten: Alle Ämter eines Bereichs werden aus der Datenbank entnommen.
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können den Vorgang auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält den Namen des ausgewählten Bereichs sowie die dazugehörige Nummer des Amts einer Kandidatur.
    :return: Das gerenderte Dropdown.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")

    global aemternum
    bereich_id = request.GET.get('bereich')
    amtnum = request.GET.get('amtnum')
    # als Bereich wurde "keiner" gewaehlt => nur Aemter des Referats ohne Bereich werden geladen
    if bereich_id == "-1":
        referat_id = request.GET.get('organisationseinheit')
        aemter = Organisationseinheit.objects.get(pk=referat_id).funktion_set.all()
        aemter = aemter.filter(unterbereich__isnull=True)
    # Laden aller Aemter fuer gewaehlten Unterbereich
    else:
        aemter = Unterbereich.objects.get(pk=bereich_id).funktion_set.all()
        # print(bereich_id)
        # print(aemter)
    return render(
        request=request,
        template_name='kandidaturen/amt_dropdown_list_options.html',
        context={
            'aemter': aemter,
            'amtid': amtnum
        })



# Formular fuer ein Funktion hinzufuegen (Kandidatur erstellen/bearbeiten)
def funktionen_html_laden(request):
    """
    Rendert ein Formular für ein weiteres Amt, nachdem dieses angefordert wurde und inkrementiert die Anzahl der Formulare für ein Amt in der View.

    Aufgaben:

    * Bereitstellung der Daten: Alle Referate werden aus der Datenbank entnommen.
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können den Vorgang auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat.
    :return: Das gerenderte Formular.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")

    global aemternum
    aemternum += 1
    referate = Organisationseinheit.objects.order_by('bezeichnung')
    # Senden von aemternum an Frontend, um HTML-Elementen richtige Id zuzuordnen
    return render(
        request=request,
        template_name='kandidaturen/aemter.html',
        context={
            'referate': referate,
            'amtid': aemternum
        })

# Formular fur ein Funktion loeschen (Kandidatur erstellen/bearbeiten)
def funktion_loeschen(request):
    """
    Dekrementiert die Anzahl der Formulare für ein Amt in der KandidaturBearbeitenView oder KandidaturErstellenView nach Löschen eines Formulars.

    Aufgaben:

    * Erfassen der Anzahl der Ämter
    * Rechteeinschränkung: Nur angemeldete Nutzer können den Vorgang auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat.
    :return: HTTP Response
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    global aemternum
    aemternum-=1
    return HttpResponse()


# Formular fur eine E-Mail hinzufuegen (Kandidatur erstellen/bearbeiten)
def email_html_laden(request):
    """
    Rendert ein Formular für eine weitere E-Mail, nachdem diese angefordert wurde und inkrementiert die Anzahl der Formulare für eine E-Mail in der View.

    Aufgaben:

    * Rendern des Formulars
    * Erfassen der Anzahl der E-Mails einer Kandidatur
    * Rechteeinschränkung: Nur angemeldete Nutzer können den Vorgang auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat.
    :return: HTTP Response
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")

    global emailnum
    emailnum +=1
    return render(
        request=request,
        template_name='kandidaturen/email.html',
        context={
            'emailid': emailnum
        })

# Formular für eine E-Mail loeschen (Kandidatur erstellen/bearbeiten)
def email_loeschen(request):
    """
    Dekrementiert die Anzahl der Formulare für eine E-Mail in der KandidaturBearbeitenView oder KandidaturErstellenView nach Löschen eines Formulars.

    Aufgaben:

    * Erfassen der Anzahl der E-Mails
    * Rechteeinschränkung: Nur angemeldete Nutzer können den Vorgang auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat.
    :return: HTTP Response
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    global emailnum
    emailnum-=1
    return HttpResponse()


    # Suche in der Kandidaturenanzeige
def suchen(request):
    """
    Anzeige von Kandidaturen, deren Namen auf die Sucheingabe passen.

    Aufgaben:

    * Bereitstellung der Daten: Die Sucheingabe wird in mehrere Suchbegriffe unterteilt. Bei allen Kandidaturen der Datenbank wird überprüft, ob sie mindestens einen der Suchbegriffe
      im Vor- oder Nachnamen als Substring enthalten. Diese Kandidaturen werden angezeigt und nach der Anzahl der Suchbegriffe, die auf den Vor- oder Nachnamen passen, sortiert.
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können die Funktion auslösen.

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält die Sucheingabe.
    :return: Das gerenderte Templates mit den gefunden Kandidaturen.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")

    search_string = request.GET.get('search_string')
    page_number = request.GET.get('page')

    # Trennzeichen: ", ", "," oder " "
    tokens = re.split(', |,| ', search_string)
    # leere Strings aus Liste entfernen
    search_tokens = [t for t in tokens if t]

    if not search_tokens:
        # Paginate data
        queryset = Kandidatur.objects.order_by('vorname', 'name')
        paginator = Paginator(queryset, 15) # Show 15 entries per page
        queryset_page = paginator.get_page(page_number) # Get entries for that page

        return render(request=request,
                  template_name="kandidaturen/row.html",
                  context = {"data": queryset_page})

    # Hinzufuegen aller Kandidaturen zum QuerySet, deren Vor- oder Nachnamen ein Token enthalten
    matches={}
    for token in search_tokens:
        kandidaturen_name_matches = Kandidatur.objects.filter(name__icontains=token)
        kandidaturen_vorname_matches = Kandidatur.objects.filter(vorname__icontains=token)
        # Speichern, wie viele Matches es fuer jede Kandidatur gibt
        for queryset in kandidaturen_name_matches, kandidaturen_vorname_matches:
            for m in queryset:
                if m.id in matches:
                    matches[m.id]+=1
                else:
                    matches[m.id]=1

    # Kandidaturen-Ids nach Anzahl der Matches sortieren
    matches_sorted = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1])}
    # Kandidaturenliste fuellen
    kandidaturen_matches = []
    kandidatur = lambda pk : Kandidatur.objects.get(id=pk)
    for kandid in matches_sorted :
        kandidaturen_matches.insert(0, kandidatur(kandid))

    # Paginate data
    paginator = Paginator(kandidaturen_matches, 15) # Show 15 entries per page
    kandidaturen_matches_page = paginator.get_page(page_number) # Get entries for that page

    return render(request=request,
                  template_name="kandidaturen/row.html",
                  context={
                      "data": kandidaturen_matches_page
                  })


def kandidatur_aufnehmen(request):
    """
    Nimmt eine Kandidatur als Mitglied auf.

    Aufgaben:

    * Übernahme der Kandidaturendaten in ein neues Mitglied und speichern in der Datenbank.
    * Löschen der alten Kandidatur.
    * Rechteeinschränkung: Nur Admins können die Funktion auslösen.

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält die ID der Kandidatur, die aufgenommen werden soll
    :return: HTTP Response
    """

    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    
    kandidaturid = request.POST.get('kandidatur')
    kandidatur = Kandidatur.objects.get(pk=kandidaturid)
    name = kandidatur.name
    vorname = kandidatur.vorname
    spitzname = kandidatur.spitzname

    mitglied = Mitglied(name=name, vorname=vorname, spitzname=spitzname)
    mitglied.save()

    for kandidaturamt in kandidatur.kandidaturamt_set.all(): 
        mitgliedamt = MitgliedAmt(funktion=kandidaturamt.funktion, mitglied = mitglied, amtszeit_beginn=kandidatur.wahldatum)
        mitgliedamt.save()
        kandidaturamt.delete()

    for kandidaturmail in kandidatur.kandidaturmail_set.all():
        mitgliedmail = MitgliedMail(email=kandidaturmail.email, mitglied=mitglied)
        mitgliedmail.save()
        kandidaturmail.delete()

    kandidatur.delete()

    return HttpResponse()