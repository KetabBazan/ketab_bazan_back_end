from rest_framework import generics, status, parsers, renderers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from pytz import unicode

from .serializers import UserSerializer, AuthCustomTokenSerializer

class UserSignUp(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = UserSerializer

class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': f'Bye {request.user.nickname}!'},
            status=status.HTTP_204_NO_CONTENT
        )    

class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)  

    def get(self, request):
        return Response(
            data={'nickname': request.user.nickname},
            status=status.HTTP_200_OK
        )    

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': unicode(token.key),
        }

        return Response(content)