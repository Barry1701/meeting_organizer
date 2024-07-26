from datetime import datetime, time, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Room(models.Model):
    name = models.CharField(max_length=30)
    floor = models.IntegerField(default=0)
    room_number = models.IntegerField()

    def __str__(self):
        return f'{self.name}: Room {self.room_number} on floor {self.floor}'

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(default=time(9))
    duration = models.IntegerField(default=1)  # Duration in hours
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # User who created the meeting

    def __str__(self):
        return f'{self.title} at {self.start_time} on {self.date}'

    @property
    def end_time(self):
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = start_datetime + timedelta(hours=self.duration)
        return end_datetime.time()

    def clean(self):
        super().clean()
        # Custom validation to ensure no overlapping meetings in the same room
        overlapping_meetings = Meeting.objects.filter(
            room=self.room,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)
        if overlapping_meetings.exists():
            raise ValidationError('This meeting overlaps with another meeting in the same room.')

