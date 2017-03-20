from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from .models import Suite, Application, Site, DatabaseType, DispositionType, ApplicationRole, \
    ServerRole, Server, HardwareType, TechnicalOwnerContact, EndUserContact, BusinessOwnerContact, ServiceAccount, \
    RegulatoryType, AuthenticationType, Project, ApplicationType, Vendor, ProjectLead, RiskEntry
import pdfkit
from django.core.urlresolvers import resolve
from xhtml2pdf import pisa
import matplotlib
matplotlib.use('Agg')
from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg
import datetime
import mpld3
import json
import pandas
import numpy
import random

def index(request):
    context={}
    template = loader.get_template('silkollect/index.html')
    return HttpResponse(template.render(context, request))

def suitedetail(request, suite_id):
    selectedsuite = get_object_or_404(Suite, id=suite_id)
    all_apps = Application.objects.filter(Suite_id = suite_id)
    context = {
        'selectedsuite' : selectedsuite,
        'allapps' : all_apps
    }
    return render(request, 'silkollect/suitedetail.html', context)

def showappfilter(request, filterset, filtersettitle, filterkey):
    context = {
        'filterset' : filterset,
        'filterkey' : filterkey,
        'filtersettitle' : filtersettitle
    }
    return render(request, 'silkollect/appfilter.html', context)

