import argparse
import csv
import os

def CSVExportServerRoles(allServerRoles, csvwriter):
    from silkollect.models import ServerRole, Server, Application
    csvwriter.writerow(['Physical Location', 'Description', 'ComputerName','IPAddress','Environment',
                        'HardwareType','Server OS', 'ServerType', 'DatabaseVersion', 'ApplicationsHosted'])
    for role in allServerRoles:
        server = role.Server
        if server is not None:
            locationstr = server.Site.Name
            servername = server.ComputerName
            ipaddress = server.IPAddress
            dbtype = None if role.DatabaseType is None else role.DatabaseType.Name
            envstr = None if role.ApplicationEnvironment is None else role.ApplicationEnvironment.Name
            hwtype = None if server.HardwareType is None else server.HardwareType.Name
            ostype = None if server.OperatingSystem is None else server.OperatingSystem.Name
            srvtype = None if role.ServerType is None else role.ServerType.Name
            apps = Application.objects.filter(ServerRoles = role)
            appline = ', '.join(i.Name for i in apps)

            csvwriter.writerow(
                [locationstr,server.ShortDescription, servername, ipaddress, envstr, hwtype, ostype, srvtype, dbtype, appline])

    return csvwriter



def CSVExportRiskEntries(allrisks, csvwriter):
    from silkollect.models import DispensationEntry, BusinessCapability
    csvwriter.writerow(['RiskEntryID', 'Name', 'SatisifiedDate','Open Dispensations',
                        'TechnologyClassifications',
                        'ArchitecturePillars', 'ViolatedPrinciples','ViolatedStandards',
                        'ViolatedStrategies', 'Description', 'AffectedApplications', 'AffectedITCapabilities','AffectedBusinessCapabilities'])
    for risk in allrisks:
        appline = ', '.join([a.Name for a in risk.Applications.all()])

        opendisps = DispensationEntry.objects.filter(RiskEntry=risk).filter(Disposition=1)
        dline = None
        for disp in opendisps:
            working = 'Due: ' + str(disp.DispensationDueDate) + ': ' + disp.Name
            if dline is None:
                dline = working
            else:
                dline += '; ' + working
        displine = dline
        #displine = ', '.join([str(i.DispensationDueDate) for i in DispensationEntry.objects.filter(RiskEntry=risk).filter(Disposition=1)])
        classline = ', '.join([c.Name for c in risk.TechnologyClassifications.all()])
        pillarline = ', '.join([i.Name for i in risk.ArchitecturePillars.all()])
        princeline = ', '.join([i.Name for i in risk.ViolatedPrinciples.all()])
        standardsline = ', '.join([i.Name for i in risk.ViolatedStandards.all()])
        strategiesline = ', '.join([i.Name for i in risk.ViolatedStrategies.all()])
        totalbcaps = []
        totalicaps = []
        for a in risk.Applications.all():
            for approle in a.ApplicationRoles.all():
                if approle is not None:
                    for icap in approle.ITCapabilities.all():
                        if icap not in totalicaps:
                            totalicaps.append(icap)
                        for bcap in icap.BusinessCapabilities.all():
                            if bcap not in totalbcaps:
                                totalbcaps.append(bcap)
        bcapline = ', '.join(i.Name for i in totalbcaps)
        icapline= ', '.join(i.Name for i in totalicaps)
        descline = risk.Description.encode('utf-8').strip()
        csvwriter.writerow(
            [risk.id, risk.Name, risk.SatisfiedDate if True else '',displine,classline,
             pillarline, princeline, standardsline, strategiesline,descline, appline, icapline, bcapline])
    return csvwriter


