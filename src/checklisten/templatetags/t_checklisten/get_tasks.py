from django import template

from checklisten.models import ChecklisteAufgabe

register = template.Library()

@register.filter
def get_tasks(checklist_id):
    """
    Gets all ChecklisteAufgabe objects that belong to the Checkliste identified by checklist_id.

    :param checklist_id: The ID of the Checkliste to fetch the ChecklisteAufgabe objects for.
    :type checklist_id: int

    :return: A QuerySet containing all ChecklisteAufgabe objects for the specified Checkliste.
    :rtype: QuerySet
    """
    tasks = ChecklisteAufgabe.objects.filter(checkliste_id=checklist_id)
    return tasks
