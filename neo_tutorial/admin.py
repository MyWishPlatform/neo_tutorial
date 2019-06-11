from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.admin.apps import AdminConfig


class TutorialAdminSite(AdminSite):
    site_header = 'Admin panel'


class TutorialAdminConfig(AdminConfig):
    default_site = 'neo_tutorial.admin.TutorialAdminSite'
