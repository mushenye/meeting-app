class Person:
    def __init__(self, first_name, last_name, middle_name):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name

    def host_meeting(self, start_time, duration):
        return Meeting(host=self, speaker=None, audience=[], start_time=start_time, duration=duration)

    def join_meeting(self, meeting):
        meeting.audience.append(self)
        return f"{self.full_name()} has joined the meeting."

    def exit_meeting(self, meeting):
        if self in meeting.audience:
            meeting.audience.remove(self)
            return f"{self.full_name()} has left the meeting."
        return f"{self.full_name()} is not in the meeting."

    def request_as_speaker(self, host, meeting):
        if self not in meeting.audience:
            return f"{self.full_name()} is not in the meeting to request as speaker."
        host.add_speaker(self)
        return f"{self.full_name()} has requested to be a speaker."


    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"


class Meeting:
    def __init__(self, host, speaker, audience, start_time, duration):
        self.host = host
        self.speaker = speaker
        self.audience = audience
        self.start_time = start_time
        self.duration = duration

    def meeting_details(self):
        speaker_name = self.speaker.full_name() if self.speaker else "None"
        audience_names = ', '.join([aud.full_name() for aud in self.audience])
        return (f"Meeting hosted by {self.host.full_name()} with speaker {speaker_name}. "
                f"Audience: {audience_names}. Starts at {self.start_time} for {self.duration} minutes.")


class Host(Person):
    def create_space(self):
        return "Space created for the meeting."

    def add_speaker(self, speaker):
        if isinstance(speaker, Person):
            self.speaker = speaker
            return f"Speaker {speaker.full_name()} added to the meeting."
        return "Invalid speaker."

    def sound(self):
        return "Sound system is set up."


class Audience(Person):
    def join_meeting(self, meeting):
        if self not in meeting.audience:
            meeting.audience.append(self)
            return f"{self.full_name()} joined the meeting."
        return f"{self.full_name()} is already in the meeting."


# Example usage
host = Host("John", "Doe", "A.")
audience_member = Audience("Charlie", "Brown", "C.")
meeting = host.host_meeting("10:00 AM", 60)

print(host.create_space())
print(host.sound())

print(audience_member.join_meeting(meeting))
print(audience_member.request_as_speaker(host, meeting))
print(meeting.meeting_details())
