from allauth.account.admin import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import get_user_model
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

schema_view = get_schema_view(
    openapi.Info(
        title="Users API",
        default_version='v1',
        description="API used to manage user in loteria game",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# Create your views here.
class NewEmailConfirmation(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            return Response({'message': 'This email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                send_email_confirmation(request, user=user)
                return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)
            except APIException:
                return Response({'message': 'This email does not exist, please create a new account'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def serviceStatus(request, *args, **kwargs):
    return Response({'status': 'Users up and ready'}, status=status.HTTP_200_OK)