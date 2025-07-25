


from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, time

from users.models import Profile
from services.models import Service
from appointments.models import Appointment
from appointments.views import get_next_slots
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Generate minimal test data for Barbershop project'

    def handle(self, *args, **options):
        User = get_user_model()

        # 1. Create a barber user
        barber, created = User.objects.get_or_create(username='par4', defaults={'email': '123@gmail.com'})
        if created:
            barber.set_password('123')
            barber.save()
            Profile.objects.create(user=barber, is_barber=True)
            self.stdout.write(self.style.SUCCESS('Created barber user: par4'))
        else:
            self.stdout.write('Barber user already exists')

        # 2. Create a regular client user
        client, created = User.objects.get_or_create(username='user2', defaults={'email': '123@gmail.com'})
        if created:
            client.set_password('123')
            client.save()
            Profile.objects.create(user=client, is_barber=False)
            self.stdout.write(self.style.SUCCESS('Created client user: user2'))
        else:
            self.stdout.write('Client user already exists')

        # 3. Create a service by barber
        service, created = Service.objects.get_or_create(
            name='Test',
            defaults={
                'description': 'A standard test',
                'price': 20.00,
                'duration': timezone.timedelta(minutes=30),
                'created_by': barber,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created service: Test'))
        else:
            self.stdout.write('Service Test already exists')

        # 4. Create a normal appointment (free slot)
        appt_date = date.today()
        appt_time = time(hour=13, minute=0)
        appt, created = Appointment.objects.get_or_create(
            client=client,
            barber=barber,
            service=service,
            date=appt_date,
            time=appt_time,
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created appointment at {appt_time}'))
            Notification.objects.create(
                recipient=barber,
                message=f'{client.username} added an appointment on {appt_date} at {appt_time}',
            )
        else:
            self.stdout.write('Appointment already exists for 13:00')

        # 5. Attempt conflicting appointment to trigger suggestion
        conflict_time = appt_time
        suggestions = get_next_slots(barber, service.duration)
        self.stdout.write('Conflicting appointment test:')
        self.stdout.write(f'Existing appointment at {conflict_time}. Suggested slots:')
        for slot in suggestions:
            self.stdout.write(f'  - {slot[0]} at {slot[1]}')

        self.stdout.write(self.style.SUCCESS('Test data generation complete.'))
