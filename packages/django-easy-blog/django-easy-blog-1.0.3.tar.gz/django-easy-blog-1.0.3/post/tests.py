from unittest import TestCase

from django.template import Template, Context

from .models import Post


class PostTest(TestCase):
    def setUp(self):
        Post.objects.create(title='My first blog', content='My first blog content').save()

    def test_blog_list_tags_good(self):
        """
            Test if the custom tag returns the expected data
        """
        rendered = Template("{% load  post_tags %}" 
                            "{% for post in ''|post_list %} {{post}} {% endfor %}").render(Context({}))
        self.assertIn('My first blog', rendered)
