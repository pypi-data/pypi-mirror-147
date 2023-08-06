====================
Package Description
====================

**Django easy blog** post is a package that allows you to create blog posts
with a text editor to customize the content of your publication.

Quick Start
============
1. Add **post** in your INSTALLED_APPS and update settings

.. code:: bash

    INSTALLED_APPS = [
    ...
    'ckeditor',
    'ckeditor_uploader',
    'post',
    ] 
    
    CKEDITOR_UPLOAD_PATH = "uploads/"
    ...
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static'
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    ...

2. update your project url

.. code:: bash

    from django.conf.urls.static import static
    from . import settings 
    from django.urls import path, include
    urlpatterns = [
    ...
    path('ckeditor', include('ckeditor_uploader.urls')),
    ] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

3. Install ckeditor and pillow

.. code:: bash

    pip install django-ckeditor pillow

4. Migrate your project and collect static

.. code:: bash

    python manage.py migrations post
    python manage.py migrate
    python manage.py collectstatic

5. Create super user, run your app and go to admin to create your blog post


6. Use **post_list** tag to get all posts list on your template
   
.. code:: html

    {% load post_tags %}
    <!DOCTYPE html>
    ... 
    <body>
        ...
	    <p>My blogs</p>
    	<div>
            {% for post in ''|post_list %}
                <h2>{{post.title}}</h2>
                <h2>{{post.content|safe}}</h2>
            {% endfor %}
    	</div>
        ...
    </body>

