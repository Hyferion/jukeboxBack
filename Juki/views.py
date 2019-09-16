import base64
import random
import string
import requests

from rest_framework import mixins, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Juki.config import CLIENT_SECRET, CLIENT_ID, AUTH_URL, REDIRECT_URI
from Juki.models import User, Playlist, Song, Vote
from Juki.serializers import UserSerializer, PlaylistSerializer, SongSerializer, VoteSerializer


@api_view(['POST'])
def add_members_to_playlist(request):
    if request.method == 'POST':
        try:
            member = request.data.get('member')
            identifier = request.data.get('playlist')
        except AttributeError:
            return Response(status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.get(identifier=identifier)
        user = User.objects.get(userid=member)

        playlist.members.add(user)
        playlist.save()

        return Response(status.HTTP_200_OK)


@api_view(['POST'])
def play(request):
    if request.method == 'POST':
        try:
            access_token = request.data.get('access_token')
            playlist = request.data.get('playlist')
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        songs = Song.objects.filter(playlist__identifier=playlist)
        firstSong = Song.objects.filter(playlist__identifier=playlist).first()

        header = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }
        body = {"uris": ["spotify:track:" + firstSong.spotifyId]}
        print(body)
        r = requests.put('https://api.spotify.com/v1/me/player/play', headers=header, json=body)

        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def trade_refresh_for_token(request):
    if request.method == 'POST':
        try:
            refresh_token = request.data.get('refreshToken')
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        auth_str = '{}:{}'.format(CLIENT_ID, CLIENT_SECRET)
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic {}'.format(b64_auth_str)
        }
        body = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
        r = requests.post(AUTH_URL, data=body, headers=header)
        answer = r.json()

        access_token = answer['access_token']
        data = {'access_token': access_token}
        return Response(data)


@api_view(['POST'])
def trade_code_for_token(request):
    if request.method == 'POST':
        try:
            code = request.data.get('code')
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        auth_str = '{}:{}'.format(CLIENT_ID, CLIENT_SECRET)
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic {}'.format(b64_auth_str)
        }
        body = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI}
        r = requests.post(AUTH_URL, data=body, headers=header)
        answer = r.json()

        refresh_token = answer['refresh_token']
        access_token = answer['access_token']
        data = {'access_token': access_token, 'refresh_token': refresh_token}
        return Response(data)


def randomStringDigits(stringLength=5):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


class UserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PlaylistListDefault(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(is_default=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PlaylistList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        queryset = Playlist.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            querysetowner = Playlist.objects.filter(creator=user)
            querysetmember = Playlist.objects.filter(members=user)
            return querysetowner | querysetmember
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = PlaylistSerializer(data=request.data)
        playlistIdentifier = randomStringDigits()

        serializer.is_valid(raise_exception=True)
        serializer.save(identifier=playlistIdentifier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SongList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = Song.objects.all()
        playlist = self.request.query_params.get('playlist', None)
        if playlist is not None:
            queryset = Song.objects.filter(playlist=playlist)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class VoteList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
