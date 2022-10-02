from django.urls import reverse
from rest_framework.test import APITestCase

from social_app.models import Post


class CreatePostRest(APITestCase):
    def setUp(self):
        """
        Populating Test DB user
        """
        self.user_data = {
            "first_name": "test",
            "last_name": "user1",
            "email": "test@user1.com",
            "password": "123456789",
        }
        self.sign_up_url = reverse("social_app:user_sign_up")
        self.client.post(self.sign_up_url, data=self.user_data)

        auth_url = reverse("social_app:token_obtain_pair")

        self.access_token = self.client.post(
            auth_url,
            {
                "email": self.user_data.get("email"),
                "password": self.user_data.get("password"),
            },
        ).data.get("access")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_post_valid(self):
        """
        Creating post - Valid
        """
        print(f"test_create_post_valid")
        data = {"title": "Test title", "description": "Test description"}

        self.url = reverse("social_app:create_post")
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("title"), data.get("title"))
        self.assertEqual(response.data.get("description"), data.get("description"))

        print("###################")

    def test_create_post_invalid(self):
        """
        Creating post - Invalid
        """
        print(f"test_create_post_invalid")
        user_detail_url = reverse("social_app:user_detail")
        user_id = self.client.get(user_detail_url).get("user_id")
        user_post_count = Post.objects.filter(user_id=user_id).count()
        self.assertEqual(user_post_count, 0)

        data = {"title": "", "description": "Test description"}

        self.url = reverse("social_app:create_post")
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 500)
        user_post_count = Post.objects.filter(user_id=user_id).count()
        self.assertEqual(user_post_count, 0)

        print("###################")
