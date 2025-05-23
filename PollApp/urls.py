"""
URL configuration for PollApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views, settings

urlpatterns = [
       path('schema/', SpectacularAPIView.as_view(), name='schema'),
       path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
       path('admin/', admin.site.urls),
       path('tinymce/', include('tinymce.urls')),
       path('', views.HomePageView.as_view(), name='home'),
       path('account/', include('account.urls')),
       path('polls/', include('polls.urls')),
       path('poll_api/', include('poll_api.urls')),

]

urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
