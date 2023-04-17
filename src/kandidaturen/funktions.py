# Attribut attr (string) wird aus request (POST-Request) entnommen und zurueckgegeben
# bei einem KeyError oder leerem String wird None zurueckgegeben
def getValue(request, attr):
    """
    Entnimmt das Attribut attr aus request und verwendet dieses als Rückgabewert.

    Aufgaben:

    * Entnehmen des Attributs
    * Ausnahmebehandlung und Gültigkeitsüberprüfung: Existiert das Attribut nicht oder ist dieses ein leerer String, so wird None zurückgegeben

    :param request: Eine POST-Request.
    :param attr: Das Attribut, das aus Request entnommen werden soll.
    :return: Der Wert des Attributs attr aus request oder None, falls dieses nicht vorhanden oder ein leerer String ist
    """
    try:
        val = request.POST[attr]
        if val=="":
            val=None
    except KeyError:
        print("KeyError for attribute " + attr)
        val = None
    return val


# preuft, ob date2 liegt hinter date1 liegt
def is_past_due(date1, date2):
    if date1 is None or date2 is None:
        return False
    return date2 > date1