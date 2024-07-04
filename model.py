from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)

    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def host_meeting(self, start_time, duration):
        meeting = Meeting.objects.create(host=self, start_time=start_time, duration=duration)
        return meeting

    def join_meeting(self, meeting):
        if self not in meeting.audience.all():
            meeting.audience.add(self)
            return f"{self.full_name()} has joined the meeting."
        return f"{self.full_name()} is already in the meeting."

    def exit_meeting(self, meeting):
        if self in meeting.audience.all():
            meeting.audience.remove(self)
            return f"{self.full_name()} has left the meeting."
        return f"{self.full_name()} is not in the meeting."

    def request_as_speaker(self, host, meeting):
        if self not in meeting.audience.all():
            return f"{self.full_name()} is not in the meeting to request as speaker."
        host.add_speaker(self)
        return f"{self.full_name()} has requested to be a speaker."
    

    def __str__(self):
        return self.full_name()


class Meeting(models.Model):
    host = models.ForeignKey(Person, related_name='hosted_meetings', on_delete=models.CASCADE)
    speaker = models.ForeignKey(Person, related_name='speaking_meetings', on_delete=models.SET_NULL, null=True, blank=True)
    audience = models.ManyToManyField(Person, related_name='attending_meetings')
    start_time = models.DateTimeField()
    duration = models.DurationField()

    def meeting_details(self):
        speaker_name = self.speaker.full_name() if self.speaker else "None"
        audience_names = ', '.join([aud.full_name() for aud in self.audience.all()])
        return (f"Meeting hosted by {self.host.full_name()} with speaker {speaker_name}. "
                f"Audience: {audience_names}. Starts at {self.start_time} for {self.duration} minutes.")


class Host(Person):
    def create_space(self):
        return "Space created for the meeting."

    def add_speaker(self, speaker):
        if isinstance(speaker, Person):
            # Assuming a meeting object is available
            meeting = self.hosted_meetings.latest('start_time')
            meeting.speaker = speaker
            meeting.save()
            return f"Speaker {speaker.full_name()} added to the meeting."
        return "Invalid speaker."

    def sound(self):
        return "Sound system is set up."


class Audience(Person):
    def join_meeting(self, meeting):
        if self not in meeting.audience.all():
            meeting.audience.add(self)
            return f"{self.full_name()} joined the meeting."
        return f"{self.full_name()} is already in the meeting."
