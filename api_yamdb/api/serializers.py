from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя."""
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, name):
        """Запрещено использование имени 'me'."""
        if name == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return name

    class Meta:
        fields = ('username', 'email',)
        model = User


class TokenSerializer(serializers.Serializer):
    """Сериализация для получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
