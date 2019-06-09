import os, re
from datetime import datetime, timedelta
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings

from authentication.models import User, ForgotPassword
from .serializers import UserSerializer

VALID_EMAIL_REGEX = r'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$'

@api_view(['POST'])
def signup(request):
    payload = request.data.copy()
    payload.update({
        'username': payload.get('email', None)
    })
    serializer = UserSerializer(data=payload, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)    
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Create ForgotPassword object with the provided payload
    payload = {
        'email': serializer.instance.email,
        'expired': False,
        'valid_upto': datetime.now() + timedelta(days=1),
        'created_on': datetime.now()
    }
    instance = ForgotPassword.objects.create(**payload)
    # send email
    send_email(serializer.instance.email, 'CortaSwamp - Create your Password', 'Click <a href="%s/reset-password/%s">Here</a> to reset your password'%(settings.FROM_DOMAIN, instance.id))
    return Response({'message': 'User created successfully'}, status=status.HTTP_200_OK)


def send_email(to, subject, body):

    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to,
        subject=subject,
        html_content=body)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


class CheckResetPasswordView(APIView):
    """
    No authentication & permission classes are needed
    as this view will be accessed prior to login,
    hence, these attributes are empty tuples
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, *args, **kwargs):
        """
        @email
        """
        is_valid, email, user_id = self.check_link(*args, **kwargs)
        return Response({'valid': is_valid, 'email': email, 'id': user_id}, status=status.HTTP_200_OK)

    def check_link(self, *args, **kwargs):
        try:
            instance = ForgotPassword.objects.get(id=kwargs['id'])
        except Exception:
            return False, None, None  # exit

        if instance.expired is True:
            return False, None, None  # exit
        current_datetime = datetime.isoformat(datetime.now())  # + datetime.timedelta for testing

        if current_datetime > instance.valid_upto.isoformat():
            instance.expired = True
            instance.save()
            return False, None, None  # exit
        return (True, instance.email, instance.id)  # exit


class ResetPasswordView(CheckResetPasswordView):
    """
    No authentication & permission classes are needed
    as this view will be accessed prior to login,
    hence, these attributes are empty tuples
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        @password
        """
        is_valid, email, user_id = self.check_link(*args, **kwargs)
        if not is_valid or email is None:
            return Response({
                'valid': is_valid,
                'status': False
            }, status=status.HTTP_400_BAD_REQUEST)

        # Read the password from the request
        password = request.data.get('password', None)

        # Check for email key in the request payload
        if password is None or password == '':
            return Response("Password is not supplied", status=status.HTTP_400_BAD_REQUEST)

        # Update the password
        user = User.objects.get(email__iexact=email)
        user.set_password(password)
        user.save()

        # expire the link
        password_recovery = ForgotPassword.objects.get(id=user_id)
        password_recovery.expired = True
        password_recovery.save()

        return Response({
            'valid': is_valid,
            'status': True
        }, status=status.HTTP_200_OK)

class ResetPasswordLink(object):

    def is_valid_email(self, email):
        if email is not None:
            if re.match(VALID_EMAIL_REGEX, email) is not None:
                return True
        return False

    def send_reset_password_link(self, email, id):
        """
        params:
        @email : EMail to which link should be mailed
        @id: PK - ID of forgot password
        """
        # email engine objects
        send_email(email, 'CortaSwamp - Create your Password', 'Click <a href="%s/reset-password/%s">Here</a> to reset your password'%(settings.FROM_DOMAIN, id))


class ForgotPasswordView(APIView, ResetPasswordLink):
    """
    No authentication & permission classes are needed
    as this view will be accessed prior to login,
    hence, these attributes are empty tuples
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        # Post email as parameter from the client and validate email against user database
        email = request.data.get('email', '')

        # 1. Checking if the email is in valid format
        if not self.is_valid_email(email):
            return Response("Invalid email address", status=status.HTTP_200_OK)

        # 2. Get user queryset and validate
        try:
            user = User.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            return Response("Email Address Not Found in the System", status=status.HTTP_400_BAD_REQUEST)

        # 3. Invalidate older links if reset link was previously sent to the user
        ForgotPassword.objects.filter(email__iexact=email).update(expired=True)

        payload = {
            'email': email,
            'expired': False,
            'valid_upto': datetime.now() + timedelta(days=1),
            'created_on': datetime.now()
        }

        # 4. Create ForgotPassword object with the provided payload
        instance = ForgotPassword.objects.create(**payload)

        # 5. Send email from sendgrid to the recepient
        is_sent = self.send_reset_password_link(email, instance.id)
        if is_sent:
            return Response("Reset Link sent to your specified email address", status=status.HTTP_200_OK)
        return Response("Something went Wrong, Please contact Administrator", status=status.HTTP_200_OK)
