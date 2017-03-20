from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

from silk import settings as s2
urlpatterns = [
    url(r'^$',views.index, name='index'),
    # all projects
    url(r'^projects', views.projects, name='projects'),
    # all suites in a bulletted list
    url(r'^suites', views.suites, name='suites'),
    # each suite
    url(r'^suitedetail/(?P<suite_id>[0-9]+)/$', views.suitedetail, name='suitedetail'),
    # all applications in a bulleted list
    url(r'^applications',views.applications, name='applications'),
    # each applicaiton
    url(r'^appdetail/(?P<application_id>[0-9]+)/$', views.appdetail, name='appdetail'),
    # all sites in a bulleted list
    url(r'^sites',views.sites, name='sites'),
    # each site
    url(r'^sitedetail/(?P<site_id>[0-9]+)/$', views.sitedetail, name='sitedetail'),
    # all applications in detailed form
    url(r'^allappdetail',views.allappdetail, name='allappdetail'),
    # all database type
    url(r'^dispositions',views.dispositiontypes, name='dispositions'),
    # all approles
    url(r'^approles', views.approles, name='approles'),
    # all serverroles
    url(r'^serverroles', views.serverroles, name='serverroles'),
    # all databasetypes
    url(r'^databasetypes', views.databasetypes, name='databasetypes'),
    # all hardware types
    url(r'^hardwaretypes', views.hardwaretypes, name='hardwaretypes'),
    # all application roles
    url(r'^approles', views.approles, name='approles'),
    # all regulatory types
    url(r'^regulatory', views.regulatory, name='regulatory'),
    # all authentication types
    url(r'^authtypes', views.authtypes, name='authtypes'),
    # all service accounts
    url(r'^serviceaccounts', views.serviceaccounts, name='serviceaccounts'),
    # all tech contacts
    url(r'^techcontacts', views.techcontacts, name='techcontacts'),
    # all business contacts
    url(r'^BusinessOwnerContacts', views.BusinessOwnerContacts, name='BusinessOwnerContacts'),
    # all end user contacts
    url(r'^endusercontacts', views.endusercontacts, name='endusercontacts'),
    # all application types
    url(r'^applicationtypes', views.applicationtypes, name='applicationtypes'),
    #all vendors
    url(r'^vendors', views.vendors, name='vendors'),
    # all project leads
    url(r'^projectleads', views.projectleads, name='projectleads'),
    #core application mapping
    url(r'^coreapplicationmapping', views.coreapplicationmapping, name='coreapplicationmapping'),
    #project gantt
    url(r'^projectgantt', views.projectgantt, name='projectgantt'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
