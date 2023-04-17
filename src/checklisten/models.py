from django.db import models
from simple_history.models import HistoricalRecords

from mitglieder.models import Mitglied, MitgliedAmt
from aemter.models import Recht

class Checkliste(models.Model):
    """
    Datenbankmodell für eine Checkliste.
    
    Felder:

    * mitglied: Das Mitglied, für das die Checkliste erstellt wurde. Darf nicht null sein.
    * amt: Die Funktion, für die die Checkliste erstellt wurde. Kann null sein.
    * history

    Es ist zu beachten, dass die Checkliste gelöscht wird, wenn das zugehörige Mitglied oder die Funktion gelöscht wird. (Cascade)
    """
    mitglied = models.ForeignKey(Mitglied, on_delete=models.CASCADE, null=False)
    amt = models.ForeignKey(MitgliedAmt, on_delete=models.CASCADE, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.amt.__str__()
    class Meta:
        verbose_name = "Checkliste"
        verbose_name_plural = "Checklisten"

class Aufgabe(models.Model):
    """
    Datenbankmodell Aufgabe

    Felder:

    * bezeichnung: Die Aufgabenbezeichnung, die im UI angezeigt wird. Kann bis zu 50 Zeichen lang sein und darf nicht null sein.
    * history
    """
    bezeichnung = models.CharField(max_length=50, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.bezeichnung.__str__()
    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"

class ChecklisteAufgabe(models.Model):
    """
    Datenbankmodell einer spezifischen Aufgabe in einer bestimmten Checkliste.

    Felder:

    * checkliste: Referenziert die Checkliste, zu der diese Aufgabe gehört. Kann nicht null sein.
    * aufgabe: Referenziert die Aufgabe, die zu der Checkliste gehört. Kann nicht null sein.
    * abgehakt: Stellt dar, ob die Aufgabe in dieser bestimmten Checkliste bereits erledigt wurde. Standard ist False.
    * history

    Es ist zu beachten, dass diese Checklisten-Aufgabe gelöscht wird, wenn die zugehörige Checkliste oder die Aufgabe gelöscht wird. (Cascade)
    """
    checkliste = models.ForeignKey(Checkliste, on_delete=models.CASCADE, null=False)
    aufgabe = models.ForeignKey(Aufgabe, on_delete=models.CASCADE, null=False)
    abgehakt = models.BooleanField(default=False, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.checkliste.__str__() + " - " + self.aufgabe.__str__()
    class Meta:
        verbose_name = "Zuordnung Checkliste-Aufgabe"
        verbose_name_plural = "Zuordnungen Checkliste-Aufgabe"

class ChecklisteRecht(models.Model):
    """
    Datenbankmodell eines Rechts, das in einer Checkliste gegeben werden soll.

    Felder:
    
    * checkliste: Die Checkliste, zu der dieses Recht gehört. Kann nicht null sein.
    * recht: Das Recht, was dieser Checkliste zugeordnet wurde. Kann nicht null sein.
    * abgehakt: Stellt dar, ob das Recht in dieser Checkliste schon gegeben wurde. Standard ist False.
    * history

    Es ist zu beachten, dass dieses Checklisten-Recht gelöscht wird, wenn die zugehörige Checkliste oder das Recht gelöscht wird. (Cascade)
    """
    checkliste = models.ForeignKey(Checkliste, on_delete=models.CASCADE, null=False)
    recht = models.ForeignKey(Recht, on_delete=models.CASCADE, null=False)
    abgehakt = models.BooleanField(default=False, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.checkliste.__str__() + " - " + self.recht.__str__()
    class Meta:
        verbose_name = "Zuordnung Checkliste-Recht"
        verbose_name_plural = "Zuordnungen Checkliste-Recht"
