from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class ToolsViewTest(TestCase):
    def test_tool(self):
        url = reverse("app:tools")
        response = self.client.get(url)
        print(response.status_code)