def CSVExportApplicationsCAMPlot(allapps, csvwriter):
    from silkollect.models import Application, ApplicationInterface, RiskEntry, BusinessCapability, ServerRole, Server
    csvwriter.writerow(['AppID','Name', 'Disposition', 'Site', 'Vendor', 'AccountingNumber','Suite', 'ApplicationCategory',
                        'ApplicationRole', 'ITCapabilities', 'BusinessCapabilities','AppType',
                        'AuthenticationType', 'TechnicalOwners', 'BusinessOwners', 'ProjectLeads', 'EndUserContacts',
                        'BusinessUnit',  'BusinessValue', 'TechnicalIntegrity', 'RiskClassification',
                        'RiskEntry?',
                        'RecoveryPointObjective', 'RecoveryTimeObjective',
                        'ApplicationInterfaces','Servers'])
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
        site = ''
        euline = ''
        vendorName = ''
        vendorNumber = ''
        riskclass = ''
        if app.Site is not None:
            site = app.Site.Name
        if app.Vendor is not None:
            vendorName = app.Vendor.Name
            vendorNumber = app.Vendor.AccountingNumber
        if app.Suite is not None:
            suite = app.Suite
        if app.BusinessUnit is not None:
            unit = app.BusinessUnit
        if app.ApplicationType is not None:
            apptype = app.ApplicationType
        if app.business_value is not None:
            busval = dict(Application.Value_Choices)[app.business_value]
        if app.technical_integrity is not None:
            tecint = dict(Application.Value_Choices)[app.technical_integrity]
        if app.RiskClassification is not None:
            riskclass = dict(Application.Risk_Classification_Choices)[app.RiskClassification]
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
        riskline = ', '.join([i.Name for i in RiskEntry.objects.filter(Applications = app)])
        capline = ''
        totalbcaps = []
        totalicaps = []
        roleline = ', '.join([i.Name for i in app.ApplicationRoles.all()])
        for approle in app.ApplicationRoles.all():
            if approle is not None:
                for icap in approle.ITCapabilities.all():
                    if icap not in totalicaps:
                        totalicaps.append(icap)
                    for bcap in icap.BusinessCapabilities.all():
                        if bcap not in totalbcaps:
                            totalbcaps.append(bcap)

        bcapline = ', '.join(i.Name for i in totalbcaps)
        icapline = ', '.join(i.Name for i in totalicaps)
        srvline = ', '.join(i.Server.ComputerName for i in app.ServerRoles.all())
        dispositionType = '' if app.disposition_type is None else dict(Application.disposition_type_choices)[app.disposition_type]
        csvwriter.writerow(
            [app.id, app.Name, dispositionType, site, vendorName, vendorNumber, suite, app.ApplicationCategory,
             roleline, icapline, bcapline, apptype, app.AuthenticationType, tocline, busline,
             prldline, euline, unit, busval, tecint, riskclass, riskline,
             app.RecoveryPointObjective,
             app.RecoveryTimeObjective, intline,srvline])
    return csvwriter

def CSVExportOpenProjects(projects, csvwriter):
    from silkollect.models import ProjectTask
    csvwriter.writerow(['ProjectName', 'StartDate', 'DueDate', 'ProjectManager',
                        'Finished', 'PMO?',
                        'ProjectTask', 'TaskStartDate', 'TaskDueDate', 'Finished'])
    # build up row.

    for prj in projects:
        tasks = ProjectTask.objects.filter(Project = prj)
        pmline = ''
        for g in prj.ProjectManager.all():
            if g.Contact.Name is not None:
                if pmline == '':
                    pmline = g.Contact.Name
                else:
                    pmline += ',' + g.Contact.Name
        if len(tasks) == 0:
            csvwriter.writerow([prj.Name, prj.StartDate, prj.DueDate, pmline, prj.Finished,
                                str(prj.PMOSupported)])
        else:
            for task in tasks:
                csvwriter.writerow([prj.Name, prj.StartDate, prj.DueDate,
                                    pmline, prj.Finished, str(prj.PMOSupported),
                                    task.Name, task.StartDate, task.DueDate, task.Finished])

    return csvwriter

if __name__ == '__main__':
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'silk.settings.development')
    django.setup()
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silk.settings")
    print 'CSV Exporter....driver for CSVExport method'
    parser = argparse.ArgumentParser(description='CSV Export of SILK')
    parser.add_argument('-file','--file',help='File',required=True)
    parser.add_argument('-action','--action', help='Action', required=True)
    args = vars(parser.parse_args())
    if args['action'].upper() == 'APPLICATIONS':
        from silkollect.models import Application
        allapps = Application.objects.all().order_by('Name')#''ApplicationCategory__Name', 'Name')
        with open(args['file'], 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)  # , #delimiter='', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            CSVExportApplicationsCAMPlot(allapps, csvwriter)
            csvfile.close()
    elif args['action'].upper() == 'RISKENTRIES':
        from silkollect.models import RiskEntry
        allrisks = RiskEntry.objects.all().order_by('Name')
        with open(args['file'], 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            CSVExportRiskEntries(allrisks, csvwriter)
            csvfile.close()
    elif args['action'].upper() == 'SERVERROLES':
        from silkollect.models import ServerRole
        allserverroles = ServerRole.objects.all()
        with open(args['file'], 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            CSVExportServerRoles(allserverroles, csvwriter)
            csvfile.close()
    elif args['action'].upper() == 'PROJECTS':
        from silkollect.models import Project
        allprojects = Project.objects.filter(Finished=False)
        with open(args['file'], 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            CSVExportOpenProjects(allprojects, csvwriter)
            csvfile.close()
    else:
        print 'nothing to do...perhaps provide a valid ACTION?'