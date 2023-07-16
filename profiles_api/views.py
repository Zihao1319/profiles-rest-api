from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles_api import serializers, models
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from profiles_api import permissions
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

class HelloApiView(APIView):
    """test api view"""
    serializer_class = serializers.HelloSerializer


    def get(self, request, format=None):
        """return a list of apiview features"""

        an_apiview = [
            "uses http methods as function", 
            "is similar to traditional django view", 
            "gives you the most control over your application logico"
        ]

        return Response({"message": "hello", "an_apiview": an_apiview})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f'Hello {name}'
            return Response({"message": message})

        else:
            return Response(
                serializer.errors, 
                status = status.HTTP_400_BAD_REQUEST
                )

    def put (self, request, pk=None):
        """handle updating an object"""
        return Response({"method": "PUT"})

    def patch(self, request, pk=None):
        """partial update only"""
        return Response({"method": "patch"})

    def delete(self, request, pk=None):
        return Response({"method": "delete"})

class HelloViewSet(viewsets.ViewSet):
    """test api viewset"""

    serializer_class = serializers.HelloSerializer;

    def list (self, request):
        """retrun a jellp msg"""
        
        a_viewset = [
            "uses http methods as function", 
            "is similar to traditional django view", 
            "lesser codes"
        ]

        return Response({"message": "hello", "a_viewset": a_viewset})

    def create(self, request):
        """create new hellow message"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f'Hello{name}'
            return Response({"message": message})

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    def retrieve(self, request, pk=None):
        return Response({"method": "get"})

    def update(self, request, pk=None):
        return Response({"method": "put"})

    def partial_update(self, request, pk=None):
        return Response({"method": "patch"})

    def destroy(self, request, pk=None):
        return Response({"method": "delete"})


class UserProfileViewSet(viewsets.ModelViewSet):
    """handle creating and udpdating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset= models.UserProfile.objects.all()

    #create a tuple when you add comma to the end of variable 
    authentication_classes = (TokenAuthentication,)
    permission_classes= (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "email",)


class UserLoginApiView(ObtainAuthToken):
    """handle creating user authentication tokens"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus,IsAuthenticated)

    # gets called whenever we call the http POST in this viewset
    # This method is called during the creation of a new ProfileFeedItem instance. 
    # It is a hook provided by DRF that allows you to perform additional actions before saving the new instance
    def perform_create(self, serializer):
        """set the user profile to the logged in user"""
        serializer.save(user_profile = self.request.user)

