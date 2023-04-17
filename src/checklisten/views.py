from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from .models import Checkliste, ChecklisteAufgabe, ChecklisteRecht, Aufgabe
from aemter.models import FunktionRecht
from mitglieder.models import Mitglied, MitgliedAmt

def main_screen(request):
    """
    Diese View rendert alle vorhandenen Checklisten. Des Weiteren liefert sie die letzten 20 Mitglieder für das Modal, das zum Erstellen einer neuen Checkliste verwendet wird.
    Wenn der User nicht authentifiziert ist, wird eine Fehlermeldung angezeigt und der User wird auf die Anmeldeseite zurückgeleitet.

    :param request: Die HTTP-Request, welche die View auslöst hat.
    :return: Die gerenderte main_screen View oder eine Weiterleitung zur Anmeldeseite, falls der User nicht authentifiziert ist.
    """

    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")

    checklisten = Checkliste.objects.all()
    mitglieder = Mitglied.objects.all().order_by('-id')[:20]

    return render(request=request, 
                  template_name='checklisten/main_screen.html', 
                  context = {"checklisten": checklisten, "mitglieder": mitglieder})

def erstellen(request):
    """
    Diese View ist für das Erstellen einer neuen Checkliste verantwortlich.
    Sie prüft zunächst, ob der User eine neue Checkliste erstellen darf (d. h. authentifiziert und Admin ist).
    Als nächstes werden die IDs des Mitglieds und der Funktion aus der Request geholt, sowie ob allgemeine Aufgaben aufgenommen werden sollen.
    Die View versucht dann, das Mitglied und die Funktion mit der angegebenen ID zu finden und gibt eine Fehlermeldung zurück, falls mindestens eins davon nicht gefunden werden konnte.
    Danach prüft die View, ob für dieses Mitglied und diese Funktion bereits eine Checkliste existiert. Sollte dies der Fall sein, wird dem Benutzer eine Fehlermeldung ausgegeben.
    Zum Schluss wird die neue Checkliste erstellt und alle Aufgaben sowie Rechte gemäß den in der Request angegebenen Parametern hinzugefügt.

    :param request: Die HTTP-Request, welche die View auslöst, einschließlich der Parameter mitgliedSelect, funktionSelect und generalTasksCheckbox.
    :return: Eine HttpResponse, die dem User anzeigt, wenn ein Fehler aufgetreten ist.
    :return: Eine Weiterleitung zu /checklisten, wenn das Erstellen der Checkliste erfolgreich war oder bereits eine Checkliste für das gleiche Mitglied mit gleicher Funktion existiert.
    """

    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    # Get data from request
    mitglied_id = request.POST.get("mitgliedSelect")
    funktion_id = request.POST.get("funktionSelect")
    includeGeneralTasks = request.POST.get("generalTasksCheckbox")

    # Determine if general tasks shall be included
    if includeGeneralTasks == "on" or includeGeneralTasks is None and funktion_id == "-1":
        includeGeneralTasks = True
    else:
        includeGeneralTasks = False

    # Get foreign data
    mitglied = Mitglied.objects.get(id=mitglied_id)
    if not mitglied:
        return HttpResponse("Mitglied does not exist")
    
    # Get funktion if selected
    funktion = None
    if funktion_id != "-1":
        funktion = MitgliedAmt.objects.get(id=funktion_id)
        if not funktion:
            return HttpResponse("Funktion does not exist")

    existing = Checkliste.objects.filter(mitglied=mitglied, amt=funktion)
    if existing:
        messages.error(request, "Es existiert bereits eine Checkliste für dieses Mitglied und diese Funktion.")
        return redirect("/checklisten")

    # Create checkliste
    checkliste = Checkliste(mitglied=mitglied, amt=funktion)
    checkliste.save()

    # Add general tasks if selected
    if includeGeneralTasks == True:
        for task in Aufgabe.objects.all():
            aufgabe = ChecklisteAufgabe(checkliste=checkliste, aufgabe=task)
            aufgabe.save()
    
    # Add Rechte if Funktion was selected
    if funktion is not None:
        for funktion_recht in FunktionRecht.objects.filter(funktion__id=funktion.funktion.id):
            perm = funktion_recht.recht
            recht = ChecklisteRecht(checkliste=checkliste, recht=perm)
            recht.save()

    return redirect("/checklisten")

