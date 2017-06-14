from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
# in, out, in/out
from django.utils.html import format_html

class InterfaceDirection(models.Model):
    Name = models.CharField(max_length=10)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "interfacedirection"

# com, csv file, etc.
class InterfaceType(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "interfacetype"


class TransportType(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "transporttype"


class Site(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "site"


class ApplicationType(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "applicationtype"


class DatabaseType(models.Model):
    Name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.Name

    class Meta:
        db_table = "databasetype"


class AuthenticationType(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "authenticationtype"


class Report(models.Model):
    Value_Choices = (
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Very High')
    )
    Name = models.CharField(max_length=255)
    InformationSource = models.ForeignKey('InformationSource', null=True, blank=True)
    business_value = models.IntegerField(choices=Value_Choices, null=True, blank=True)
    technical_integrity = models.IntegerField(choices=Value_Choices, null=True, blank=True)
    Application = models.ForeignKey('Application', related_name='applicationreport')
    Description = models.TextField(blank=True, null=True)
    EnhancementNeeds = models.TextField(blank=True, null=True)
    Attachment = models.FileField(blank=True)
    TechnicalOwnerContacts = models.ManyToManyField('TechnicalOwnerContact', blank=True)
    BusinessOwnerContacts = models.ManyToManyField('BusinessOwnerContact', blank=True)
    EndUserContacts = models.ManyToManyField('EndUserContact', blank=True)
    ProjectLeads = models.ManyToManyField('ProjectLead', blank=True)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "report"


class BusinessCapability(models.Model):
    Name = models.CharField(max_length=255)
    BusinessUnit = models.ForeignKey('BusinessUnit', null=True, blank=True)
    BusinessCapabilityParent = models.ForeignKey('BusinessCapability', null=True, blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Name

    @property
    def Level(self):
        level = 1
        parent = self.BusinessCapabilityParent
        while parent != None:
            level += 1
            parent = parent.BusinessCapabilityParent
        return level
    def getChildren(bcap):
        nextchiles = BusinessCapability.objects.filter(BusinessCapabilityParent = bcap)
        return nextchiles
    class Meta:
        ordering = ['Name']
        verbose_name_plural = "Business Capabilities"
        db_table = "businesscapability"

    def display_Children(self):
        firstchiles = BusinessCapability.objects.filter(BusinessCapabilityParent=self)
        chilestring = ', '.join(
            ["<a href='" + reverse("admin:silkollect_businesscapability_change", args=[i.id]) + "'>(" +
             str(i.Level) + ') - ' +  i.Name + "</a>" for i in firstchiles.all()])
        return chilestring
    display_Children.short_description = 'Children Capabilities'
    display_Children.allow_tags = True

class ITCapability(models.Model):
    Name = models.CharField(max_length=255)
    ITCapabilityParent = models.ForeignKey('ITCapability', null=True, blank=True)
    Description = models.TextField(blank=True, null=True)
    BusinessCapabilities = models.ManyToManyField('BusinessCapability', blank=True)
    def __str__(self):
        return self.Name

    @property
    def Level(self):
        level = 1
        parent = self.ITCapabilityParent
        while parent != None:
            level += 1
            parent = parent.ITCapabilityParent
        return level

    class Meta:
        ordering = ['Name']
        verbose_name_plural = "IT Capabilities"
        db_table = 'itcapability'
    def display_BusinessCapabilities(self):
        return ', '.join([i.Name for i in self.BusinessCapabilities.all()])

class Suite(models.Model):
    Value_Choices = (
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Very High')
    )
    Name = models.CharField(max_length=255)
    InformationSource = models.ForeignKey('InformationSource', null=True, blank=True)
    business_value = models.IntegerField(choices=Value_Choices, null=True, blank=True)
    technical_integrity = models.IntegerField(choices=Value_Choices, null=True, blank=True)
    ApplicationCategory = models.ForeignKey('ApplicationCategory', null=True, blank=True)
    Project = models.ForeignKey('Project', blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Maintenance = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    CostNotes = models.TextField(blank=True, null=True)
    EnhancementNeeds = models.TextField(blank=True, null=True)
    Version = models.CharField(max_length=255, blank=True, null=True)
    Site = models.ForeignKey(Site, blank=True, null=True)
    Attachment = models.FileField(blank=True)
    BusinessUnit = models.ForeignKey('BusinessUnit', blank=True, null=True)
    CostCenter = models.ForeignKey('CostCenter', blank=True, null=True)
    TechnicalOwnerContacts = models.ManyToManyField('TechnicalOwnerContact', blank=True)
    BusinessOwnerContacts = models.ManyToManyField('BusinessOwnerContact', blank=True)
    EndUserContacts = models.ManyToManyField('EndUserContact', blank=True)
    ProjectLeads = models.ManyToManyField('ProjectLead', blank=True)

    def __str__(self):
        return self.Name

    def display_suiteapplications(self):
        apps = Application.objects.filter(Suite=self)
        return ', '.join([a.Name for a in apps.all()])

    display_suiteapplications.short_description = 'Applications for Suite'
    display_suiteapplications.allow_tags = True

    class Meta:
        db_table = "suite"


class FunctionalArea(models.Model):
    Name = models.CharField(max_length=255)
    BusinessUnit = models.ForeignKey('BusinessUnit', blank=True, null=True)
    BusinessOwnerContacts = models.ManyToManyField('BusinessOwnerContact', blank=True)

    def __str__(self):
        if BusinessUnit == None:
            return self.Name
        else:
            return self.Name + ' (' + str(self.BusinessUnit) + ')'

    class Meta:
        ordering = ['Name']

    class Meta:
        db_table = "functionalarea"


class BusinessUnitAttachment(models.Model):
    BusinessUnit = models.ForeignKey("BusinessUnit")
    File = models.FileField(blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.File)

    class Meta:
        db_table = "businessunitattachment"


class BusinessGoalAttachment(models.Model):
    BusinessGoal = models.ForeignKey("BusinessGoal")
    File = models.FileField(blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'BusinessGoal: ' + str(self.BusinessGoal) + ', file: ' + str(self.File)

    class Meta:
        db_table = "businessgoalattachment"


class BusinessGoal(models.Model):
    Name = models.CharField(max_length=255)
    Year = models.IntegerField(blank=True, null=True)
    BusinessUnit = models.ForeignKey('BusinessUnit', blank=True, null=True)
    Description = models.TextField(blank=True, null=True)

    # BusinessStrategy
    def __str__(self):
        if BusinessUnit != None:
            return '(' + str(self.BusinessUnit) + ') - ' + self.Name
        else:
            return self.Name

    class Meta:
        db_table = "businessgoal"

    def display_BusinessObjectives(self):
        o = BusinessObjective.objects.filter(BusinessGoals=self)
        return ', '.join(
            ["<a href='" + reverse("admin:silkollect_businessobjective_change", args=[i.id]) + "'>" + i.Name + "</a>" for
             i in o.all()])
    display_BusinessObjectives.short_description = 'Objectives assigned to this'
    display_BusinessObjectives.allow_tags = True


    def display_BusinessStrategies(self):
        objs = BusinessObjective.objects.filter(BusinessGoals=self)
        returnString = None
        for o in objs:
            strats = BusinessStrategy.objects.filter(BusinessObjectives = o)
            printstring =   ', '.join(
                    ["<a href='" + reverse("admin:silkollect_businessstrategy_change", args=[i.id]) + "'>" + i.Name + "</a>" for
                    i in strats.all()])
            if returnString == None:
                returnString= printstring
            else:
                returnString = returnString + ', ' + printstring

        return returnString
    display_BusinessStrategies.short_description = 'Strategies assigned to this'
    display_BusinessStrategies.allow_tags = True


    def display_BusinessTactics(self):
        objs = BusinessObjective.objects.filter(BusinessGoals=self)
        returnString = None
        for o in objs:
            strats = BusinessStrategy.objects.filter(BusinessObjectives=o)
            for s in strats:
                tacs = BusinessTactic.objects.filter(BusinessStrategies = s)
                printstring = ', '.join(
                    ["<a href='" + reverse("admin:silkollect_businesstactic_change", args=[i.id]) + "'>" + i.Name + "</a>" for
                    i in tacs.all()])
                if returnString == None:
                    returnString = printstring
                else:
                    returnString = returnString + ', ' + printstring

        return returnString


    display_BusinessTactics.short_description = 'Tactics assigned to this'
    display_BusinessTactics.allow_tags = True

class BusinessStrategy(models.Model):
    Name = models.CharField(max_length=255)
    BusinessUnit = models.ForeignKey('BusinessUnit', blank=True, null=True)
    BusinessObjectives = models.ManyToManyField('BusinessObjective', blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        if BusinessUnit != None:
            return '(' + str(self.BusinessUnit) + ') - ' + self.Name
        else:
            return self.Name

    def display_BusinessObjectives(self):
        return ', '.join(
            ["<a href='" + reverse("admin:silkollect_businessobjective_change", args=[i.id]) + "'>" + str(
                i.Name) + "</a>" for i in self.BusinessObjectives.all()])

    display_BusinessObjectives.short_description = 'Objective this is Tied to'
    display_BusinessObjectives.allow_tags = True

    def display_BusinessGoals(self):
        returnString = None
        goals = self.BusinessObjectives.all()
        for g in goals:
            objstring = ', '.join(
                    ["<a href='" + reverse("admin:silkollect_businessgoal_change", args=[i.id]) + "'>" + str(
                        i.Name) + "</a>" for i in s.BusinessGoals.all()])
            if returnString == None:
                returnString = objstring
            else:
                returnString = returnString + ', ' + objstring
        return returnString
    display_BusinessGoals.short_description = 'Goal this is Tied to'
    display_BusinessGoals.allow_tags = True

    class Meta:
        db_table = "businessstrategy"


class BusinessObjective(models.Model):
    Name = models.CharField(max_length=255)
    BusinessUnit = models.ForeignKey('BusinessUnit', blank=True, null=True)
    BusinessGoals = models.ManyToManyField(BusinessGoal, blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        if BusinessUnit != None:
            return '(' + str(self.BusinessUnit) + ') - ' + self.Name
        else:
            return self.Name

    class Meta:
        db_table = "businessobjective"

    def display_BusinessGoals(self):
        return ', '.join(
            ["<a href='" + reverse("admin:silkollect_businessgoal_change", args=[i.id]) + "'>" + str(
                i.Name) + "</a>" for i in self.BusinessGoals.all()])
    display_BusinessGoals.short_description = 'Goal this is Tied to'
    display_BusinessGoals.allow_tags = True

    def display_BusinessStrategies(self):
        s = BusinessStrategy.objects.filter(BusinessObjectives=self)
        return ', '.join(
            ["<a href='" + reverse("admin:silkollect_businessstrategy_change", args=[i.id]) + "'>" + i.Name + "</a>" for
             i in s.all()])
    display_BusinessStrategies.short_description = 'Strategies assigned to this'
    display_BusinessStrategies.allow_tags = True

    class Meta:
        db_table = "businessobjective"


class BusinessTactic(models.Model):
    Name = models.CharField(max_length=255)
    BusinessUnit = models.ForeignKey('BusinessUnit', blank=True, null=True)
    BusinessStrategies = models.ManyToManyField(BusinessStrategy, blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        if BusinessUnit != None:
            return '(' + str(self.BusinessUnit) + ') - ' + self.Name
        else:
            return self.Name

    class Meta:
        db_table = "businesstactic"

    def display_BusinessStrategies(self):
        return ', '.join(
            ["<a href='" + reverse("admin:silkollect_businessstrategy_change", args=[i.id]) + "'>" + str(
                i.Name) + "</a>" for i in self.BusinessStrategies.all()])
    display_BusinessStrategies.short_description = 'Strategy this is Tied to'
    display_BusinessStrategies.allow_tags = True

    def display_BusinessObjectives(self):
        returnString = None
        strats = self.BusinessStrategies.all()
        for s in strats:
            objstring = ', '.join(
                    ["<a href='" + reverse("admin:silkollect_businessobjective_change", args=[i.id]) + "'>" + str(
                        i.Name) + "</a>" for i in s.BusinessObjectives.all()])
            if returnString == None:
                returnString = objstring
            else:
                returnString = returnString + ', ' + objstring
        return returnString
    display_BusinessObjectives.short_description = 'Objective this is Tied to'
    display_BusinessObjectives.allow_tags = True

    def display_BusinessGoals(self):
        returnString = None
        strats = self.BusinessStrategies.all()
        for s in strats:
            for o in s.BusinessObjectives.all():
                goalstring = ', '.join(
                    ["<a href='" + reverse("admin:silkollect_businessgoal_change", args=[i.id]) + "'>" + str(
                        i.Name) + "</a>" for i in o.BusinessGoals.all()])
                if returnString == None:
                    returnString = goalstring
                else:
                    returnString = returnString + ', ' + goalstring
        return returnString
    display_BusinessGoals.short_description = 'Goal this is Tied to'
    display_BusinessGoals.allow_tags = True


class Contact(models.Model):
    Name = models.CharField(max_length=255)
    UID = models.CharField(max_length=255, blank=True, null=True)
    Email = models.CharField(max_length=255, blank=True, null=True)
    PositionClass = models.ForeignKey('PositionClass', null=True, blank=True)
    PositionTitle = models.ForeignKey('PositionTitle', null=True, blank=True)

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']
        db_table = 'contact'


class EndUserContact(models.Model):
    Contact = models.OneToOneField('Contact')

    def __str__(self):
        return str(self.Contact)

    class Meta:
        ordering = ['Contact__Name']
        db_table = "endusercontact"

    @property
    def Name(self):
        return self.Contact.Name


class BusinessOwnerContact(models.Model):
    Contact = models.OneToOneField('Contact')

    def __str__(self):
        return str(self.Contact)

    class Meta:
        ordering = ['Contact__Name']
        db_table = "businessownercontact"

    @property
    def Name(self):
        return self.Contact.Name


class TechnicalOwnerContact(models.Model):
    Contact = models.OneToOneField('Contact')

    def __str__(self):
        return str(self.Contact)

    class Meta:
        ordering = ['Contact__Name']
        "technicalownercontact"

    @property
    def Name(self):
        return self.Contact.Name


class ProjectLead(models.Model):
    Contact = models.OneToOneField('Contact')

    def __str__(self):
        return str(self.Contact)

    class Meta:
        ordering = ['Contact__Name']
        db_table = "projectlead"

    @property
    def Name(self):
        return self.Contact.Name


class ProjectManager(models.Model):
    Contact = models.OneToOneField('Contact')

    def __str__(self):
        return str(self.Contact)

    class Meta:
        ordering = ['Contact__Name']
        db_table = "projectmanager"

    @property
    def Name(self):
        return self.Contact.Name


class Survey(models.Model):
    Application = models.ForeignKey('Application', related_name='survey')
    Name = models.CharField(max_length=255)

    def __str__(self):
        return 'Application: ' + str(self.Application) + ', ' + self.Name

    class Meta:
        ordering = ['Application']
        db_table = "survey"


class SurveyQuestion(models.Model):
    Survey = models.ForeignKey('Survey', related_name='surveyquestion')
    Question = models.TextField()
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Survey: ' + str(self.Survey) + ', question: ' + self.Question

    @property
    def noanswers(self):
        return not SurveyAnswer.objects.filter(Question=self).exists()

    class Meta:
        ordering = ['Question']
        db_table = "surveyquestion"


class SurveyAnswer(models.Model):
    Question = models.ForeignKey('SurveyQuestion', related_name='surveyanswer')
    Answer = models.TextField()
    Date = models.DateTimeField(auto_now_add=True)
    Answerer = models.ForeignKey(Contact, blank=True, null=True)

    def __str__(self):
        # return self.Answer
        return ('%s' % self.Answer).encode('ascii', errors='replace')

    class Meta:
        db_table = "surveyanswer"


class GenericToDoItem(models.Model):
    Name = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.Name)

    class Meta:
        db_table = "generictodoitem"


class ToDoItem(models.Model):
    Application = models.ForeignKey('Application', related_name='todoitem')
    Name = models.CharField(max_length=1000, blank=True, null=True)
    GenericToDoItem = models.ForeignKey('GenericToDoItem', blank=True, null=True)
    Done = models.BooleanField(default=False)
    DoneDate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '(' + str(self.Application) + '): ' + str(self.Name)

    class Meta:
        db_table = "todoitem"


class ApplicationAttachment(models.Model):
    Application = models.ForeignKey('Application')
    File = models.FileField(blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Application: ' + str(self.Application) + ', file: ' + str(self.File)

    class Meta:
        db_table = "applicationattachment"


class ITStrategyAttachment(models.Model):
    ITStrategy = models.ForeignKey("ITStrategy")
    File = models.FileField(blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'ITStrategy: ' + str(self.ITStrategy) + ', file: ' + str(self.File)

    class Meta:
        db_table = "itstrategyattachment"


class InterfaceAttachment(models.Model):
    ApplicationInterface = models.ForeignKey("ApplicationInterface")
    File = models.FileField(blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'ApplicationInterface: ' + str(self.ApplicationInterface) + ', file: ' + str(self.File)

    class Meta:
        db_table = "interfaceattachment"


class ArchitectureStandardAttachment(models.Model):
    ArchitectureStandard = models.ForeignKey("ArchitectureStandard")
    File = models.FileField(blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'ArchitectureStandard: ' + str(self.ArchitectureStandard) + ', file: ' + str(self.File)

    class Meta:
        db_table = "architecturestandardattachment"


class TechnicalOwnerContactAttachment(models.Model):
    TechnicalOwnerContact = models.ForeignKey("TechnicalOwnerContact")
    File = models.FileField(blank=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Technical Contact: ' + str(self.TechnicalOwnerContact) + ', file: ' + str(self.File)

    class Meta:
        db_table = "technicalownercontactattachment"


class UserBase(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.TextField(blank=True, null=True)
    def __str__(self):
        return 'User Base: ' + str(self.Name)
    class Meta:
        db_table = "userbase"


class ApplicationCategory(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "applicationcategory"


class InformationSource(models.Model):
    Name = models.CharField(max_length=255)
    Attachment = models.FileField(blank=True)

    def __str__(self):
        return self.Name


class Meta:
    db_table = "informationsource"


class ITService(models.Model):
    Name = models.CharField(max_length=255)
    ITCapabilities = models.ManyToManyField('ITCapability', blank=True)

    def __str__(self):
        return self.Name

    def display_ITCapabilities(self):
        #return ', '.join([i.Name for i in self.ITCapabilities.all()])
        return ', '.join(
            ["<a href='" + reverse("admin:silkollect_itcapability_change", args=[i.id]) + "'>" + i.Name +
             "</a>" for i in self.ITCapabilities.all()])

    display_ITCapabilities.short_description = 'Provides IT Capabilities (top level)'
    display_ITCapabilities.allow_tags = True

    class Meta:
        db_table = "itservice"


class DataClassification(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.Name

class DataType(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.TextField(blank=True, null=True)
    DataClassification = models.ForeignKey('DataClassification', null=True, blank=True)
    def __str__(self):
        return self.Name + ', Classification: ' + str(self.DataClassification)

#TODO: build out data classificatons for each application according to IT Security
class Application(models.Model):
    Name = models.CharField(max_length=255)
    #ITServices = models.ManyToManyField('ITService', blank=True)
    ApplicationCategory = models.ForeignKey('ApplicationCategory', null=True, blank=True)
    InformationSource = models.ForeignKey('InformationSource', null=True, blank=True)
    DataTypes = models.ManyToManyField('DataType', blank=True)
    # VeryLow = 'VL'
    # Low = 'L'
    # Medium = 'M'
    # High = 'H'
    # VeryHigh = 'VH'
    Value_Choices = (
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Very High')
    )
    Risk_Classification_Choices = (
        (1, 'End of Life (System Retirements)'),
        (2, 'Out of Compliance (Declining and Risky)'),
        (3, 'Stable and Proven (Core to the Business)'),
        (4, 'Available and Ready (Strategic Importance)'),
        (5, 'Early Adoption (Emerging Opportunity)')
    )
    disposition_type_choices = (
        (1, 'Currently Deployed'),
        (2, 'Decommissioned'),
        (3, 'Deployed, will decommission'),
        (4, 'Not in Production - in planning')
    )
    # business_value = models.CharField(max_length=2, choices=Value_Choices, blank=True, null=True)
    # technical_integrity = models.CharField(max_length=2, choices=Value_Choices, blank=True, null=True)
    business_value = models.IntegerField(choices=Value_Choices, null=True, blank=True)
    technical_integrity = models.IntegerField(choices=Value_Choices, null=True, blank=True)
    RiskClassification = models.IntegerField(choices=Risk_Classification_Choices, blank=True, null=True)
    #DispositionType = models.ForeignKey('DispositionType', blank=True, null=True)
    disposition_type = models.IntegerField(choices=disposition_type_choices, blank=True, null=True)
    Vendor = models.ForeignKey('Vendor', blank=True, null=True)
    # Cost = models.CharField(max_length=255, blank=True, null=True)
    InitialCost = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    Maintenance = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    CostNotes = models.TextField(blank=True, null=True)
    ApproximateNumberOfUsers = models.CharField(max_length=255, blank=True, null=True)
    ApplicationRoles = models.ManyToManyField('ApplicationRole', blank=True)
    RegulatoryType = models.ManyToManyField('RegulatoryType', blank=True)
    Projects = models.ManyToManyField('Project', blank=True)
    Description = models.TextField(blank=True, null=True)
    EnhancementNeeds = models.TextField(blank=True, null=True)
    Version = models.CharField(max_length=255, blank=True, null=True)
    Suite = models.ForeignKey(Suite, blank=True, null=True)
    ApplicationType = models.ForeignKey(ApplicationType, blank=True, null=True)
    AuthenticationType = models.ForeignKey(AuthenticationType, blank=True, null=True)
    ApplicationSpecifics = models.TextField(blank=True, null=True)
    Site = models.ForeignKey(Site, blank=True, null=True)
    ServiceAccounts = models.ManyToManyField('ServiceAccount', blank=True)
    ServerRoles = models.ManyToManyField('ServerRole', blank=True)
    TechnicalOwnerContacts = models.ManyToManyField(TechnicalOwnerContact, blank=True)
    BusinessOwnerContacts = models.ManyToManyField(BusinessOwnerContact, blank=True)
    EndUserContacts = models.ManyToManyField(EndUserContact, blank=True)
    ProjectLeads = models.ManyToManyField(ProjectLead, blank=True)
    UserBases = models.ManyToManyField(UserBase, blank=True)
    Dependencies = models.ManyToManyField('Application', blank=True)
    BusinessUnit = models.ForeignKey('BusinessUnit', blank=True, null=True)
    CostCenter = models.ForeignKey('CostCenter', blank=True, null=True)
    RecoveryPointObjective = models.ForeignKey('RecoveryObjective', blank=True, null=True,
                                               related_name='RecoveryPointObjective')
    RecoveryTimeObjective = models.ForeignKey('RecoveryObjective', blank=True, null=True,
                                                related_name = 'RecoveryTimeObjective')
    # ToDoItems = models.ManyToManyField(ToDoItem, blank=True)
    def __str__(self):
        return self.Name

    def display_RiskEntries(self):
        risks = RiskEntry.objects.filter(Applications=self).filter(Satisfied=False)
        printstring = None
        for r in risks:
            urlstring = format_html("<a href='{url}'>" + r.Name + "</a>", url=reverse("admin:silkollect_riskentry_change", args=[r.id]))
            if printstring == None:
                printstring = urlstring
            else:
                printstring = printstring + ', ' + urlstring
        return printstring
    display_RiskEntries.short_description = 'Risk Entries'
    display_RiskEntries.allow_tags = True
    # this functionality adds a many-to-many field on the admin form
    # https://www.jmccauli.com/django-list-display-and-manytomany-fields
    def display_TechnicalOwnerContacts(self):
        return ', '.join([bc.Contact.Name for bc in self.TechnicalOwnerContacts.all()])

    display_TechnicalOwnerContacts.short_description = 'TechnicalOwnerContacts'
    display_TechnicalOwnerContacts.allow_tags = True

    #def display_ITServices(self):
     #   return ', '.join([i.Name for i in self.ITServices.all()])

    #display_ITServices.short_description = 'Supports IT Services'
    #display_ITServices.allow_tags = True

    def display_TechnicalIntegrity(self):
        return self.get_technical_integrity_display()
    display_TechnicalIntegrity.short_description = 'Technical Integrity'
    def display_BusinessValue(self):
        return self.get_business_value_display()
    display_BusinessValue.short_description = 'Business Value'
    def display_ToDoItems(self):
        todos = ToDoItem.objects.filter(Application = self)
        return ', '.join([i.Name for i in todos])
    display_ToDoItems.short_description = 'TODO Items'
    def display_ApplicationRoles(self):
        return ', '.join(
            ["<a href='" + reverse("admin:silkollect_applicationrole_change", args=[i.id]) + "'>" + i.Name +
             "</a>" for i in self.ApplicationRoles.all()])
    display_ApplicationRoles.short_description = 'Application Roles'
    display_ApplicationRoles.allow_tags = True

    def display_ITCapabilities(self):
        for role in self.ApplicationRoles.all():
            caps = role.ITCapabilities
            return ', '.join(["<a href='" + reverse("admin:silkollect_itcapability_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in caps.all()])
        else:
            return ''
    display_ITCapabilities.short_description = 'IT Capabilities'
    display_ITCapabilities.allow_tags = True

    def display_BusinessCapabilities(self):
        caps = None
        for role in self.ApplicationRoles.all():
            for icap in role.ITCapabilities.all():
                caps = icap.BusinessCapabilities
        if caps is not None:
            return ', '.join(["<a href='" + reverse("admin:silkollect_businesscapability_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in caps.all()])
        else:
            return ''

    display_BusinessCapabilities.short_description = 'Business Capabilities'
    display_BusinessCapabilities.allow_tags = True


    def display_Dependencies(self):
        return ', '.join(
            ["<a href='" + reverse("admin:silkollect_application_change", args=[i.id]) + "'>" + i.Name +
             "</a>" for i in self.Dependencies.all()])
    display_Dependencies.short_description = 'Dependencies'
    display_Dependencies.allow_tags = True
    def display_Disposition(self):
        return None if self.disposition_type is None else \
            dict(Application.disposition_type_choices)[self.disposition_type]

    class Meta:
        db_table = "application"


class SuiteRoadmap(models.Model):
    Suite = models.ForeignKey('Suite', related_name='roadmap')
    Year = models.CharField(max_length=255)
    Version = models.CharField(max_length=255, blank=True, null=True)
    Cost = models.CharField(max_length=255, blank=True, null=True)
    CostNotes = models.TextField(blank=True, null=True)
    Notes = models.TextField(blank=True, null=True)

    def __str__(self):
        notes = ''
        if self.Notes != None:
            notes = self.Notes
        return 'Suite: ' + str(self.Suite) + " (" + self.Year + "): " + notes

    class Meta:
        ordering = ['Suite']

    class Meta:
        db_table = "suiteroadmap"


class ApplicationRoadmap(models.Model):
    Application = models.ForeignKey('Application', related_name='roadmap')
    Year = models.CharField(max_length=255)
    Version = models.CharField(max_length=255, blank=True, null=True)
    Cost = models.CharField(max_length=255, blank=True, null=True)
    CostNotes = models.TextField(blank=True, null=True)
    Notes = models.TextField(blank=True, null=True)

    def __str__(self):
        notes = ''
        if self.Notes != None:
            notes = self.Notes
        return 'Application: ' + str(self.Application) + " (" + self.Year + "): " + notes

    class Meta:
        ordering = ['Application']

    class Meta:
        db_table = "applicationroadmap"


class PositionTitle(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name


class PositionClass(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "positionclass"


class BusinessUnit(models.Model):
    Name = models.CharField(max_length=255)
    BusinessUnitParent = models.ForeignKey('BusinessUnit', blank=True, null=True)
    BusinessOwnerContact = models.ForeignKey('BusinessOwnerContact', blank=True, null=True)

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']
        db_table = "businessunit"


class CostCenter(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "costcenter"


class Vendor(models.Model):
    Name = models.CharField(max_length=255)
    AccountingNumber = models.IntegerField(null=True, blank=True,)
    def __str__(self):
        return self.Name

    class Meta:
        db_table = "vendor"
        ordering = ['Name']
    def display_Applications(self):
        apps = Application.objects.filter(Vendor=self)
        returnstring = ''
        numb = len(apps)
        if numb > 1:
            appstring = ', '.join([a.Name for a in apps.all()])
            if len(appstring) > 50:
                returnstring = '(' + str(numb) + ' apps): ' + appstring[:50] + '...'
            else:
                returnstring = '(' + str(numb) + ' apps): ' + appstring
        else:
            returnstring = ', '.join([a.Name for a in apps.all()])
        return returnstring


class ITGroup(models.Model):
    Name = models.CharField(max_length=255)
    TechnicalOwnerContacts = models.ManyToManyField('TechnicalOwnerContact', blank=True)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "itgroup"

class ProjectTask(models.Model):
    Name = models.CharField(max_length=255)
    Project = models.ForeignKey('Project', null=True, blank=True)
    Description = models.TextField(blank=True, null=True)
    Finished = models.BooleanField(default=False)
    StartDate = models.DateField(blank=True, null=True)
    DueDate = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.Name

class Project(models.Model):
    Name = models.CharField(max_length=255)
    PMOSupported = models.BooleanField(default=False)
    ProjectManager = models.ManyToManyField(ProjectManager, blank=True)
    BusinessUnit = models.ManyToManyField(BusinessUnit, blank=True)
    ITGroup = models.ManyToManyField(ITGroup, blank=True)
    Description = models.TextField(blank=True, null=True)
    Finished = models.BooleanField(default=False)
    StartDate = models.DateField(blank=True, null=True)
    DueDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.Name

    def display_projectapplications(self):
        apps = Application.objects.filter(Projects=self)
        return ', '.join([a.Name for a in apps.all()])

    display_projectapplications.short_description = 'Applications for Project'
    display_projectapplications.allow_tags = True

    def display_projecttasks(self):
        tasks = ProjectTask.objects.filter(Project=self)
        return ', '.join(["<a href='" + reverse("admin:silkollect_projecttask_change", args=[i.id]) + "'>" + i.Name +
         "</a>" for i in tasks.all()])
    display_projecttasks.short_description = 'Tasks for Project'
    display_projecttasks.allow_tags = True

    class Meta:
        db_table = "project"
        ordering = ('Name',)


class ApplicationInterface(models.Model):
    Name = models.CharField(max_length=255)
    InterfaceType = models.ForeignKey(InterfaceType, blank=True, null=True)
    TransportType = models.ForeignKey(TransportType, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    IncomingApplication = models.ForeignKey(Application, blank=True, null=True, related_name='IncomingInterface')
    OutgoingApplication = models.ForeignKey(Application, blank=True, null=True, related_name='OutgoingInterface')
    InterfaceDirection = models.ForeignKey(InterfaceDirection, blank=True, null=True)
    TechnicalOwnerContacts = models.ManyToManyField(TechnicalOwnerContact, blank=True)
    BusinessOwnerContacts = models.ManyToManyField(BusinessOwnerContact, blank=True)
    EndUserContacts = models.ManyToManyField(EndUserContact, blank=True)
    ProjectLeads = models.ManyToManyField(ProjectLead, blank=True)
    FunctionalArea = models.ManyToManyField(FunctionalArea, blank=True)

    # Attachment = models.FileField(blank=True)
    def __str__(self):
        retstring = str(self.Name)
        if self.InterfaceDirection != None and self.InterfaceDirection != '':
            retstring = retstring + ', Direction: ' + str(self.InterfaceDirection)
        # if self.Description != None and self.Description != '':
        #    retstring = retstring +  ', Description: ' + str(self.Description)
        return retstring

    class Meta:
        db_table = "applicationinterface"


class Server(models.Model):
    ShortDescription = models.CharField(max_length=255)
    IPAddress = models.CharField(max_length=255, blank=True, null=True)
    ComputerName = models.CharField(max_length=255, blank=True, null=True)
    OperatingSystem = models.ForeignKey('OperatingSystem', blank=True, null=True)
    Storage = models.CharField(max_length=255, blank=True, null=True)
    RAM = models.CharField(max_length=255, blank=True, null=True)
    Site = models.ForeignKey(Site, blank=True, null=True)
    Network = models.ForeignKey('Network', blank=True, null=True)
    ServiceAccounts = models.ManyToManyField('ServiceAccount', blank=True)
    HardwareType = models.ForeignKey('HardwareType', blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        retstr = self.ShortDescription
        if self.ComputerName != None and self.ComputerName != '':
            retstr += ' (' + self.ComputerName + ')'
        return retstr

    class Meta:
        db_table = "server"


class ServerType(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "servertype"


class HardwareType(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "hardwaretype"


class ServerRole(models.Model):
    Server = models.ForeignKey(Server)
    ServerType = models.ForeignKey(ServerType)
    Shared = models.NullBooleanField()
    DatabaseType = models.ForeignKey(DatabaseType, blank=True, null=True)
    ApplicationEnvironment = models.ForeignKey('ApplicationEnvironment', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        # retstr = 'Server: ' + str(self.Server) + ', Type: ' + str(self.ServerType)
        # if self.ApplicationEnvironment != None:
        #    retstr += ', Environment: ' + str(self.ApplicationEnvironment)
        # return retstr
        return str(self.Server.ShortDescription)

    @property
    def Name(self):
        retstring = self.Server.ShortDescription
        if retstring == None or retstring == '':
            retstring = self.Server.IPAddress
        return retstring

    class Meta:
        db_table = "serverrole"
        ordering = ['Server__ComputerName']

    def display_AssignedApplications(self):
        apps = Application.objects.filter(ServerRoles=self)
        return ', '.join(
            ["<a href='" + reverse("admin:silkollect_application_change", args=[i.id]) + "'>" + i.Name +
             "</a>" for i in apps.all()])
    display_AssignedApplications.short_description = 'Assigned Applications'
    display_AssignedApplications.allow_tags = True

class ServiceAccount(models.Model):
    Name = models.CharField(max_length=255)
    Password = models.CharField(max_length=255, blank=True, null=True)
    AccountType = models.ForeignKey('ServiceAccountType', blank=True)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "serviceaccount"


class ServiceAccountType(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "serviceaccounttype"


class OperatingSystem(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "operatingsystem"


class ApplicationEnvironment(models.Model):
    Name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.Name

    class Meta:
        db_table = "applicationenvironment"


class Network(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "network"


class RegulatoryType(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']
        db_table = "regulatorytype"


#class DispositionType(models.Model):
#    Name = models.CharField(max_length=255)

    #def __str__(self):
     #   return self.Name

    #class Meta:
     #   ordering = ['Name']
      #  db_table = "dispositiontype"


class ApplicationRole(models.Model):
    Name = models.CharField(max_length=255)
    #BusinessCapabilities = models.ManyToManyField('BusinessCapability', blank=True)
    ITCapabilities = models.ManyToManyField('ITCapability', blank=True)
    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']
        db_table = "applicationrole"

    def display_ITCapabilities(self):
        return ', '.join(["<a href='" + reverse("admin:silkollect_itcapability_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in self.ITCapabilities.all()])
    display_ITCapabilities.short_description = 'Assigned IT Capabilities'
    display_ITCapabilities.allow_tags = True

    def display_BusinessCapabilities(self):
        bcaps = []
        for icap in self.ITCapabilities.all():
            for bcap in icap.BusinessCapabilities.all():
                bcaps.append(bcap)
        return ', '.join(["<a href='" + reverse("admin:silkollect_businesscapability_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in bcaps])
    display_BusinessCapabilities.short_description = 'Assigned Business Capabilities'
    display_BusinessCapabilities.allow_tags = True

    def display_AssignedApplications(self):
        apps = Application.objects.filter(ApplicationRoles=self)
        return ', '.join(["<a href='" + reverse("admin:silkollect_application_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in apps.all()])
    display_AssignedApplications.short_description = 'Assigned Applications'
    display_AssignedApplications.allow_tags = True

# Risk Register Items
class RiskEntry(models.Model):
    Value_Choices = (
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Very High')
    )
    ProbabilityRating = models.IntegerField(choices=Value_Choices, null=True, blank=True)
    ImpactRating = models.IntegerField(choices=Value_Choices, null=True, blank=True)
    Name = models.CharField(max_length=255)
    Description = models.TextField(blank=True, null=True)
    Applications = models.ManyToManyField(Application, blank=True)
    DatabaseType = models.ForeignKey(DatabaseType, blank=True, null=True)
    TechnologyClassifications = models.ManyToManyField('TechnologyClassification', blank=True)
    ArchitecturePillars = models.ManyToManyField('ArchitecturePillar', blank=True)
    ViolatedPrinciples = models.ManyToManyField('ArchitecturePrinciple', blank=True)
    ViolatedStandards = models.ManyToManyField('ArchitectureStandard', blank=True)
    ViolatedStrategies = models.ManyToManyField('ITStrategy', blank=True)
    # DispensationEntries = models.ManyToManyField('DispensationEntry', blank=True)
    Satisfied = models.BooleanField(default=False)
    SatisfiedDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']
        db_table = "riskentry"

    def display_riskapplications(self):
        apps = []
        for app in self.Applications.all():
            apps.append(app)
        #walk through the implied ones now.
        if self.DatabaseType is not None:
            for app in Application.objects.all():
                for srole in app.ServerRoles.all():
                    if srole.DatabaseType == self.DatabaseType:
                        #pass
                        apps.append(app)
        return ', '.join(["<a href='" + reverse("admin:silkollect_application_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in apps])
    def display_riskdatabasetype(self):
        return self.DatabaseType
    display_riskdatabasetype.short_description = 'DatabaseType'

    def show_change_url(self):
        return "<a href='" + reverse("admin:silkollect_riskentry_change", args=[self.id]) + "'>" + self.Name + "</a>"
    display_riskapplications.short_description = 'Applications'
    display_riskapplications.allow_tags = True

    def display_strategies(self):
        #format_html("<a href='{url}'>" + r.Name + "</a>", url=reverse("admin:silkollect_riskentry_change", args=[r.id]))
        return ', '.join(["<a href='" + reverse("admin:silkollect_itstrategy_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in self.ViolatedStrategies.all()])
    display_strategies.short_description = 'Violated Strategies'
    display_strategies.allow_tags = True
    def display_principles(self):
        return ', '.join(["<a href='" + reverse("admin:silkollect_architectureprinciple_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in self.ViolatedPrinciples.all()])
    display_principles.short_description = 'Violated Principles'
    display_principles.allow_tags = True
    def display_pillars(self):
        return ', '.join(["<a href='" + reverse("admin:silkollect_architecturepillar_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in self.ArchitecturePillars.all()])
    display_pillars.short_description = 'Affected Architecture Pillars'
    display_pillars.allow_tags = True

    def display_Satisfied(self):
        if self.Satisfied:
            return 'Satisfied: ' + str(self.SatisfiedDate)
        else:
            return ''
    display_Satisfied.short_description= 'Satisfied?'
    def display_Dispensations(self):
        disps = DispensationEntry.objects.filter(RiskEntry = self)
        return ', '.join(["<a href='" + reverse("admin:silkollect_dispensationentry_change", args=[i.id]) + "'>" + i.Name +
                   "</a>" for i in disps.all()])

    display_Dispensations.short_description = 'Dispensations'
    display_Dispensations.allow_tags = True

    def display_DispensationDates(self):
        disps = DispensationEntry.objects.filter(RiskEntry = self)
        return ', '.join(["<a href='" + reverse("admin:silkollect_dispensationentry_change", args=[i.id]) + "'>" + str(i.DispensationDueDate) +
                   "</a>" for i in disps.all()])

    display_DispensationDates.short_description = 'Dispensation Date'
    display_DispensationDates.allow_tags = True

    def display_affectedbusinesscapabilities(self):
        totalicaps = []
        totalbcaps = []
        for a in self.Applications.all():
            for approle in a.ApplicationRoles.all():
                if approle is not None:
                    for itcap in approle.ITCapabilities.all():
                        if itcap not in totalicaps:
                            totalicaps.append(itcap)
                        for bcap in itcap.BusinessCapabilities.all():
                            if bcap not in totalbcaps:
                                totalbcaps.append(bcap)
        return ', '.join(["<a href='" + reverse("admin:silkollect_businesscapability_change", args=[i.id]) + "'>" + i.Name +
                          "</a>" for i in totalbcaps])
    display_affectedbusinesscapabilities.short_description = 'Affected Business Capabilities'
    display_affectedbusinesscapabilities.allow_tags = True

class DispensationEntry(models.Model):
    Name = models.CharField(max_length=255,null=True, blank=True)
    Value_Choices = (
        (1, 'Open'),
        (2, 'Closed, No new Dispensation'),
        (3, 'Closed, New Dispensation'),
    )
    Finding = models.TextField(blank=True, null=True)
    DispensationDueDate = models.DateField()
    Disposition = models.IntegerField(choices=Value_Choices, null=True, blank=True)
    RiskEntry = models.ForeignKey(RiskEntry, blank=True, null=True)

    def __str__(self):
        return str(self.DispensationDueDate) + '; ' + self.Finding[:50]

    class Meta:
        ordering = ['DispensationDueDate']
        db_table = "dispensationentry"

    def display_riskapplications(self):
        return ', '.join([str(i) for i in self.RiskEntry.Applications.all()])

    display_riskapplications.short_description = 'Applications'
    display_riskapplications.allow_tags = True

    def display_RiskEntry(self):
        if self.RiskEntry is not None:
            return "<a href='" + reverse("admin:silkollect_riskentry_change",
                                         args=[self.RiskEntry.id]) + "'>" + self.RiskEntry.Name + "</a>"
        else:
            return None
    display_RiskEntry.short_description = 'Risk Entry'
    display_RiskEntry.allow_tags = True


class TechnologyClassification(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']
        db_table = "technologyclassification"


class ArchitectureContact(models.Model):
    Contact = models.OneToOneField('Contact')

    def __str__(self):
        return str(self.Contact)

    class Meta:
        ordering = ['Contact__Name']
        db_table = "architecturecontact"

    @property
    def Name(self):
        return self.Contact.Name


class ArchitecturePillar(models.Model):
    Name = models.CharField(max_length=255)
    ArchitectureContacts = models.ManyToManyField('ArchitectureContact', blank=True)

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']
        db_table = "architecturepillar"


class ArchitecturePrinciple(models.Model):
    Name = models.CharField(max_length=255)
    ArchitecturePillar = models.ForeignKey('ArchitecturePillar', null=True, blank=True)
    Statement = models.TextField(blank=True, null=True)
    Rationale = models.TextField(blank=True, null=True)
    #   Implications = models.ManyToManyField('PrincipleImplication', blank=True)
    Implications = models.TextField(blank=True, null=True)
    Source = models.CharField(max_length=255, blank=True, null=True)
    ApprovalRecord = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.ArchitecturePillar != None:
            return '(' + self.ArchitecturePillar.Name + ') ' + self.Name
        else:
            return self.Name

    class Meta:
        ordering = ['Name']
        db_table = "architectureprinciple"


class ArchitectureStandard(models.Model):
    Name = models.CharField(max_length=255)

    # Attachment = models.ForeignKey('ArchitectureStandardAttachment', null=True,blank=True)
    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']
        db_table = "architecturestandard"


class ITStrategy(models.Model):
    Name = models.CharField(max_length=255)

    # Attachment = models.ForeignKey('ITStrategyAttachment', null=True,blank=True)
    def __str__(self):
        return self.Name

    class Meta:
        ordering = ['Name']
        db_table = "itstrategy"

class RecoveryObjective(models.Model):
    Name = models.CharField(max_length=255)
    def __str__(self):
        return self.Name
    class Meta:
        ordering = ['Name']