def applications(request):
    dispositiontype = request.GET.get('dispositiontype', False)
    applicationtype = request.GET.get('applicationtype', False)
    approle = request.GET.get('applicationrole', False)
    site = request.GET.get('site',False)
    suite = request.GET.get('suite', False)
    serverrole = request.GET.get('serverrole',False)
    databasetype = request.GET.get('databasetype',False)
    hardwaretype = request.GET.get('hardwaretype', False)
    regulatorytype = request.GET.get('regulatorytype', False)
    authtype = request.GET.get('authenticationtype', False)
    serviceaccount = request.GET.get('serviceaccount')
    techcontact = request.GET.get('TechnicalOwnerContact')
    BusinessOwnerContact = request.GET.get('BusinessOwnerContact')
    endusercontact = request.GET.get('endusercontact')
    project = request.GET.get('project')
    vendor = request.GET.get('vendor')
    projectlead = request.GET.get('projectlead')
    filtertitle = '(no filter)'
    if applicationtype:
        id = ApplicationType.objects.filter(Name = applicationtype)
        all_apps = Application.objects.filter(ApplicationType = id)
        if applicationtype == 'NONE':
            all_apps = Application.objects.filter(ApplicationType = None).order_by('Name')
        filtertitle = 'Application Type: ' + applicationtype
    elif dispositiontype:
        id = DispositionType.objects.filter(Name = dispositiontype)
        all_apps = Application.objects.filter(DispositionType = id)
        if dispositiontype == 'NONE':
            all_apps = Application.objects.filter(DispositionType = None).order_by('Name')
        filtertitle = 'Application Disposition: ' + dispositiontype
    elif vendor:
        id = Vendor.objects.filter(Name = vendor)
        all_apps = Application.objects.filter(Vendor = id)
        if vendor == 'NONE':
            all_apps = Application.objects.filter(Vendor = None).order_by('Name')
        filtertitle = 'Vendor: ' + vendor
    elif approle:
        id = ApplicationRole.objects.filter(Name = approle)
        all_apps = Application.objects.filter(ApplicationRole = id)
        if approle == 'NONE':
            all_apps = Application.objects.filter(ApplicationRole = None).order_by('Name')
        filtertitle = 'Application Role: ' + approle
    elif site:
        id = Site.objects.filter(Name = site)
        all_apps = Application.objects.filter(Site = id)
        if site == 'NONE':
            all_apps = Application.objects.filter(Site = None).order_by('Name')
        filtertitle = 'Site: ' + site
    elif suite:
        id = Suite.objects.filter(Name = suite)
        all_apps = Application.objects.filter(Suite = id)
        if suite == 'NONE':
            all_apps = Application.objects.filter(Suite = None).order_by('Name')
        filtertitle = 'Suite: ' + suite
    elif serverrole:
        serverid = Server.objects.filter(ShortDescription = serverrole)
        all_apps = Application.objects.filter(ServerRoles__Server_id = serverid)
        if serverrole == 'NONE':
            all_apps = Application.objects.filter(ServerRoles__Server_id = None).order_by('Name')
        filtertitle = 'ServerRole: ' + serverrole
    elif databasetype:
        #id = ServerRole.objects.filter(DatabaseType__Name = databasetype)
        all_apps = Application.objects.filter(ServerRoles__DatabaseType__Name = databasetype).distinct()
        filtertitle = 'DatabaseType: ' + databasetype
    elif hardwaretype:
        all_apps = Application.objects.filter(ServerRoles__Server__HardwareType__Name = hardwaretype).distinct()
        filtertitle = 'HardwareType: ' + hardwaretype
    elif regulatorytype:
        all_apps = Application.objects.filter(RegulatoryType__Name = regulatorytype).distinct()
        filtertitle = 'Regulatory Type: ' + regulatorytype
    elif authtype:
        all_apps = Application.objects.filter(AuthenticationType__Name = authtype).distinct()
        filtertitle = 'Auth Type: ' + authtype
    elif serviceaccount:
        all_apps = Application.objects.filter(ServiceAccounts__Name = serviceaccount).distinct()
        filtertitle = 'Service Account: ' + serviceaccount
    elif techcontact:
        all_apps = Application.objects.filter(TechnicalOwnerContacts__Contact__Name = techcontact).distinct()
        if techcontact == 'NONE':
            all_apps = Application.objects.filter(TechnicalOwnerContacts__Contact__Name = None).order_by('Name')
        filtertitle = 'Technical Contact: ' + techcontact
    elif BusinessOwnerContact:
        all_apps = Application.objects.filter(BusinessOwnerContacts__Contact__Name = BusinessOwnerContact).distinct()
        if BusinessOwnerContact == 'NONE':
            all_apps = Application.objects.filter(BusinessOwnerContacts__Contact__Name = None).order_by('Name')
        filtertitle = 'Business Contact: ' + BusinessOwnerContact
    elif endusercontact:
        all_apps = Application.objects.filter(EndUserContacts__Contact__Name = endusercontact).distinct()
        if endusercontact == 'NONE':
            all_apps = Application.objects.filter(EndUserContacts__Contact__Name = None).order_by('Name')
        filtertitle = 'End User Contact: ' + endusercontact
    elif projectlead:
        all_apps = Application.objects.filter(ProjectLeads__Contact__Name = projectlead).distinct()
        if projectlead == 'NONE':
            all_apps = Application.objects.filter(ProjectLeads__Contact__Name = None).order_by('Name')
        filtertitle = 'Project Lead Contact: ' + projectlead
    elif project:
        all_apps = Application.objects.filter(Project__Name = project).distinct()
        if project == 'NONE':
            all_apps = Application.objects.filter(Project__Name = None).order_by('Name')
        filtertitle = 'Project: ' + project
    else:
        all_apps = Application.objects.all().order_by('Name')
    request.session['allapps'] = all_apps
    request.session['filtertitle'] = filtertitle
    context = {
        'allapps' : all_apps,
        'filtertitle' : filtertitle
    }
    return render(request, 'silkollect/applications.html', context)

def allappdetail(request):
    allapps = request.session['allapps']
    filtertitle = 'No Filter'
    if 'filtertitle' in request.session:
        filtertitle = request.session['filtertitle']
    if allapps == None:
        allapps = Application.objects.all().order_by('Name')
    context = {
        'allapps' : allapps,
        'filtertitle' : filtertitle
    }
    printvar = request.GET.get('print',False)
    #http://stackoverflow.com/questions/23767073/how-can-i-convert-a-html-page-to-pdf-using-django
    if printvar and printvar.upper() == 'TRUE':
        resultFile = open('applications.pdf', 'w+b')
        #pisastatus = pisa.CreatePDF(
        #    render(request, 'silkollect/allappdetail.html', context),
        #    dest = resultFile)
	pisastatus = pisa.CreatePDF(
		render(request,'silkollect/allappdetail.html', context).content, 
		dest=resultFile)
        resultFile.seek(0)
        pdf = resultFile.read()
        resultFile.close()
        return HttpResponse(pdf, 'application/pdf')
    return render(request, 'silkollect/allappdetail.html', context)

