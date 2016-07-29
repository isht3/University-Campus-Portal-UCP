from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from login.api import UserViewSet, UserPasswordViewSet
from login.views import Login
from discussion.api import DiscussionViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, base_name="Authentication")
router.register(r'password', UserPasswordViewSet, base_name="Passwords")
router.register(r'discussions', DiscussionViewSet, base_name="Discussions")

urlpatterns = []

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^user/', include('login.urls')),
    url(r'^discussions/', include('discussion.urls')),
    url(r'^news/', include('news_event.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^', Login.as_view()),
    url(r'^tinymce/',include('tinymce.urls')),
]
