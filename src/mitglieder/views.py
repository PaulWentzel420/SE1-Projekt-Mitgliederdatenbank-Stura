from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower
from .models import Mitglied, MitgliedAmt, MitgliedMail
from checklisten.models import Checkliste, ChecklisteAufgabe, ChecklisteRecht, Aufgabe
from aemter.models import Funktion, Organisationseinheit, Unterbereich, FunktionRecht
import datetime
import simplejson, json
# string splitting
import re
from django.db.models import Q
from .funktions import *

# Anzahl der Aemter bzw. E-Mails die gespeichert werden muessen
aemternum = 0
emailnum = 0


def main_screen(request):
    """
    Zeigt eine Tabelle mit Migliedern an und ermöglicht die Suche nach Mitgliedern mit bestimmten Namen.
    Admins wird zusätzlich das Löschen von einem oder mehreren Mitgliedern sowie das Wechseln zur View zum Erstellen oder zum Bearbeiten ermöglicht.

    Aufgaben:

    * Bereitstellung der Daten: Die View holt sämtliche Mitglieder-Einträge aus der Datenbank und stellt diese als Kontext bereit.
    * Rendern des Templates
    * Rechteeinschränkung: Nur Admins können Mitglieder erstellen, bearbeiten und löschen.

    :param request: Die HTML-Request, welche den Aufruf der View ausgelöst hat.
    :return: Die gerenderte View.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")

    # Paginate data
    queryset = Mitglied.objects.order_by(Lower('vorname'), Lower('name'))

    paginator = Paginator(queryset, 15) # Show 15 entries per page
    queryset_page = paginator.get_page(1) # Get entries for the first page

    return render(
        request=request,
        template_name="mitglieder/mitglieder.html",
        context={"data": queryset_page
                 })


@user_passes_test(lambda u: u.is_superuser, login_url="/")
def mitgliedErstellenView(request):
    """
    View zum Erstellen eines Mitglieds.

    Stellt Textfelder, Dropwdowns und Buttons zum Hinzufügen der Attribute bereit. Anfangs steht jeweils genau ein Eingabebereich für ein Amt und eine E-Mail-Adresse zur Verfügung. Über Buttons können weitere dieser hinzugefügt oder bereits bestehende entfernt werden.

    Mit Betätigung des Speichern-Buttons wird überprüft, ob Name, Vorname, Ämter und E-Mail-Adressen ausgefüllt wurden und ob alle E-Mail-Adressen gültig sind. Bei erfolgreicher Prüfung wird das Mitglied gespeichert und der
    Nutzer zu main_screen umgeleitet, ansonsten werden Felder mit fehlenden oder fehlerhaften Eingaben rot markiert.

    Aufgaben:

    * Zugriffsbeschränkung: Zugriff wird nur gewährt, wenn der Nutzer angemeldet UND Administrator ist.
    * Rendern des Templates
    * Speichern des Mitglieds in der Datenbank

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
        template_name="mitglieder/mitglied_erstellen_bearbeiten.html",
        context={'referate':referate, 'amtid': aemternum, 'emailid': emailnum
                 })


