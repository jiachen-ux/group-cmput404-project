# from django.test import TestCase
# from SocialDistribution.authors.models import Author
# from SocialDistribution.post.models import Post

# # Create your tests here.
# class PostViewTestCases(TestCase):
#      @classmethod
#      def setUpData(cls):
#         uuids = [
#             "e84c8098-c240-48c2-91d9-1d266a0cd371",
#             "e84c8098-c240-48c2-91d9-1d266a0cd372",
#         ]
#         authors = []
#         for index in range(len(uuids)):
#             authors.append(Author.objects.create(
#                 userId=uuids[index],
#                 username = "PostTestCase{}".format(index),
#                 display_name="Test object{}".format(index),
#                 url="https://cmput-404-social-distribution.herokuapp.com/author/{}".format(uuids[index]),
#                 host="https://cmput-404-social-distribution.herokuapp.com/",
#             ))
