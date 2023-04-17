from django import template

from checklisten.models import ChecklisteRecht

register = template.Library()

@register.filter
def get_perms(checklist_id):
    """
    Gets all ChecklisteRecht objects that belong to the Checkliste identified by checklist_id.

    :param checklist_id: The ID of the Checkliste to fetch the ChecklisteRecht objects for.
    :type checklist_id: int

    :return: A QuerySet containing all ChecklisteRecht objects for the specified Checkliste.
    :rtype: QuerySet
    """
    perms = ChecklisteRecht.objects.filter(checkliste_id=checklist_id)
    return perms