from django.conf import settings as base_settings
from storages.backends.s3boto3 import S3Boto3Storage


class S3PublicStorage(S3Boto3Storage):
    def __init__(self, **settings):
        settings.update(
            {
                "querystring_auth": False,
                "default_acl": "public-read",
            }
        )
        super().__init__(**settings)


class S3StaticStorage(S3Boto3Storage):
    def __init__(self, **settings):
        settings.update(
            {
                "querystring_auth": False,
                "default_acl": "public-read",
                "location": base_settings.STATICFILES_LOCATION,
            }
        )
        super().__init__(**settings)