def abhaken(request):
    """
    Diese View ist dafür verantwortlich, eine Aufgabe in der Checkliste zu aktivieren oder zu deaktivieren.
    Sie prüft zunächst, ob der User eine Aufgabe abhaken darf, d. h. authentifiziert und Admin ist.
    Als nächstes werden die Parameter task_type und task_id aus der request geholt. Sie werden verwendet, um festzustellen, ob eine Aufgabe oder ein Recht geprüft wurde, und um die richtige Aufgabe zu erhalten.
    Zum Schluss wird die Aufgabe je nach aktuellem Status aktiviert oder deaktiviert und die Änderungen gespeichert.

    :param request: Die HTTP-Request, welche die View ausgelöst hat, einschließlich der Parameter task_type und task_id.
    :return: Eine leere HttpResponse, wenn der Vorgang erfolgreich war.
    :return: Eine HttpResponse, die dem User anzeigt, wenn ein Fehler aufgetreten ist oder der User die Operation nicht ausführen darf.
    """

    if not request.user.is_authenticated:
        return HttpResponse("Nice try, FBI.")
    if not request.user.is_superuser:
        return HttpResponse("No way, CIA.")

    # Determine if an Aufgabe or a Recht was selected
    task_type = request.POST.get('task_type')
    if(task_type != "Aufgabe" and task_type != "Recht"):
        return HttpResponse("Invalid task_type")

    # Get the appropriate task from ChecklisteAufgabe or ChecklisteRecht, depending on task_type
    task_id = request.POST.get('task_id')
    if not task_id:
        return HttpResponse("No task_id provided")

    task = None
    if task_type == "Aufgabe":
        task = ChecklisteAufgabe.objects.get(id=task_id)
    if task_type == "Recht":
        task = ChecklisteRecht.objects.get(id=task_id)
    if not task:
        return HttpResponse("Invalid task_id")

    # Flip the (boolean) abgehakt property and save it
    task.abgehakt = not task.abgehakt
    task.save()

    return HttpResponse()

def loeschen(request):
    """
    Diese View ist für das Löschen einer bestehenden Checkliste verantwortlich.
    Zunächst wird geprüft, ob der User die Checkliste löschen darf (d. h. authentifiziert und Admin ist).
    Als nächstes wird die Checkliste mit dem in der request angegebenen Parameter checklist_id gelöscht.
    Da alle Fremdschlüssel-Beziehungen in anderen Models auf Cascade gesetzt sind, muss, wenn die Checkliste gelöscht wird (d. h. in ChecklistRecht und TaskRecht), nur die Checkliste selbst explizit gelöscht werden.

    :param request: Die HTTP-Request, welche die View auslöst, einschließlich der checkliste_id.
    :return: Eine leere HttpResponse, falls das Löschen der Checkliste erfolgreich war.
    : return: Eine HttpResponse, die einen Fehler anzeigt, wenn einer aufgetreten ist oder der User eine Checkliste nicht löschen darf.
    """

    if not request.user.is_authenticated:
        return HttpResponse("Not today, NSA.")
    if not request.user.is_superuser:
        return HttpResponse("Good trick, MI6.")

    # Get Checkliste with specified ID
    checkliste_id = request.POST.get('checkliste_id')
    if not checkliste_id:
        return HttpResponse("No checkliste_id provided")
    checkliste = Checkliste.objects.get(id=checkliste_id)
    if not checkliste:
        return HttpResponse("Invalid checkliste_id")

    # Delete Checkliste
    checkliste.delete()

    return HttpResponse()

def get_funktionen(request):
    """
    Diese View ist dafür verantwortlich, alle Funktionen abzurufen, die einem Mitglied zugeordnet sind, welches im Modal zum Erstellen einer Checkliste ausgewählt wurde.
    Zunächst wird geprüft, ob der User in diesem Zusammenhang eine Liste von Funktionen für ein Mitglied erhalten darf (d. h. der User ist authentifiziert und Admin).
    Als nächstes werden alle Funktionen für die angegebene mitglied_id bestimmt und durch eine gerenderte Vorlage mit Auswahloptionen zurückgegeben, um das Dropdown-Menü im „Checklisten erstellen“ Modal zu füllen.

    :param request: Die HTTP-Request, welche die View auslöst, einschließlich der mitglied_id, um die Funktionen zu erhalten.
    :return: Eine HttpResponse, die dem User anzeigt, wenn ein Fehler aufgetreten ist.
    :return: Die gerenderten Auswahloptionen zum Auffüllen des Dropdown-Menüs, wenn alles erfolgreich war.
    """

    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    mitglied_id = request.GET.get('mitglied_id')
    if not mitglied_id:
        return HttpResponse("No mitglied_id provided")
    funktionen = MitgliedAmt.objects.filter(mitglied__id=mitglied_id)

    return render(request=request, 
                  template_name='checklisten/_funktionSelectOptions.html', 
                  context = {"funktionen": funktionen})