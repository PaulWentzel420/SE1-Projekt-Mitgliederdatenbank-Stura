from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Organisationseinheit, Unterbereich, Funktion
from mitglieder.models import MitgliedAmt

# Create your views here.
def main_screen(request):
    """
       Zeigt den Funktionen-Tab an
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")

    organisationseinheiten = Organisationseinheit\
        .objects.all()\
        .order_by('bezeichnung')
    paginator = Paginator(organisationseinheiten, 15) # Show 15 entries per page
    page_number = request.GET.get('page') # Get page number from request
    organisationseinheit_page = paginator.get_page(page_number) # Get entries for that page
    organisationseinheiten_ids = organisationseinheit_page.object_list.values_list('id', flat=True) # Get IDs of those entries

    # Only get associated data for current page
    unterbereiche = Unterbereich.objects.filter(organisationseinheit__id__in=organisationseinheiten_ids)
    funktionen = Funktion.objects.filter(Q(organisationseinheit__id__in=organisationseinheiten_ids) | Q(unterbereich__id__in=unterbereiche))
    funktionen_ids = funktionen.values_list('id', flat=True)

    # get current mitglieder funktionen
    mitglieder = MitgliedAmt.objects\
        .filter(Q(funktion__id__in=funktionen_ids) & Q(Q(amtszeit_ende__isnull=True) | Q(amtszeit_ende__gte=date.today())))

    # get prev mitglieder funktionen
    prev_mitglieder = MitgliedAmt.objects\
        .raw('SELECT * From (SELECT funktion_id, MAX(amtszeit_ende) as max_time FROM mitglieder_mitgliedamt GROUP BY funktion_id) u INNER JOIN mitglieder_mitgliedamt m ON m.funktion_id = u.funktion_id AND  m.amtszeit_ende = u.max_time')
        #.filter(amtszeit_ende__lt=date.today())

    context = {
        'referate': organisationseinheit_page,
        'unterbereiche': unterbereiche,
        'aemter': funktionen,
        'mitglieder': mitglieder,
        # type: MitgliedAmt
        'prev_mitglieder': prev_mitglieder
    }

    return render(request, 'aemter/main_screen.html', context)