def appdetail(request, application_id):
    selectedapp = get_object_or_404(Application, id=application_id)
    context = {
        'selectedapp' : selectedapp
    }
    return render(request, 'silkollect/appdetail.html', context)

def sitedetail(request, site_id):
    selectedsite = get_object_or_404(Site, id=site_id)
    all_apps = Application.objects.filter(Site_id = site_id).order_by('Name')
    all_suites = Suite.objects.filter(Site_id = site_id).order_by('Name')
    context = {
        'selectedsite' : selectedsite,
        'allapps' : all_apps,
        'allsuites' : all_suites,
    }
    return render(request, 'silkollect/sitedetail.html', context)
def projectgantt(request):

    def create_date(month, day,  year):
        date = datetime.datetime(int(year), int(month), int(day))
        return matplotlib.dates.date2num(date)

    allprojects = Project.objects.all().order_by('Name')
    ylabels = []
    customDates = []

    ylabels.append('Project 1')
    ylabels.append('Project 2')
    ylabels.append('Project 3')
    customDates.append([create_date(12,17,2016), create_date(5,3,2017)])
    customDates.append([create_date(5,13,2017),create_date(10,13,2017)])
    customDates.append([create_date(1, 13, 2016), create_date(1, 13, 2017)])

    #for tx in textlist:
     #   if not tx.startswith('#'):
      #      ylabel, startdate, enddate = tx.split(',')
       #     ylabels.append(ylabel.replace('\n', ''))
        #    customDates.append([_create_date(startdate.replace('\n', '')), _create_date(enddate.replace('\n', ''))])

    ilen = len(ylabels)
    pos = numpy.arange(0.5, ilen * 0.5 + 0.5, 0.5)

    task_dates = {}
    for i, task in enumerate(ylabels):
        task_dates[task] = customDates[i]

    fig = matplotlib.pyplot.figure(figsize=(20, 8))
    ax = fig.add_subplot(111)

    for i in range(len(ylabels)):
        start_date, end_date = task_dates[ylabels[i]]
        ax.barh((i * 0.5) + 0.5, end_date - start_date, left=start_date, height=0.3, align='center',
                edgecolor='lightgreen', color='orange', alpha=0.8)
        #ax.text(0,0,ylabels[i], ha='center')
        #ax.set_yticklabels(ylabels[i])

    #matplotlib.pyplot.ylabel('blah', fontsize=14)
    #matplotlib.pyplot.yticks(ylabels)
    #locsy, labelsy = matplotlib.pyplot.yticks(numpy.arange(2), ("test", "test2"))


    #locsy, labelsy = matplotlib.pyplot.yticks(pos, ylabels)
    #matplotlib.pyplot.setp(labelsy, fontsize=14)
    #matplotlib.pyplot.ylim(0,len(ylabels) + 1)

    #matplotlib.pyplot.yticks(("bruce", "elroy", "mack"))

    ax.set_yticks((1, 2, 3))
    #ax.set_yticklabels(("bruce", "elroy", "mack"))

    #ax.tick_params(reset=True)
    #fig.set_yticks(pos, ylabels)
    #matplotlib.pyplot.yticks(pos, ylabels)
    #matplotlib.pyplot.yticks(range(3), ylabels, rotation=45)

    #ax.set_yticks(pos)
    #ax.set_yticklabels(labelsy)

    #locsy, labelsy = matplotlib.pyplot.yticks(pos, ("Blah", "Test", "book"))


    #    ax.axis('tight')
#    ax.set_ylim(ymin=-0.1, ymax=ilen * 0.5 + 0.5)
#    ax.grid(color='g', linestyle=':')
#    ax.xaxis_date()
#    rule = matplotlib.dates.rrulewrapper(matplotlib.dates.WEEKLY, interval=1)
#    loc = matplotlib.dates.RRuleLocator(rule)
    # formatter = DateFormatter("%d-%b '%y")
#    formatter = matplotlib.dates.DateFormatter("%d-%b")

#    ax.xaxis.set_major_locator(loc)
#    ax.xaxis.set_major_formatter(formatter)
#    labelsx = ax.get_xticklabels()
#    matplotlib.pyplot.setp(labelsx, rotation=30, fontsize=10)