# Mitglied erstellen
def erstellen(request):

    """
    Speichert ein neues Mitglied in der Datenbank.

    Aufgaben:

    * Speichern der Daten: Die Daten werden aus request gelesen und in die Datenbank eingefügt.
    * Weiterleitung zur Mitgliederanischt.
    * Rechteeinschränkung: Nur Admins können die Funktion auslösen.

    :param request: Die POST-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält alle Daten zu einem Mitglied.
    :return: Weiterleitung zur Mitgliederansicht.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    global aemternum, emailnum
    if request.method == 'POST':
        # Mitglied
        vorname = request.POST['vorname']
        nachname = request.POST['nachname']
        spitzname = request.POST['spitzname']
        telefon_mobil = request.POST['telefon_mobil']

        if getValue(request, 'auto_checkliste') == 'on':
            auto_checkliste = True
        else:
            auto_checkliste = False

        if getValue(request, 'wahl_angenommen') == 'on':
            wahl_angenommen = True
        else:
            wahl_angenommen = False

        if getValue(request, 'kenntnis_ordn') == 'on':
            kenntnis_ordn = True
        else:
            kenntnis_ordn = False

        if getValue(request, 'verpfl_datengeheimnis') == 'on':
            verpfl_datengeheimnis = True
        else:
            verpfl_datengeheimnis = False

        if getValue(request, 'stammdatenblatt') == 'on':
            stammdatenblatt = True
        else:
            stammdatenblatt = False

        if getValue(request, 'tel_weitergabe') == 'on':
            tel_weitergabe = True
        else:
            tel_weitergabe = False

        mitglied = Mitglied(name=nachname, vorname=vorname, spitzname=spitzname, tel_mobil=telefon_mobil, tel_weitergabe=tel_weitergabe,
                         auto_checkliste=auto_checkliste, wahl_angenommen=wahl_angenommen, kenntnis_ordn=kenntnis_ordn, verpfl_datengeheimnis=verpfl_datengeheimnis, stammdatenblatt=stammdatenblatt)
        mitglied.save()

        # E-Mail
        for i in range(1, emailnum+1):
            email = request.POST['email'+str(i)]
            mitgliedmail = MitgliedMail(email=email, mitglied=mitglied)
            mitgliedmail.save()

        # Funktion
        for i in range(1, aemternum+1):
            amt_id = request.POST['selectamt'+str(i)]
            funktion = Funktion.objects.get(pk=amt_id)
            amtszeit_beginn_str = request.POST['beginn_kandidatur'+str(i)]
            if amtszeit_beginn_str:
                amtszeit_beginn = datetime.datetime.strptime(amtszeit_beginn_str, "%d.%m.%Y").date()
            else:
                amtszeit_beginn = None
            amtszeit_ende_str = request.POST['ende_kandidatur'+str(i)]
            if amtszeit_ende_str:
                amtszeit_ende = datetime.datetime.strptime(amtszeit_ende_str, "%d.%m.%Y").date()
            else:
                amtszeit_ende = None

            mitgliedamt = MitgliedAmt.objects.create(funktion=funktion, mitglied=mitglied, amtszeit_beginn=amtszeit_beginn, amtszeit_ende=amtszeit_ende)
            
            if auto_checkliste:
                checkliste = Checkliste.objects.create(mitglied=mitglied, amt=mitgliedamt)
                for task in Aufgabe.objects.all():
                    aufgabe = ChecklisteAufgabe(checkliste=checkliste, aufgabe=task)
                    aufgabe.save()
                for funktion_recht in FunktionRecht.objects.filter(funktion=funktion):
                    perm = funktion_recht.recht
                    recht = ChecklisteRecht(checkliste=checkliste, recht=perm)
                    recht.save()
    

        return HttpResponseRedirect(reverse('mitglieder:homepage'))
    else:
        return HttpResponseRedirect('/mitglieder/erstellen')


@user_passes_test(lambda u: u.is_superuser, login_url="/")
def mitgliedBearbeitenView(request, mitglied_id):
    """
    View zum Bearbeiten eines Mitglieds.

    Stellt Textfelder, Dropwdowns und Buttons zum Bearbeiten der Attribute bereit, welche mit derzeitigen Attributen des Mitglieds befüllt sind. Über Buttons können weitere Ämter und E-Mail-Adressen hinzugefügt oder bereits bestehende entfernt werden.

    Mit Betätigung des Speichern-Buttons wird überprüft, ob Name, Vorname, Ämter und E-Mail-Adressen ausgefüllt wurden und ob alle E-Mail-Adressen gültig sind. Bei erfolgreicher Prüfung wird das Mitglied gespeichert und der
    Nutzer zu main_screen umgeleitet, ansonsten werden Felder mit fehlenden oder fehlerhaften Eingaben rot markiert.

    Aufgaben:

    * Zugriffsbeschränkung: Zugriff wird nur gewährt, wenn der Nutzer angemeldet UND Administrator ist.
    * Bereitstellung der Daten: Die View holt Attribute eines Mitglieds aus der Datenbank und zeigt diese an.
    * Rendern des Templates
    * Speichern des Mitglieds in der Datenbank

    :param request: Die HTML-Request, welche den Aufruf der View ausgelöst hat.
    :param mitglied_id: Id des Mitglieds, das bearbeitet werden soll
    :return: Die gerenderte View.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")
    global aemternum, emailnum

    mitglied = Mitglied.objects.get(pk=mitglied_id)
    aemternum = mitglied.mitgliedamt_set.all().count()
    emailnum = mitglied.mitgliedmail_set.all().count()
    referate = Organisationseinheit.objects.order_by('bezeichnung')
    curr_funktionen = mitglied.mitgliedamt_set.filter(amtszeit_ende__isnull=True)
    prev_funktionen = mitglied.mitgliedamt_set.filter(amtszeit_ende__isnull=False)

    return render(
        request=request,
        template_name="mitglieder/mitglied_erstellen_bearbeiten.html",
        context={
            'mitglied': mitglied,
            'curr_funktionen': curr_funktionen,
            'prev_funktionen': prev_funktionen,
            'referate': referate
                 })


