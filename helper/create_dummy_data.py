from core.authors.models import Author
from core.blogs.models import Blog
from core.blogs.models import CoverImage

author_data = [
    {"name": "John Doe", "email": "john@email.com", "bio": "Python Blogger"},
    {"name": "Jane Doe", "email": "jane@email.com", "bio": "Django Blogger"},
]

blog_data = [
    {
        "title": "Python is cool",
        "content": "Python is cool",
        "author": "john@email.com",
        "cover_image": "https://ih1.redbubble.net/image.600658100.7460/flat,750x,075,f-pad,750x1000,f8f8f8.u1.jpg",
    },
    {
        "title": "Django for Everyone",
        "content": "Django for Everyone",
        "author": "jane@email.com",
        "cover_image": "https://automationpanda.com/wp-content/uploads/2017/09/django-logo-negative.png",
    },
    {
        "title": "Django vs. Flask",
        "content": "Django vs. Flask",
        "author": "jane@email.com",
        "cover_image": "https://flowygo.com/wp-content/uploads/2021/04/django_vs_flask-1.jpeg",
    },
]

cover_image = [
    {
        "image_link": "https://ih1.redbubble.net/image.600658100.7460/flat,750x,075,f-pad,750x1000,f8f8f8.u1.jpg",
    },
    {
        "image_link": "https://flowygo.com/wp-content/uploads/2021/04/django_vs_flask-1.jpeg",
    },
    {
        "image_link": "https://automationpanda.com/wp-content/uploads/2017/09/django-logo-negative.png",
    },
]

for author in author_data:
    Author.objects.get_or_create(email=author["email"], defaults={**author})

for image in cover_image:
    CoverImage.objects.get_or_create(image_link=image["image_link"], defaults={**image})

for blog in blog_data:
    author = Author.objects.get(email=blog["author"])
    cover_image = CoverImage.objects.get(image_link=blog["cover_image"])
    data = {**blog, "author": author, "cover_image": cover_image}
    Blog.objects.get_or_create(title=blog["title"], defaults={**data})
