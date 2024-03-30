from enum import Enum

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class SchemaTags(Enum):
    AUTHORIZATION = "Authorization"


API_METADATA = {
    "SendConfirmationCodeView_post": {
        "operation_description": "Receiving a confirmation code. "
                                 "By SMS if the SMS service is active, or with a response if not.",
        "tags": ['Authorization'],
        "request_body": openapi.Schema(
            description="User's phone number. Format '+7<10 digits>'",
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['phone_number']
        ),
        "responses": {
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    description='4 digit code',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )),
            404: 'User with this phone number does not exist',
            429: "Too many requests. No more than 3 requests per minute for 1 phone number"
        }
    },
    "VerifyConfirmationCode_create": {
        "operation_description": "Code verification",
        "tags": ['Authorization'],
        'request_body': openapi.Schema(
            description='4 digit code received via SMS or from the server',
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['code']
        ),
        'responses': {
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING,
                                                       description="JWT Token"),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="User data",
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                     description='User ID'),
                                'phone_number': openapi.Schema(type=openapi.TYPE_STRING,
                                                               description='Phone number'),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING,
                                                             description='First name'),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING,
                                                            description='Last name'),
                                'is_trainer': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                             description='Is the user a trainer or not'),
                                'is_phone_number_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                           description='Is the phone number verified'),
                                'created_at': openapi.Schema(type=openapi.TYPE_STRING,
                                                             description='Date and time of user create'),
                                'updated_at': openapi.Schema(type=openapi.TYPE_STRING,
                                                             description='Date and time of user update'),
                                'avatar': openapi.Schema(type=openapi.TYPE_STRING,
                                                         description='Link to user avatar'),
                            })
                    }
                )),
            400: 'Invalid code or expired',
        }
    },
    "EntryCreateView_post": {
        "operation_description": "Create a timestamp of check-in",
        "tags": ["Membership check-in"],
        "request_body": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "to_pass_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Membership ID"),
            },
            required=["to_pass_id"]
        ),
        "responses": {
            201: "Created",
            400: "Membership pass with this ID does not exists",
            401: "Client is unauthorized"
        }
    },
}
