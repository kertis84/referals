from django.shortcuts import get_object_or_404
from rest_framework import views, viewsets, exceptions, status
from rest_framework.response import Response
from users.models import Referal, SmsCode, User
from users.serializers import ReferalSerializer, SmsCodeSerializer, UserPhoneSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def filter_queryset(self, queryset):
        queryset = queryset.filter(id=self.request.user.id, is_active=True)
        return super().filter_queryset(queryset)


class ReferalView(views.APIView):
    queryset = Referal.objects.all()

    def get_parent_serializer(self, request):
        referal = self.queryset.filter(child_user=request.user).first()
        parent = referal.parent_user if referal else None
        return UserPhoneSerializer(parent)

    def get_children_serializer(self, request):
        queryset = self.queryset.filter(parent_user=request.user)
        children = User.objects.filter(child__in=queryset)
        return UserPhoneSerializer(children, many=True)
    
    def activate_invitation_serializer(self, request):
        invite_code = request.data.get('invite_code')
        parent = User.objects.filter(user_ref=invite_code).exclude(id=request.user.id).first()
        if invite_code is None or parent is None:
            raise exceptions.NotFound()
        data = {'parent_user': parent.id, 'child_user': request.user.id}
        return ReferalSerializer(data=data)

    def wrong_type(*args):
        raise exceptions.ValidationError()

    post_serializers = {
        'activate': activate_invitation_serializer,
    }

    get_serializers = {
        'parent': get_parent_serializer,
        'children': get_children_serializer,
    }

    def get(self, request, *args, **kwargs):
        type = self.kwargs.get('type')
        get_serializer = self.get_serializers.get(type, self.wrong_type)
        serializer = get_serializer(self, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        type = self.kwargs.get('type')
        post_serializer = self.post_serializers.get(type, self.wrong_type)
        serializer = post_serializer(self, request)
        if serializer.is_valid():
            referal = serializer.save()
            serializer = UserPhoneSerializer(referal.parent_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        phone = self.kwargs.get('phone')
        code = request.data.get('code') if (type(request.data) == dict) else None

        if phone is None:
            raise exceptions.AuthenticationFailed()

        if code is None:     # сгенерировать код и направить СМС
            SmsCode.objects.filter(phone=phone).delete()
            code = SmsCode.objects.create(phone=phone)
            # send_code_in_sms(code)
            return Response(status=status.HTTP_201_CREATED)
        else:               # проверить правильный ли код подтверждения, если да, то авторизовать пользователя
            get_object_or_404(SmsCode.objects.all(), phone=phone, code=code).delete()
            user = User.objects.filter(phone=phone).first()
            if not user:
                user = User.objects.create(phone=phone)
                user.set_unusable_password()
                user.save()
            login(request, user)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class SmsCodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = SmsCode.objects.all()
    serializer_class = SmsCodeSerializer

