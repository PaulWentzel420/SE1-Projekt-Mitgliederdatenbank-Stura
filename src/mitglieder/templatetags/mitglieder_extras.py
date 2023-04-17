from django import template

register = template.Library()

@register.filter
def amtszeit_ende_isnull(value):
    """
    Template-Filter, der prüft, ob der übergebene Wert None ist.
    
    :param value: Der Wert, der überprüft werden soll
    :type value: any
    
    :return: True, wenn der Wert None ist, sonst False.
    :rtype: bool
    """
    if value is None:
        return True
    return False
