from django.test import TestCase
from author.models import Author

from rest_framework.test import APIClient


# Create your tests here.

class AuthorTest(TestCase):
    def test_create_author(self):
        Author.objects.all().delete()
        author = Author.objects.create_user(username="Test", password="testpassword")
        self.assertTrue(Author.objects.filter(username=author.username))

        return


    def test_create_superuser(self):
        Author.objects.all().delete()
        author = Author.objects.create_user(username='Test Author', password='testpassw0rd')
        self.assertTrue(author.is_staff)
        self.assertTrue(author.is_active)

    def test_author_str_(self):
            test_username = 'Test'
            Author.objects.all().delete()
            author = Author.objects.create_user(username="Test", password='testauthorpassw0rd')
            self.assertEqual(str(author.username), test_username)


