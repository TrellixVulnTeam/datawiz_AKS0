from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Like
from django.db.models import Count

#admin.site.register(Post)
#admin.site.register(Comment)
admin.site.register(Like)


#коменти під постами
class CommentAdminModelInline(admin.TabularInline):
    model = Comment
    # скільки пустих виводити
    extra = 1


class LikeAdminModelInline(admin.TabularInline):
    model = Like
    extra = 1

    # заборонити міняти
    #def has_change_permission(self, request, obj=None) -> bool:
    #    return False

    # заборонити добавляти
    #def has_add_permission(self, request, obj) -> bool:
    #    return False


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    # коменти під постами
    inlines = [CommentAdminModelInline, LikeAdminModelInline]
    # поля, які бачимо при перегляді всіх Постів
    list_display = ('title', 'slug', 'created', 'user_name', 'likes_count')
    # автоматичне заповнення слагу
    prepopulated_fields = {'slug': ('title', )}
    # сортування
    ordering = ("-created",)
    #фільтри
    list_filter = ('status', 'created')

    # щоб одним запросом забрати всі коменти для поста
    # зменшує кількість запитів, оптимізує
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs.prefetch_related('comments')
            .select_related('author')
            .annotate(likes_count=Count('likes'))
        )

    # вивід свого додаткового поля в list_display
    def user_name(self, obj):
        return obj.author.username

    # вивести кількість лайків
    def likes_count(self, obj):
        return obj.likes_count


@admin.register(Comment)
class CommentAdminModel(admin.ModelAdmin):
    list_display = ('post', 'author', 'created')
    ordering = ("-created", )
    list_filter = ('created', 'post')