#    font = matplotlib.font_manager.FontProperties(size='small')
#    ax.legend(loc=1, prop=font)

    ax.invert_yaxis()
    fig.autofmt_xdate()
    #plt.savefig('gantt.svg')
    #plt.show()
    js = json.dumps(mpld3.fig_to_dict(fig))
    context = {
        "theFig": js,
        "allprojects": allprojects,
    }
    return render(request, 'silkollect/projectgantt.html', context)

def projectganttOLD(request):
    def create_date(month, day,  year):
        date = datetime.datetime(int(year), int(month), 1)
        return matplotlib.dates.date2num(date)
#    camapps = Application.objects.exclude(business_value=None).exclude(technical_integrity=None)
    allprojects = Project.objects.all().order_by('Name')
    matplotlib.pyplot.rcParams["figure.figsize"] = [10, 10]
    #pos = numpy.arange(0.5, 5.5, 0.5)
    pos = numpy.arange(0.5, len(allprojects), 0.5)

#    fig, ax = matplotlib.pyplot.subplots()
#    xaxis = []
#    yaxis = []
#    labels = []
#    apptypecolors = {}
#    colors = []
#    ranwindow = 0.12
#    for app in camapps:
#        x = random.uniform(app.business_value - ranwindow, app.business_value + ranwindow)
#        y = random.uniform(app.technical_integrity - ranwindow, app.technical_integrity + ranwindow)
#        xaxis.append(x)
#        yaxis.append(y)
#        label = app.Name
#        labels.append(label)
#        if app.ApplicationType not in apptypecolors:
#            apptypecolors[app.ApplicationType] = random.randint(1, 2)
#        colors.append(apptypecolors[app.ApplicationType])

#    N = len(xaxis)
#    colormap = numpy.array(['r', 'g', 'b'])
#    area = 40
#    scatter = ax.scatter(xaxis, yaxis, alpha=0.4, s=area)  # , c=colormap[colors] )
#    matplotlib.pyplot.ylabel('Technical Integrity')
#    matplotlib.pyplot.xlabel('Business Value')
#    ax.axis([0, 6, 0, 6])

    # http://stackoverflow.com/questions/16947151/vertical-line-not-respecting-min-max-limits-matplotlib
    # axvline uses axes coordinate system, vs. vlines uses data coordinate system.
    # ax.axhline(y=3, xmin=0, xmax=6)
    # matplotlib.pyplot.hlines(y=3, xmin=0, xmax=6, linewidth=2, color='red')
    # matplotlib.pyplot.vlines(x=3, ymin=0, ymax=6, linewidth=2, color='red')
#    matplotlib.pyplot.text(1, 5, 'Tolerate', fontsize=22, color='red')
#    matplotlib.pyplot.text(4, 5, 'Invest', fontsize=22, color='red')
#    matplotlib.pyplot.text(1, 1.5, 'Eliminate', fontsize=22, color='red')
#    matplotlib.pyplot.text(4, 1.5, 'Migrate', fontsize=22, color='red')

#    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
#    mpld3.plugins.connect(fig, tooltip)

    ylabels = []
    #for p in allprojects:
    #    ylabels.append(p.Name)
    ylabels.append('Test1')
    #ylabels.append('Test2')

    #effort = []
    #effort.append([0.2, 1.0])

    customdates = []
    customdates.append([create_date(12, 2016), create_date(4, 2017)])
#    customdates.append([create_date(10, 2016), create_date(9, 2017)])
    task_dates = {}
    for i, task in enumerate(ylabels):
        task_dates[task] = customdates[i]

    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(111)

    start_date, end_date = task_dates[ylabels[0]]
    ax.barh(0.5, end_date - start_date, left=start_date, height=0.3, align='center', color='blue', alpha=0.75)


    #ax.barh(0.45, (end_date - start_date) * effort[0][0], left=start_date, height=0.1, align='center', color='red',
    #        alpha=0.75, label="PI Effort")
    #ax.barh(0.55, (end_date - start_date) * effort[0][1], left=start_date, height=0.1, align='center', color='yellow',
    #        alpha=0.75, label="Student Effort")


#    for i in range(0, len(ylabels) - 1):
        #labels = ['Analysis', 'Reporting'] if i == 1 else [None, None]
 #       start_date, mid_date, end_date = task_dates[ylabels[i + 1]]
  #      #piEffort, studentEffort = effort[i + 1]
   #     ax.barh((i * 0.5) + 1.0, mid_date - start_date, left=start_date, height=0.3, align='center', color='blue',
    #        alpha=0.75)
