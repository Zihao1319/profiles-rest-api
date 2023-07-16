from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """serializes a name field for testing our api view"""
    
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):

    #to point to a model 
    class Meta:
        model = models.UserProfile

        #these fields will be accessible
        fields = ("id", "email", "name", "password")
        #extra keyword args - this is to set custom config, such as ensuring that only post password is possible, not read (get)
        extra_kwargs = {
            "password" : {
                "write_only": True,
                "style": {"input_type": "password"}
            }
        }
    # to overwrite the default create function in the serializer (not the MODEL's create function!), to create objects
    # in usual cases, this will call the create function of the model set in the meta class
    def create(self, validated_data):
        """"create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data["email"],
            name= validated_data["name"],
            password= validated_data["password"]
        )

        return user

    def update(self, instance, validated_data):
        """handle updating user data"""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProfileFeedItem
        fields = ("id", "user_profile", "status_text", "created_on")
        extrakwargs = {
            "user_profile" : {
                "read_only": True
            }
        }

    

