from django.core.management.base import BaseCommand, CommandError
from datetime import timedelta
from django.utils import timezone

from mitglieder.models import Mitglied, MitgliedAmt, MitgliedMail

class Command(BaseCommand):
    help = 'Deletes all entries concerning Mitglieder from the Historie older than 5 years. If the associated Mitglied is not in the database anymore, the entry will be deleted if it is older than 1 year.'

    def handle(self, *args, **options):
        """
        This command deletes all entries from the history of Mitglied, MitgliedAmt and MitgliedMail that

        * are at least 1 year old if the referenced Mitglied does not exist in the database anymore
        * are at least 5 years old otherwise

        Please note that 1 year is equivalent to 365 days, so leap years are not accounted for.

        It can be called using ``python manage.py delete_old_historie`` and can thus be automated, for example by setting up a cronjob.
        """
        # Mitglied
        self.stdout.write('Deleting entries from Mitglied Historie...')
        mitglied_history = Mitglied.history.filter(history_date__lte=timezone.now()-timedelta(days=365))
        mitglied_counter = 0
        for entry in mitglied_history:
            if not Mitglied.objects.get(id=entry.mitglied.id):
                entry.delete()
                mitglied_counter += 1
        self.stdout.write('Deleted ' + str(mitglied_counter) + ' entries from Mitglied Historie older than 1 year')
        (mitglied_counter, _) = Mitglied.history.filter(history_date__lte=timezone.now()-timedelta(days=1825)).delete()
        self.stdout.write('Deleted ' + str(mitglied_counter) + ' entries from Mitglied Historie older than 5 years')

        # MitgliedAmt
        self.stdout.write('Deleting entries from MitgliedAmt Historie...')
        mitglied_amt_history = MitgliedAmt.history.filter(history_date__lte=timezone.now()-timedelta(days=365))
        mitglied_amt_counter = 0
        for entry in mitglied_amt_history:
            if not Mitglied.objects.get(id=entry.mitglied_id):
                entry.delete()
                mitglied_amt_counter += 1
        self.stdout.write('Deleted ' + str(mitglied_amt_counter) + ' entries from MitgliedAmt Historie older than 1 year')
        (mitglied_amt_counter, _) = MitgliedAmt.history.filter(history_date__lte=timezone.now()-timedelta(days=1825)).delete()
        self.stdout.write('Deleted ' + str(mitglied_amt_counter) + ' entries from MitgliedAmt Historie older than 5 years')

        # MitgliedMail
        self.stdout.write('Deleting entries from MitgliedMail Historie...')
        mitglied_mail_history = MitgliedMail.history.filter(history_date__lte=timezone.now()-timedelta(days=365))
        mitglied_mail_counter = 0
        for entry in mitglied_mail_history:
            if not Mitglied.objects.get(id=entry.mitglied_id):
                entry.delete()
                mitglied_mail_counter += 1
        self.stdout.write('Deleted ' + str(mitglied_mail_counter) + ' entries from MitgliedMail Historie older than 1 year')
        (mitglied_mail_counter, _) = MitgliedMail.history.filter(history_date__lte=timezone.now()-timedelta(days=1825)).delete()
        self.stdout.write('Deleted ' + str(mitglied_mail_counter) + ' entries from MitgliedMail Historie older than 5 years')