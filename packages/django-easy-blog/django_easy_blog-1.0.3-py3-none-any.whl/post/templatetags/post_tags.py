from django import template

from ..models import Post

register = template.Library()


@register.filter
def post_list(arg=None):
    all_post = Post.objects.all()
    return all_post
