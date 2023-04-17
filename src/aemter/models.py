from django.db import models
from simple_history.models import HistoricalRecords

class Organisationseinheit(models.Model):
    """
        Datenbankmodell Organisationseinheit

        Felder:

        * bezeichnung
        * history
        * funktionen_ohne_unterbereich_count
    """
    bezeichnung = models.CharField(max_length=50, null=False)
    history = HistoricalRecords()
    funktionen_ohne_unterbereich_count = models.IntegerField(default=0)

    def __str__(self):
        return self.bezeichnung
    def __unicode__(self):
        return u'%s' % self.bezeichnung
    class Meta:
        verbose_name = "Organisationseinheit"
        verbose_name_plural = "Organisationseinheiten"

class Unterbereich(models.Model):
    """
        Datenbankmodell Unterbereich

        Felder:

        * bezeichnung
        * organisationseinheit (Referenziert zugehörige Organisationseinheit)
        * history
    """
    bezeichnung = models.CharField(max_length=50, null=False)
    organisationseinheit = models.ForeignKey(Organisationseinheit, on_delete=models.CASCADE, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.bezeichnung + " (" + self.organisationseinheit.__str__() + ")"
    def __unicode__(self):
        return u'%s' % self.bezeichnung
    class Meta:
        verbose_name = "Unterbereich"
        verbose_name_plural = "Unterbereiche"

class Funktion(models.Model):
    """
        Datenbankmodell Funktion

        Felder:

        * bezeichnung
        * workload
        * max_members (Maximale Anzahl an Mitgliedern in der Funktion)
        * organisationseinheit (Referenziert zugehörige Organisationseinheit)
        * unterbereich (Referenziert zugehörigen Unterbereich)
            Unterbereich kann null sein
        * history
    """
    bezeichnung = models.CharField(max_length=50, null=False)
    workload = models.IntegerField(null=True)
    max_members = models.IntegerField(null=False)
    organisationseinheit = models.ForeignKey(Organisationseinheit, on_delete=models.CASCADE, null=True, blank=True)
    unterbereich = models.ForeignKey(Unterbereich, on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        if self.unterbereich is None:
            return self.bezeichnung + " (" + self.organisationseinheit.__str__() + ")"
        else:
            return self.bezeichnung + ' ' + self.unterbereich.__str__()
    def tostring(self):
        return self.__str__()
    class Meta:
        verbose_name = "Funktion"
        verbose_name_plural = "Funktionen"

class Recht(models.Model):
    """
        Datenbankmodell Recht

        Felder:

        * bezeichnung
        * history
    """
    bezeichnung = models.CharField(max_length=50, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.bezeichnung
    class Meta:
        verbose_name = "Recht"
        verbose_name_plural = "Rechte"

class FunktionRecht(models.Model):
    """
        Datenbankmodell FunktionRecht

        Felder:

        * funktion (Referenziert zugehörige Funktion)
        * recht (Referenziert zugehöriges Recht)
        * history
    """
    funktion = models.ForeignKey(Funktion, on_delete=models.CASCADE, null=False)
    recht = models.ForeignKey(Recht, on_delete=models.CASCADE, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.funktion.__str__() + ": " + self.recht.__str__()
    class Meta:
        verbose_name = "Zuordnung Funktion-Recht"
        verbose_name_plural = "Zuordnungen Funktion-Recht"
