from django import template

register = template.Library()

@register.filter
def to_class_name(value):
    """
    Gibt den Namen der Klasse des übergebenen Objekts zurück.
    
    :param value: Das Objekt, von dem die Klasse ermittelt werden soll.
    :type value: any
    
    :return: Den Namen der Klasse des Objekts.
    :rtype: str
    """
    return value.__class__.__name__