# bearbeitetes Mitglied speichern
def speichern(request, mitglied_id):
    """
    Speichert ein bearbeitetes Mitglied in der Datenbank.

    Aufgaben:

    * Speichern der Daten: Die Daten werden aus request gelesen und in der Datenbank gespeichert. Ämter und E-Mails werden gespeichert, indem zunächst alle bereits vorhandenen Instanzen gelöscht werden
      und anschließend alle Ämter und E-Mails aus request gespeichert werden.
    * Weiterleitung zur Mitgliederanischt.
    * Rechteeinschränkung: Nur Admins können die Funktion auslösen.

    :param request: Die POST-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält alle Daten zu einem Mitglied.
    :param mitglied_id: Die Id des Mitglieds, das bearbeitet wurde.
    :return: Weiterleitung zur Mitgliederansicht.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    if request.method == 'POST':
        mitglied = Mitglied.objects.get(id=mitglied_id)
        mitglied.vorname = getValue(request, 'vorname')
        mitglied.name = getValue(request, 'nachname')
        mitglied.spitzname = getValue(request, 'spitzname')
        mitglied.tel_mobil = getValue(request, 'telefon_mobil')

        if getValue(request, 'wahl_angenommen') == 'on':
            mitglied.wahl_angenommen = True
        else:
            mitglied.wahl_angenommen = False

        if getValue(request, 'kenntnis_ordn') == 'on':
            mitglied.kenntnis_ordn = True
        else:
            mitglied.kenntnis_ordn = False

        if getValue(request, 'verpfl_datengeheimnis') == 'on':
            mitglied.verpfl_datengeheimnis = True
        else:
            mitglied.verpfl_datengeheimnis = False

        if getValue(request, 'stammdatenblatt') == 'on':
            mitglied.stammdatenblatt = True
        else:
            mitglied.stammdatenblatt = False

        if getValue(request, 'tel_weitergabe') == 'on':
            mitglied.tel_weitergabe = True
        else:
            mitglied.tel_weitergabe = False

        mitglied.save()

        # alle Aemter des Mitglieds loeschen
        mitglied.mitgliedamt_set.all().delete()

        for i in range(1, aemternum + 1):
            amt_id = request.POST['selectamt' + str(i)]
            funktion = Funktion.objects.get(pk=amt_id)
            # Beginn und Ende Amtszeit
            amtszeit_beginn_str = request.POST['beginn_kandidatur' + str(i)]
            if amtszeit_beginn_str:
                amtszeit_beginn = datetime.datetime.strptime(amtszeit_beginn_str, "%d.%m.%Y").date()
            else:
                amtszeit_beginn = None
            amtszeit_ende_str = request.POST['ende_kandidatur' + str(i)]
            if amtszeit_ende_str:
                amtszeit_ende = datetime.datetime.strptime(amtszeit_ende_str, "%d.%m.%Y").date()
            else:
                amtszeit_ende = None

            mitgliedamt = MitgliedAmt(funktion=funktion, mitglied=mitglied, amtszeit_beginn=amtszeit_beginn,
                                      amtszeit_ende=amtszeit_ende)
            mitgliedamt.save()

        # alle Mails loeschen und im Formular angegebene Mails angeben
        mitglied.mitgliedmail_set.all().delete()
        for i in range(1, emailnum + 1):
            email = request.POST['email' + str(i)]
            mitgliedmail = MitgliedMail(email=email, mitglied=mitglied)
            mitgliedmail.save()

    return HttpResponseRedirect(reverse('mitglieder:homepage'))


def mitglied_laden(request):
    """
    Rendert ein Modal mit allen Daten eines aus der Tabelle gewählten Mitlieds.

    Aufgaben:

    * Bereitstellung der Daten: Die Mitglied-Id wird aus request gelesen und extrahieren aller Daten zum Mitglied mit dieser Id
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können das gerenderte Template anfordern.

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält die Id des Mitglieds, dessen Daten angezeigt werden sollen.
    :return: Das gerenderte Modal, das mit Daten des angeforderten Mitglieds ausgefüllt wurde
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    # Extrahieren der Mitglied-Id aus der GET-Request
    mitglied_id = simplejson.loads(request.GET.get('mitgliedid'))
    # Daten zum Mitglied mit dieser Id an Frontend senden
    mitglied = Mitglied.objects.get(pk=mitglied_id)
    curr_funktionen = mitglied.mitgliedamt_set\
        .filter(Q(amtszeit_ende__isnull=True) | Q(amtszeit_ende__gte=date.today()))
    prev_funktionen = mitglied.mitgliedamt_set\
        .filter(Q(amtszeit_ende__isnull=False) & Q(amtszeit_ende__lt=date.today()))
    return render(
        request=request,
        template_name='mitglieder/modal.html',
        context={
            'mitglied': mitglied,
            'curr_funktionen': curr_funktionen,
            'prev_funktionen': prev_funktionen
        })


