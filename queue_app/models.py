from django.db import models
from django.utils import timezone
from django.db.models import Max

class Ticket(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_CALLED = 'CALLED'
    STATUS_SERVED = 'SERVED'
    STATUS_SKIPPED = 'SKIPPED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CALLED, 'Called'),
        (STATUS_SERVED, 'Served'),
        (STATUS_SKIPPED, 'Skipped'),
    ]

    day = models.DateField(default=timezone.localdate, db_index=True)
    number = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    called_at = models.DateTimeField(null=True, blank=True)
    served_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['day', 'number'], name='unique_ticket_per_day')
        ]
        ordering = ['day', 'number']

    def __str__(self):
        return f"{self.day} - {self.number} ({self.status})"

    @classmethod
    def next_number_for_today(cls):
        today = timezone.localdate()
        last = cls.objects.filter(day=today).aggregate(m=Max('number'))['m'] or 0
        return last + 1

    def position_in_queue(self):
        # Count pending tickets with a lower number on the same day
        return Ticket.objects.filter(
            day=self.day,
            status=self.STATUS_PENDING,
            number__lt=self.number
        ).count()
