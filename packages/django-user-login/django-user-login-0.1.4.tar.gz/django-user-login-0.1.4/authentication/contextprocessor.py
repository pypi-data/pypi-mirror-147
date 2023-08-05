from django.conf import settings

def site_title(request):
    return {
        "sitetitle": settings.SITE_TITLE,
        "FAVICON_URL": settings.FAVICON_URL
    }