# Entfernen von Mitgliedern aus der Datenbank
def mitglieder_loeschen(request):
    """
    Löscht ausgewählte Mitglieder aus der Datenbank.

    Aufgaben:

    * Entfernen der Daten: Alle Daten der Mitglieder werden aus der Datenbank entfernt.
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können Löschvorgänge auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält die Ids der Mitglieder, die entfernt werden sollen
    :return: HTTP Response
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")
    # Extrahieren der Liste aller Mitglied-Ids und Entfernen der Mitglieder aus Datenbank
    mitgliederids = request.POST.get('mitglieder')
    mitgliederids = json.loads(mitgliederids)
    for mitgliedid in mitgliederids:
        Mitglied.objects.get(pk=mitgliedid).delete()
    return HttpResponse()


# Unterbereiche eines Referats an das Frontend senden
def bereiche_laden(request):
    """
    Rendert ein Dropdown mit allen Bereichen eines bestimmten Referats beim dazugehörigen Amt, nachdem ein Referat bei der Mitgliedererstellung oder -bearbeitung ausgewählt wurde.

    Aufgaben:

    * Bereitstellung der Daten: Alle Bereiche eines Referats werden aus der Datenbank entnommen.
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können den Vorgang auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält den Namen des ausgewählten Referats sowie die Nummer des Amts eines Mitglieds.
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
        template_name='mitglieder/bereich_dropdown_list_options.html',
        context={
            'bereiche': bereiche,
            'amtid': amtnum,
            'funktionen_ohne_unterbereich_count': funktionen_ohne_unterbereich_count
        })


# Aemter eines Bereichs an das Frontend senden
def funktionen_laden(request):
    """
    Rendert ein Dropdown mit allen Ämtern eines bestimmten Bereich beim dazugehörigen Amt, nachdem ein Bereich bei der Mitgliedererstellung oder -bearbeitung ausgewählt wurde.

    Aufgaben:

    * Bereitstellung der Daten: Alle Ämter eines Bereichs werden aus der Datenbank entnommen.
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können den Vorgang auslösen

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält den Namen des ausgewählten Bereichs sowie die dazugehörige Nummer des Amts eines Mitglieds.
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
        template_name='mitglieder/amt_dropdown_list_options.html',
        context={
            'aemter': aemter,
            'amtid': amtnum
        })


# Formular fuer ein Funktion hinzufuegen (Mitglied erstellen/bearbeiten)
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
        template_name='mitglieder/aemter.html',
        context={
            'referate': referate,
            'amtid': aemternum
        })


# Überprüfen ob Max-Members in einer Funktion schon erreicht ist
def funktionen_max_member_ueberpruefen(request, mitglied_id):
    """
    Überprüft, ob die maximale Anzahl an Mitgliedern in einer Funktion bereits erreicht ist.

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat.
    :param mitglied_id: Die Id des Mitglieds, das bearbeitet wird.
    :return: Eine JsonResponse, die als Key 'is_valid' enthält, und als Wert entweder True oder False.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")

    funktion = None
    list_funktion = []
    amtszeit_beginn = None
    amtszeit_ende = None
    retbool = False


    # Funktion
    for i in range(1, aemternum + 1):
        amt_id = request.POST['selectamt' + str(i)]
        funktion = Funktion.objects.get(pk=amt_id)
        amtszeit_beginn_str = request.POST['beginn_kandidatur' + str(i)]
        if amtszeit_beginn_str:
            amtszeit_beginn = datetime.datetime.strptime(amtszeit_beginn_str, "%d.%m.%Y").date()
        else:
            amtszeit_beginn = None
        amtszeit_ende_str = request.POST['ende_kandidatur' + str(i)]
        if amtszeit_ende_str:
            amtszeit_ende = datetime.datetime.strptime(amtszeit_ende_str, "%d.%m.%Y").date()
        else:
            amtszeit_ende = None

        # Check Max Members
        if funktion.max_members != (0 or None):
            # Maximale Member der Funktion sind begrenzt
            mitglieder_count = 0
            for ma in MitgliedAmt.objects.filter(funktion=funktion):
                # Kein selbstzählen
                if (mitglied_id != 0):
                    if ma.mitglied == Mitglied.objects.get(pk=mitglied_id):
                        continue
                # Mitglieder ohne Datum zählen mit rein
                elif (ma.amtszeit_beginn is None) & (ma.amtszeit_ende is None):
                    mitglieder_count += 1
                # Mitglieder ohne Enddatum, aber Anfangsdatum <= derzeitiges Datum zählen mit rein
                elif (ma.amtszeit_beginn <= date.today()) & (ma.amtszeit_ende is None):
                    mitglieder_count += 1
                elif (is_past_due(ma.amtszeit_beginn, amtszeit_beginn) or is_past_due(ma.amtszeit_beginn, amtszeit_ende)) \
                        and (
                        is_past_due(amtszeit_beginn, ma.amtszeit_ende) or is_past_due(amtszeit_ende, ma.amtszeit_ende)):
                    mitglieder_count += 1
            if funktion.max_members <= mitglieder_count:
                list_funktion.append(funktion.__str__())

    if not list_funktion:
        return JsonResponse({'isValid': True})
    else:
        return JsonResponse({'isValid': False, 'funktion': list_funktion})


