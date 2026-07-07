from django.test import TestCase
from django.urls import reverse

from .models import User


class ProfileSessionTests(TestCase):
    def test_profile_page_uses_session_user_instead_of_latest_global_user(self):
        first_user = User.objects.create(full_name="Ali Valiyev", phone_number="998901111111")
        second_user = User.objects.create(full_name="Bobur Qodirov", phone_number="998902222222")

        session = self.client.session
        session["profile_user_id"] = first_user.id
        session.save()

        response = self.client.get(reverse("profile_user"))

        self.assertContains(response, first_user.full_name)
        self.assertNotContains(response, second_user.full_name)

    def test_registration_stores_current_user_in_session(self):
        response = self.client.post(
            reverse("api_register"),
            {"full_name": "Sardor", "phone_number": "998903333333"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get("profile_user_id"))
        saved_user = User.objects.get(phone_number="998903333333")
        self.assertEqual(self.client.session["profile_user_id"], saved_user.id)
