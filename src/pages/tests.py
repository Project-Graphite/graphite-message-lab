from django.test import TestCase


class ViewTests(TestCase):
    def test_home_page(self):
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin sign in")
        self.assertContains(response, "Private")
