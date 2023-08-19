from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.serializers import SmsCodeSerializer, UserPhoneSerializer, UserProfileSerializer
from users.models import CodeGenerator, Referal, SmsCode, User


class UserProfileTest(APITestCase):
    def setUp(self):
        self.user_1 = User.create_random_user()
        self.user_2 = User.create_random_user()
        self.client.force_login(user=self.user_1)

    def test_get_user_profile_list(self):
        response = self.client.get(reverse('user_profile-list'))
        serializer = UserProfileSerializer(self.user_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn(serializer.data, response.data)

    def test_get_user_profile_detail_200(self):
        kw = {'pk': self.user_1.id}
        response = self.client.get(reverse('user_profile-detail', kwargs=kw))
        serializer = UserProfileSerializer(self.user_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_get_user_profile_detail_404(self):
        kw = {'pk': '0'}
        response = self.client.get(reverse('user_profile-detail', kwargs=kw))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_other_user_profile_detail_404(self):
        kw = {'pk': self.user_2.id}
        response = self.client.get(reverse('user_profile-detail', kwargs=kw))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_profile_patch(self):
        data = {'first_name': 'John'}
        kw = {'pk': self.user_1.id}
        serializer = UserProfileSerializer(self.user_1)
        response = self.client.patch(reverse('user_profile-detail', kwargs=kw), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(data, response.data)
        self.assertNotEqual(serializer.data, response.data)

    def test_user_profile_put(self):
        data = {'first_name': 'John'}
        kw = {'pk': self.user_1.id}
        response = self.client.put(reverse('user_profile-detail', kwargs=kw), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_profile_delete(self):
        kw = {'pk': self.user_1.id}
        response = self.client.delete(reverse('user_profile-detail', kwargs=kw))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_profile_post(self):
        data = {'phone': '0000000000'}
        response = self.client.post(reverse('user_profile-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SmsCodeTest(APITestCase):
    def setUp(self) -> None:
        self.sms_code_1 = SmsCode.objects.create(phone='+79111111111', code='1234')
        self.sms_code_2 = SmsCode.objects.create(phone='+79999999999', code='4321')
        
    def test_get_sms_code_list(self):
        response = self.client.get(reverse('sms_codes-list'))
        serializer = SmsCodeSerializer(self.sms_code_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn(serializer.data, response.data)
    
    def test_get_sms_code_detail_200(self):
        response = self.client.get(reverse('sms_codes-detail', kwargs={'pk': self.sms_code_1.phone}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], self.sms_code_1.code)

    def test_get_sms_code_detail_404(self):
        response = self.client.get(reverse('sms_codes-detail', kwargs={'pk': '+00000000000'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LogoutTest(APITestCase):
    def setUp(self):
        self.user = User.create_random_user()
        self.client.force_login(user=self.user)

    def test_user_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.create_random_user()
        self.sms_code = SmsCode.objects.create(phone=self.user.phone)
        self.kwargs = {'phone': self.user.phone}

    def test_post_phone(self):
        response = self.client.post(reverse('login', kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_phone_and_code(self):
        data = {'code': self.sms_code.code}
        serializer = UserProfileSerializer(self.user)
        response = self.client.post(reverse('login', kwargs=self.kwargs), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_post_phone_and_wrong_code(self):
        data = {'code': '1111'}
        response = self.client.post(reverse('login', kwargs=self.kwargs), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReferalGetTest(APITestCase):
    def setUp(self):
        self.user = User.create_random_user()
        self.user_0 = User.create_random_user()
        self.user_2 = User.create_random_user()
        self.user_3 = User.create_random_user()
        Referal.objects.create(parent_user=self.user_0, child_user=self.user)
        Referal.objects.create(parent_user=self.user, child_user=self.user_2)
        Referal.objects.create(parent_user=self.user, child_user=self.user_3)
        self.client.force_login(user=self.user)

    def test_get_wrong(self):
        response = self.client.get(reverse('referals', kwargs={'type': 'dumb'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_parent(self):
        response = self.client.get(reverse('referals', kwargs={'type': 'parent'}))
        serializer = UserPhoneSerializer(self.user_0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_children(self):
        response = self.client.get(reverse('referals', kwargs={'type': 'children'}))
        serializer_2 = UserPhoneSerializer(self.user_2)
        serializer_3 = UserPhoneSerializer(self.user_3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn(serializer_2.data, response.data)
        self.assertIn(serializer_3.data, response.data)


class ReferalPostTest(APITestCase):
    def setUp(self):
        self.user_0 = User.create_random_user()
        self.user_1 = User.create_random_user()
        self.client.force_login(user=self.user_1)

    def test_post_activate_201(self):
        data = {'invite_code': self.user_0.user_ref}
        serializer = UserPhoneSerializer(self.user_0)
        response = self.client.post(reverse('referals', kwargs={'type': 'activate'}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_post_activate_404(self):
        data = {'invite_code': CodeGenerator.get_chars()}
        response = self.client.post(reverse('referals', kwargs={'type': 'activate'}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_wrong(self):
        response = self.client.post(reverse('referals', kwargs={'type': 'dumb'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