# Formular fur ein Funktion loeschen (Mitglied erstellen/bearbeiten)
def funktion_loeschen(request):
    """
    Dekrementiert die Anzahl der Formulare für ein Amt in der mitgliedBearbeitenView oder mitgliedErstellenView nach Löschen eines Formulars.

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


# Formular fur eine E-Mail hinzufuegen (Mitglied erstellen/bearbeiten)
def email_html_laden(request):
    """
    Rendert ein Formular für eine weitere E-Mail, nachdem diese angefordert wurde und inkrementiert die Anzahl der Formulare für eine E-Mail in der View.

    Aufgaben:

    * Rendern des Formulars
    * Erfassen der Anzahl der E-Mails eines Mitglieds
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
        template_name='mitglieder/email.html',
        context={
            'emailid': emailnum
        })


# Formular fur eine E-Mail loeschen (Mitglied erstellen/bearbeiten)
def email_loeschen(request):
    """
    Dekrementiert die Anzahl der Formulare für eine E-Mail in der mitgliedBearbeitenView oder mitgliedErstellenView nach Löschen eines Formulars.

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


# Suche in der Mitgliederanzeige
def suchen(request):
    """
    Anzeige von Mitgliedern, deren Namen auf die Sucheingabe passen.

    Aufgaben:

    * Bereitstellung der Daten: Die Sucheingabe wird in mehrere Suchbegriffe unterteilt. Bei allen Mitgliedern der Datenbank wird überprüft, ob sie mindestens einen der Suchbegriffe
      im Vor- oder Nachnamen als Substring enthalten. Diese Mitglieder werden angezeigt und nach der Anzahl der Suchbegriffe, die auf den Vor- oder Nachnamen passen, sortiert.
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können die Funktion auslösen.

    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält die Sucheingabe.
    :return: Das gerenderte Templates mit den gefunden Mitgliedern.
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
        queryset = Mitglied.objects.order_by('vorname', 'name')
        paginator = Paginator(queryset, 15) # Show 15 entries per page
        queryset_page = paginator.get_page(page_number) # Get entries for that page

        return render(request=request,
                  template_name="mitglieder/row.html",
                  context = {"data": queryset_page})

    # Hinzufuegen aller Mitglieder zum QuerySet, deren Vor- oder Nachnamen ein Token enthalten
    matches={}
    for token in search_tokens:
        mitglieder_name_matches = Mitglied.objects.filter(name__icontains=token)
        mitglieder_vorname_matches = Mitglied.objects.filter(vorname__icontains=token)
        # Speichern, wie viele Matches es fuer jedes Mitglied gibt
        for queryset in mitglieder_name_matches, mitglieder_vorname_matches:
            for m in queryset:
                if m.id in matches:
                    matches[m.id]+=1
                else:
                    matches[m.id]=1

    # Mitglieder-Ids nach Anzahl der Matches sortieren
    matches_sorted = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1])}
    # Mitgliederliste fuellen
    mitglieder_matches = []
    mitglied = lambda pk : Mitglied.objects.get(id=pk)
    for mitid in matches_sorted :
        # print(str(mitid) + " " + str(matches[mitid]))
        # print(mitglied(mitid))
        mitglieder_matches.insert(0, mitglied(mitid))

    # Paginate data
    paginator = Paginator(mitglieder_matches, 15) # Show 15 entries per page
    mitglieder_matches_page = paginator.get_page(page_number) # Get entries for that page

    return render(request=request,
                  template_name="mitglieder/row.html",
                  context={
                      "data": mitglieder_matches_page
                  })