#        ax.barh((i * 0.5) + 1.0 - 0.05, (mid_date - start_date) * piEffort, left=start_date, height=0.1, align='center',
 #               color='red', alpha=0.75)
  ##         align='center', color='yellow', alpha=0.75)

    # Format the y-axis

    locsy, labelsy = matplotlib.pyplot.yticks(pos, ylabels)
    matplotlib.pyplot.setp(labelsy, fontsize=14)

    # Format the x-axis

    ax.axis('tight')
    ax.set_ylim(ymin=-0.1, ymax=4.5)
    ax.grid(color='g', linestyle=':')

    ax.xaxis_date()  # Tell matplotlib that these are dates...

    rule = matplotlib.dates.rrulewrapper(matplotlib.dates.MONTHLY, interval=1)
    loc = matplotlib.dates.RRuleLocator(rule)
    formatter = matplotlib.dates.DateFormatter("%b '%y")

    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    labelsx = ax.get_xticklabels()
    matplotlib.pyplot.setp(labelsx, rotation=30, fontsize=12)

    # Format the legend

    font = matplotlib.font_manager.FontProperties(size='small')
    ax.legend(loc=1, prop=font)

    # Finish up
    ax.invert_yaxis()
    fig.autofmt_xdate()
    # plt.savefig('gantt.svg')
    #plt.show()




    js = json.dumps(mpld3.fig_to_dict(fig))
    context = {
        "theFig": js,
        "allprojects": allprojects,
    }
    return render(request, 'silkollect/projectgantt.html', context)

def coreapplicationmapping(request):
    class coreapp():
        AppName = None
        SuiteName = None
        ID = None
        SuiteID = None
        TechnicalIntegrity = None
        TechnicalIntegrityName = None
        BusinessValue = None
        BusinessValueName = None
        RiskEntry = None
        #RiskEntryID = None
    coreapps = []
    camapps = Application.objects.exclude(business_value = None).exclude(technical_integrity = None)
    allapps = Application.objects.all().order_by('Name')
    allrisks = RiskEntry.objects.all()
    for app in allapps:
        ca = coreapp()
        ca.AppName = app.Name
        ca.ID = app.id
        if app.Suite != None:
            ca.SuiteName = app.Suite.Name
            ca.SuiteID = app.Suite.id
        else:
            ca.SuiteName = ""
        if app.technical_integrity != None:
            ca.TechnicalIntegrityName = dict(Application.Value_Choices)[app.technical_integrity]
            ca.TechnicalIntegrity = app.technical_integrity
        if app.business_value != None:
            ca.BusinessValueName = dict(Application.Value_Choices)[app.business_value]
            ca.BusinessValue = app.business_value
        ca.RiskEntry = ""
        for risk in allrisks:
            if app in risk.Applications.all():
                if ca.RiskEntry == "":
                    ca.RiskEntry = risk.Name
                else:
                    ca.RiskEntry = ca.RiskEntry + ", " + risk.Name

        coreapps.append(ca)
    matplotlib.pyplot.rcParams["figure.figsize"] = [10,10]
    fig, ax = matplotlib.pyplot.subplots()
    xaxis = []
    yaxis = []
    labels = []
    apptypecolors = {}
    colors = []
    ranwindow = 0.12
    for app in camapps:
        x = random.uniform(app.business_value - ranwindow, app.business_value + ranwindow)
        y = random.uniform(app.technical_integrity - ranwindow, app.technical_integrity + ranwindow)
        xaxis.append(x)
        yaxis.append(y)
        label = app.Name
        labels.append(label)
        if app.ApplicationType not in apptypecolors:
            apptypecolors[app.ApplicationType] = random.randint(1,2)
        colors.append(apptypecolors[app.ApplicationType])


    N = len(xaxis)
    #colors = numpy.random.rand(N)
    #area = numpy.pi * (15 * numpy.random.rand(N)) ** 2
    #print colors
    colormap = numpy.array(['r', 'g', 'b'])
    area = 40
    scatter = ax.scatter(xaxis, yaxis, alpha = 0.4, s=area)#, c=colormap[colors] )
    matplotlib.pyplot.ylabel('Technical Integrity')
    matplotlib.pyplot.xlabel('Business Value')
    ax.axis([0,6,0,6])
