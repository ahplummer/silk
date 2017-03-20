import argparse
import csv

def CSVExportApplicationsCAMPlot(allapps, csvwriter):
    from silkollect.models import ApplicationInterface
    # eliminateapps = Application.objects.filter(business_value < 3)
    csvwriter.writerow(['Name', 'Disposition', 'ApplicationCategory', 'ApplicationRole', 'AppType', 'Vendor', 'Suite',
                        'AuthenticationType', 'TechnicalOwners', 'BusinessOwners', 'ProjectLeads', 'EndUserContacts',
                        'BusinessUnit', 'BusinessValue', 'TechnicalIntegrity', 'ApplicationInterfaces'])
    # build up row.
    for app in allapps:
        intline = ''
        tocline = ''
        apptype = ''
        suite = ''
        busline = ''
        prldline = ''
        busval = ''
        tecint = ''
        unit = ''
        euline = ''
        if app.Suite is not None:
            suite = app.Suite
        if app.BusinessUnit is not None:
            unit = app.BusinessUnit
        if app.ApplicationType is not None:
            apptype = app.ApplicationType
        if app.business_value is not None:
            busval = app.business_value
        if app.technical_integrity is not None:
            tecint = app.technical_integrity
        for eu in app.EndUserContacts.all():
            if eu.Contact.UID is not None:
                if euline == '':
                    euline = eu.Contact.Name
                else:
                    euline += ',' + eu.Contact.Name
        for toc in app.TechnicalOwnerContacts.all():
            if toc.Contact.UID is not None:
                if tocline == '':
                    tocline = toc.Contact.Name
                else:
                    tocline += ',' + toc.Contact.Name

        for bus in app.BusinessOwnerContacts.all():
            if bus.Contact.UID is not None:
                if busline == '':
                    busline = bus.Contact.Name
                else:
                    busline += ',' + bus.Contact.Name
        for pl in app.ProjectLeads.all():
            if pl.Contact.UID is not None:
                if prldline == '':
                    prldline = pl.Contact.Name
                else:
                    prldline += ',' + pl.Contact.Name
        incints = ApplicationInterface.objects.filter(IncomingApplication=app)
        outints = ApplicationInterface.objects.filter(OutgoingApplication=app)
        for i in incints:
            if intline == '':
                intline = i.Name
            else:
                intline = intline + ', ' + i.Name
        for o in outints:
            if intline == '':
                intline = o.Name
            else:
                intline = intline + ', ' + o.Name
        csvwriter.writerow(
            [app.Name, app.DispositionType, app.ApplicationCategory, app.ApplicationRole, apptype, app.Vendor, suite,
             app.AuthenticationType, tocline, busline, prldline, euline, unit, busval, tecint, intline])
    return csvwriter

def CSVExportProjects(projects, csvwriter):
    csvwriter.writerow(['ProjectName', 'StartDate', 'DueDate',
                        'Finished'])
    # build up row.
    for prj in projects:
        pmline = ''
        for g in prj.ProjectManager.all():
            if g.Contact.UID is not None:
                if pmline == '':
                    pmline = g.Contact.UID
                else:
                    pmline += ',' + g.Contact.UID
        csvwriter.writerow([prj.Name, prj.StartDate, prj.DueDate, prj.Finished])
    return csvwriter

if __name__ == '__main__':
    import django

    django.setup()
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silk.settings")
    print 'CSV Exporter....driver for CSVExport method'
    parser = argparse.ArgumentParser(description='CSV Export of SILK')
    # parser.add_argument('-d','--directory',help='Directory',required=True)
    args = vars(parser.parse_args())
    from silkollect.models import Application, Suite, SuiteRoadmap, ApplicationRoadmap, Report

    allapps = Application.objects.all().order_by('ApplicationCategory__Name', 'Name')
    with open('silk_applicationsJIRA.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)  # , #delimiter='', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        CSVExportApplicationsCAMPlot(allapps, csvwriter)