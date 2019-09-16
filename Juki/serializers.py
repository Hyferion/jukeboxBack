from rest_framework import serializers

from Juki.models import User, Playlist, Song, Vote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userid', 'display_name')


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('creator', 'identifier', 'members','is_default')
        read_only_fields = ('identifier',)


class SongSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='getUserDisplayName', read_only=True)
    votes = serializers.IntegerField(source='getSongVotes', read_only=True)

    class Meta:
        model = Song
        fields = (
        'id', 'spotifyId', 'user', 'title', 'artist', 'img', 'playlist', 'display_name', 'timePlaying', 'duration',
        'votes')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('user', 'timestamp', 'song')
