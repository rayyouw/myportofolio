from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Award


class AwardAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="award-owner",
            password="owner-password",
            email="owner@example.com",
        )
        self.regular = User.objects.create_user(
            username="award-regular",
            password="regular-password",
        )
        self.editor = User.objects.create_user(
            username="award-editor",
            password="editor-password",
        )
        editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(editor_group)
        Award.objects.all().delete()
        self.award = Award.objects.create(
            title="Portfolio Award",
            description="A competition result",
        )
        self.list_url = reverse("api:award-list")
        self.detail_url = reverse("api:award-detail", args=[self.award.pk])
        self.star_url = reverse("api:award-star", args=[self.award.pk])
        self.payload = {
            "title": "New Award",
            "description": "A new achievement",
            "thumbnail": "https://example.com/award.png",
        }

    def test_public_list_detail_and_search(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.award.pk)
        self.assertFalse(response.data[0]["is_starred"])
        self.assertEqual(
            self.client.get(self.detail_url).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.get(self.list_url, {"title": "missing"}).data,
            [],
        )

    def test_missing_award_returns_404(self):
        url = reverse("api:award-detail", args=[999999])
        self.assertEqual(
            self.client.get(url).status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_visitors_and_regular_users_cannot_write(self):
        for user in (None, self.regular):
            self.client.force_authenticate(user=user)
            self.assertEqual(
                self.client.post(
                    self.list_url, self.payload, format="json",
                ).status_code,
                status.HTTP_403_FORBIDDEN,
            )
            self.assertEqual(
                self.client.patch(
                    self.detail_url, {"title": "Changed"}, format="json",
                ).status_code,
                status.HTTP_403_FORBIDDEN,
            )
            self.assertEqual(
                self.client.delete(self.detail_url).status_code,
                status.HTTP_403_FORBIDDEN,
            )
        self.assertEqual(Award.objects.count(), 1)
        self.award.refresh_from_db()
        self.assertEqual(self.award.title, "Portfolio Award")

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(
            self.detail_url, {"title": "Edited Award"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.award.refresh_from_db()
        self.assertEqual(self.award.title, "Edited Award")

        response = self.client.post(
            self.list_url, self.payload, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Award.objects.filter(pk=self.award.pk).exists())

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url, self.payload, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_id = response.data["id"]
        response = self.client.put(
            reverse("api:award-detail", args=[created_id]),
            self.payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(
            reverse("api:award-detail", args=[created_id]),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Award.objects.filter(pk=created_id).exists())

    def test_serializer_validation_rejects_html_and_blank_text(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
        ]:
            response = self.client.post(
                self.list_url,
                {**self.payload, **changes},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        response = self.client.post(
            self.list_url,
            {**self.payload, "title": "<b>Safe title</b>", "description": "<i>Safe description</i>"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Safe title")
        self.assertEqual(response.data["description"], "Safe description")
        self.assertEqual(Award.objects.count(), 2)

    def test_star_requires_login_and_toggles_for_regular_user(self):
        self.assertEqual(
            self.client.post(self.star_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.client.force_authenticate(user=self.regular)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_session_authentication_requires_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(
            username="award-owner",
            password="owner-password",
        ))
        response = client.post(
            self.list_url, self.payload, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Award.objects.count(), 1)
