from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Checkliste, Aufgabe, ChecklisteAufgabe, ChecklisteRecht

admin.site.register(Aufgabe, SimpleHistoryAdmin)
