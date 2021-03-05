from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from core.viewsets import BaseModelViewSet
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.filters import OrderingFilter, SearchFilter


class PostViewSet(BaseModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "author__first_name", "author__last_name"]
    ordering = ["created"]
    ordering_fields = ["title", "author__username"]

    @action(methods=["POST"], detail=True, url_path="do_like")
    def like(self, request, *args, **kwargs):
        session = request.session.session_key
        # TODO зробити Like з використання session_key або IP адрес клієнта
        return Response("")

    #TODO підключити django-filter, зробити фільтрування постів, коментарів
    # підключити drf_yasg
    # cтворювати пост і т.д.
    # для коментарів permission клас, який дозволить неавторизованим


class CommentViewSet(NestedViewSetMixin, BaseModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        if kwargs.get("data"):
            kwargs["data"].update(self.get_parents_query_dict())
        return super(CommentViewSet, self).get_serializer(*args, **kwargs)
