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
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField(default=time(9))
    duration = models.IntegerField(default=1)  # Duration in hours
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} at {self.start_time} on {self.date}'

    @property
    def end_time(self):
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = start_datetime + timedelta(hours=self.duration)
        return end_datetime.time()

    def clean(self):
        super().clean()

        # Combine date and time into datetime objects
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = start_datetime + timedelta(hours=self.duration)

        # Check if the meeting is scheduled in the future
        if start_datetime < datetime.now():
            raise ValidationError("The meeting cannot be scheduled in the past.")

        # Check for overlapping meetings in the same room
        overlapping_meetings = Meeting.objects.filter(
            room=self.room,
            date=self.date,
            start_time__lt=end_datetime.time(),  # Meetings that start before this meeting ends
            start_time__gte=self.start_time  # Meetings that end after this meeting starts
        ).exclude(id=self.id)

        if overlapping_meetings.exists():
            raise ValidationError("There is an overlapping meeting scheduled in this room.")
