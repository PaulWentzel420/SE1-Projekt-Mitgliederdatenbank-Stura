from aemter.models import Funktion, Organisationseinheit
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Funktion)
def funktion_post_init(**kwargs):
    instance = kwargs.get('instance')
    if instance.unterbereich is None:
        organisationseinheit = instance.organisationseinheit
        organisationseinheit.funktionen_ohne_unterbereich_count +=1
        organisationseinheit.save()

@receiver(post_delete, sender=Funktion)
def funktion_post_delete(**kwargs):
    instance = kwargs.get('instance')
    if instance.unterbereich is None:
        organisationseinheit = instance.organisationseinheit
        organisationseinheit.funktionen_ohne_unterbereich_count -=1
        organisationseinheit.save()