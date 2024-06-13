import sys

from cacheops import cached
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from core.blogs.api.serializers import BlogSerializer
from core.blogs.models import Blog


def update_blog_title(request):
    if request.user.has_perm("blog.update_title"):
        # perform operation
        return HttpResponse("User has permission to update title")
    return HttpResponse("User does not have permission to update title")


def check_permission(user, group_name):
    return user.groups.filter(name=group_name).exists()


@api_view(["POST"])
def blog_view(request):
    if not check_permission(request.user, "can_view_blog"):
        return Response(status=403)
    sys.stdout.write("User has permission to view blog")
    return Response(status=200)


@cached(timeout=60 * 10)
def get_all_blogs(author_id):
    sys.stdout.write("Fetching blogs from database")
    blogs = Blog.objects.filter(author_id=author_id)
    return BlogSerializer(blogs, many=True).data


@api_view(["GET"])
def get_blogs_by_author(request):
    author_id = request.GET.get("author_id")
    blogs = get_all_blogs(author_id)
    return Response({"blogs": blogs})


# Throttling anonymous users.
class BlogApiView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        content = {"status": "request was permitted"}
        return Response(content)


class Blog2ApiView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "blog_limit"

    def get(self, request):
        content = {"status": "request was permitted"}
        return Response(content)


class BlogDetailApiView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "blog_limit"

    def get(self, request):
        content = {"status": "request was permitted"}
        return Response(content)


class Blog3ApiView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "blog_2_limit"

    def get(self, request):
        content = {"status": "request was permitted"}
        return Response(content)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
