from rest_framework import serializers
from apps.models.account.models import User


class SigninSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={
            'input_type': 'password',  # password form 가리기
            'placeholder': 'Password'
        }
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
        )


class SignoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()
