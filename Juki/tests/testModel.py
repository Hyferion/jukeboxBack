from django.test import TestCase

from Juki.models import User, Playlist, Song, Vote
from Juki.tests.DBHelper import DBHelper


class UserModelTest(TestCase):

    def setUp(self):
        self.db = DBHelper()

    def test_user_creation(self):
        self.db.create_user()
        self.assertEqual(len(User.objects.all()), 1)


class PlaylistModelTest(TestCase):

    def setUp(self):
        self.db = DBHelper()
        self.user = self.db.create_user()

    def test_playlist_creation(self):
        self.db.create_playlist(self.user)
        self.assertEqual(len(Playlist.objects.all()), 1)


class SongModelTest(TestCase):
    def setUp(self):
        self.db = DBHelper()
        self.user = self.db.create_user()
        self.playlist = self.db.create_playlist(creator=self.user)

    def test_song_creation(self):
        self.db.create_song(playlist=self.playlist, user=self.user)
        self.assertEqual(len(Song.objects.all()), 1)


class VoteModelTest(TestCase):
    def setUp(self):
        self.db = DBHelper()
        self.user = self.db.create_user()
        self.playlist = self.db.create_playlist(creator=self.user)
        self.song = self.db.create_song(playlist=self.playlist, user=self.user)

    def test_vote_creation(self):
        self.db.create_vote(user=self.user, song=self.song)
        self.assertEqual(len(Vote.objects.all()), 1)


class PlaylistUserModelTest(TestCase):
    def setUp(self):
        self.db = DBHelper()
        self.user = self.db.create_user()
        self.playlist = self.db.create_playlist(creator=self.user)

    def test_playlistuser_creation(self):
        self.db.create_playlistuser(user=self.user, playlist=self.playlist)
