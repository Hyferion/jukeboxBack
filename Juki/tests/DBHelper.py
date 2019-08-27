from Juki.models import User, Playlist, Song, Vote, PlaylistUser


class DBHelper(object):

    def __init__(self):
        pass

    def create_user(self, userid="a81j82"):
        return User.objects.create(userid=userid)

    def create_playlist(self, creator, identifier="ks13k"):
        return Playlist.objects.create(creator=creator, identifier=identifier)

    def create_song(self, playlist, user, spotifyId="kska2", title="aksi", artist="kalamn"):
        return Song.objects.create(spotifyId=spotifyId, played=False, title=title, artist=artist, playlist=playlist,
                                   user=user)

    def create_vote(self, user, song):
        return Vote.objects.create(user=user, count=1, song=song)

    def create_playlistuser(self,user,playlist):
        return PlaylistUser.objects.create(user=user,playlist=playlist)
