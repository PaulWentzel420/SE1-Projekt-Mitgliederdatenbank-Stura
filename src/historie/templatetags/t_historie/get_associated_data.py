from django import template

from mitglieder.models import Mitglied, MitgliedMail, MitgliedAmt
from aemter.models import Organisationseinheit, Unterbereich, Funktion, Recht, FunktionRecht
from checklisten.models import Checkliste, ChecklisteAufgabe, ChecklisteRecht, Aufgabe

register = template.Library()

@register.simple_tag
def get_associated_data(desiredInfo, queryType, primaryKey, timestamp):
    """
    Ermittelt zu einem gegebenen Historien-Eintrag gehörige, zusätzliche Daten.

    Beispiel: Ein Historien-Eintrag zum Model mitglied.MitgliedMail enhält nur die ID des entsprechenden Mitglieds.
    Mit ``get_associated_data`` können sämtliche Daten des zur ID gehörenden Mitglieds (z.B. Name oder Anschrift) ermittelt werden,
    sowohl zum jetzigen Zeitpunkt als auch zu dem Zeitpunkt, zu dem der Historien-Eintrag angelegt wurde.

    :param desiredInfo: Der Name des Models, aus welchem die zusätzlichen Daten ermittelt werden sollen.
        Zulässige Werte: "Mitglied", "Kandidatur", "Funktion", "Unterbereich", "Organisationseinheit", "Recht"
    :type desiredInfo: str

    :param queryType: Gibt an, ob die aktuellen Daten oder die Daten zum Zeitpunkt des Eintrags in die Historie ermittelt werden sollen.
        Zulässige Werte: "latest", "historical"
    :type queryType: str

    :param primaryKey: Die ID des betroffenen Datensatzes, für welchen die Daten ermittelt werden sollen; z.B. die ID des Mitglieds.
    :type primaryKey: int

    :param timestamp: Der Zeitstempel, zu welchem der Historien-Eintrag angelegt wurde. Wird nur benötigt, falls die Daten zum Zeitpunkt
        des Erstellens des Historien-Eintrags ermittelt werden sollen.
    :type timestamp: datetime, "semi-optional"

    :return: Eine Instanz des mittels `desiredInfo` angegebenen Models, welche sämtliche Daten des Objekts mit der ID `primaryKey` zum mittels
        `queryType` und ggf. `timestamp` angegebenen Zeitpunkt enthält.
    """
    if(desiredInfo == "Mitglied"): foreignClass = Mitglied
    if(desiredInfo == "MitgliedAmt"): foreignClass = MitgliedAmt
    if(desiredInfo == "MitgliedMail"): foreignClass = MitgliedMail
    if(desiredInfo == "Funktion"): foreignClass = Funktion
    if(desiredInfo == "Unterbereich"): foreignClass = Unterbereich
    if(desiredInfo == "Organisationseinheit"): foreignClass = Organisationseinheit
    if(desiredInfo == "Recht"): foreignClass = Recht
    if(desiredInfo == "Checkliste"): foreignClass = Checkliste
    if(desiredInfo == "ChecklisteAufgabe"): foreignClass = ChecklisteAufgabe
    if(desiredInfo == "ChecklisteRecht"): foreignClass = ChecklisteRecht
    if(desiredInfo == "Aufgabe"): foreignClass = Aufgabe

    if primaryKey == "": return None

    if queryType == "latest":
        # If the referenced object is still in the database
        associatedEntry = foreignClass.objects.filter(id=primaryKey).first()
        if associatedEntry == None:
            # If the referenced object has been deleted
            associatedEntry = foreignClass.history.filter(id=primaryKey).order_by("-history_date").first()

    if queryType == "historical":
        # If the referenced object is still in the database
        instance = foreignClass.objects.filter(id=primaryKey).first()
        if instance != None:
            try:
                associatedEntry = instance.history.as_of(timestamp)
            except:
                # If the referenced object has been created before history was tracked
                associatedEntry = None
        else:
            # If the referenced object has been deleted
            associatedEntry = foreignClass.history.filter(id=primaryKey).filter(history_date__lte=timestamp).order_by("-history_date").first()

    return associatedEntry
