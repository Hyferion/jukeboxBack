from django.db import models


class User(models.Model):
    userid = models.CharField(max_length=255, primary_key=True)
    display_name = models.CharField(max_length=255)


class Playlist(models.Model):
    identifier = models.CharField(max_length=255, primary_key=True)
    creator = models.OneToOneField(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, null=True, blank=True, related_name="members")


class Song(models.Model):
    spotifyId = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    img = models.CharField(max_length=255, blank=True, null=True)
    playlist = models.ForeignKey(Playlist, models.CASCADE)
    timeQueued = models.DateTimeField(auto_now_add=True)
    timePlaying = models.BigIntegerField(null=True, blank=True)
    duration = models.BigIntegerField()

    def getUserDisplayName(self):
        return self.user.display_name

    def getSongVotes(self):
        votes = Vote.objects.filter(song_id=self.id)
        return len(votes)

    class Meta:
        unique_together = ('spotifyId', 'playlist')


class Vote(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey(Song, models.CASCADE)

    class Meta:
        unique_together = ('user', 'song')
