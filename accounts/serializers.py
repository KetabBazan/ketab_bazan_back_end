from rest_framework import serializers
import random
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from userprofile.models import Profile
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'nickname',
            'password',
            'email',
            'username'
        )
        extra_kwargs = {'username': {'required': False}}

    def create(self, validated_data):

        username_candidate = 'u' + str(random.randint(10**5, 10**6 - 1))
        while User.objects.filter(username=username_candidate).count() > 0:
            username_candidate = 'u' + str(random.randint(10**5, 10**6 - 1))

        validated_data['username'] = username_candidate
        user = User.objects.create_user(**validated_data)
        return user

def validateEmail( email ):
    from django.core.validators import validate_email
    try:
        #validate_email( email ) removed all of email validations from backend side
        try: # Just check if there is an email with given address
            user = User.objects.get(email__iexact=email)
            return True
        except:
            raise ValidationError("Email not in use")
    except ValidationError:
        return False

class AuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if validateEmail(email_or_username):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )

                email_or_username = user_request.username

            user = authenticate(username=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise ValidationError(msg)

        attrs['user'] = user
        return attrs


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('image',)


class SearchUserSerializer(serializers.ModelSerializer):
    profile = ProfileImageSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'profile', )

