from django.db import Error
from google.cloud import secretmanager
from google.cloud import secretmanager_v1
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

secret_manager_client = secretmanager.SecretManagerServiceClient()
access_secret_version = secretmanager_v1.types.service.AccessSecretVersionRequest()


class ClientError(Error):
    pass


class ServerError(Error):
    pass


def get_secret(secret_key: str):
    name = f'projects/829013617684/secrets/{secret_key}/versions/1'
    access_secret_version.name = name
    return secret_manager_client.access_secret_version(request=access_secret_version).payload.data.decode("utf-8")


class GenericModelSerializer(ModelSerializer):

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except ClientError as e:
            from rest_framework.settings import api_settings
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [e]})