#http://stackoverflow.com/questions/16947151/vertical-line-not-respecting-min-max-limits-matplotlib
# axvline uses axes coordinate system, vs. vlines uses data coordinate system.
    #ax.axhline(y=3, xmin=0, xmax=6)
    #matplotlib.pyplot.hlines(y=3, xmin=0, xmax=6, linewidth=2, color='red')
    #matplotlib.pyplot.vlines(x=3, ymin=0, ymax=6, linewidth=2, color='red')
    matplotlib.pyplot.text(1,5,'Tolerate', fontsize=22, color='red')
    matplotlib.pyplot.text(4,5,'Invest', fontsize=22, color='red')
    matplotlib.pyplot.text(1,1.5,'Eliminate', fontsize=22, color='red')
    matplotlib.pyplot.text(4,1.5,'Migrate', fontsize=22, color='red')

    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels = labels)
    mpld3.plugins.connect(fig, tooltip)

    js = json.dumps(mpld3.fig_to_dict(fig))
    context = {
        "theFig" : js,
        #"apps" : camapps,
        #"allapps" : allapps,
        #"riskentries" : allrisks,
        "coreapps" : coreapps
    }
    return render(request, 'silkollect/camplot.html', context)

# GENERIC WAY, using "appfilter" template.
def dispositiontypes(request):
    return showappfilter(
        request,
        DispositionType.objects.all().order_by('Name'),
        'Disposition Types',
        'dispositiontype')

def applicationtypes(request):
    return showappfilter(
        request,
        ApplicationType.objects.all().order_by('Name'),
        'Application Types',
        'applicationtype')

def approles(request):
    return showappfilter(
        request,
        ApplicationRole.objects.all().order_by('Name'),
        'Application Roles',
        'applicationrole')

def sites(request):
    return showappfilter(
        request,
        Site.objects.all().order_by('Name'),
        'Sites',
        'site')

def suites(request):
    return showappfilter(
        request,
        Suite.objects.all().order_by('Name'),
        'Suites',
        'suite')

def serverroles(request):
    return showappfilter(
        request,
        ServerRole.objects.all().order_by('Server__ShortDescription'),
        'Server Role',
        'serverrole')

def databasetypes(request):
    return showappfilter(
        request,
        DatabaseType.objects.all().order_by('Name'),
        'Database Types',
        'databasetype')

def hardwaretypes(request):
    return showappfilter(
        request,
        HardwareType.objects.all().order_by('Name'),
        'Hardware Types',
        'hardwaretype')

def regulatory(request):
    return showappfilter(
        request,
        RegulatoryType.objects.all().order_by('Name'),
        'Regulatory Types',
        'regulatorytype')

def authtypes(request):
    return showappfilter(
        request,
        AuthenticationType.objects.all().order_by('Name'),
        'Authentication Types',
        'authenticationtype')

def serviceaccounts(request):
    return showappfilter(
        request,
        ServiceAccount.objects.all().order_by('Name'),
        'Service Accounts',
        'serviceaccount')

def techcontacts(request):
    return showappfilter(
        request,
        TechnicalOwnerContact.objects.all().order_by('Contact__Name'),
        'Technical Contacts',
        'TechnicalOwnerContact')

def BusinessOwnerContacts(request):
    return showappfilter(
        request,
        BusinessOwnerContact.objects.all().order_by('Contact__Name'),
        'Business Contacts',
        'BusinessOwnerContact')

def endusercontacts(request):
    return showappfilter(
        request,
        EndUserContact.objects.all().order_by('Contact__Name'),
        'End User Contacts',
        'endusercontact')

def projectleads(request):
    return showappfilter(
        request,
        ProjectLead.objects.all().order_by('Contact__Name'),
        'Project Leads',
        'projectlead'
    )

def projects(request):
    return showappfilter(
        request,
        Project.objects.all().order_by('Name'),
        'Projects',
        'project')

def vendors(request):
    return showappfilter(
        request,
        Vendor.objects.all().order_by('Name'),
        'Vendors',
        'vendor'
    )

