import csv

import CSVExporter
from django.contrib import admin
from django.http import HttpResponse
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Suite, Application, DatabaseType, AuthenticationType, ApplicationType, \
    Site, InterfaceDirection, InterfaceType, ApplicationInterface, BusinessOwnerContact, TechnicalOwnerContact, \
    Project, ServerType, Server, ServerRole, ServiceAccount, ServiceAccountType, OperatingSystem, \
    ApplicationEnvironment, Network, ApplicationRole, DispositionType, RegulatoryType, HardwareType, \
    EndUserContact, Contact, ApplicationAttachment, GenericToDoItem, ToDoItem, Survey, SurveyAnswer, SurveyQuestion, \
    ProjectLead, ProjectManager, TechnicalOwnerContactAttachment, Vendor, UserBase, CostCenter, BusinessUnit, \
    ApplicationCategory, ApplicationRoadmap, SuiteRoadmap, Report, InformationSource, ITGroup, ArchitectureContact, \
    ArchitecturePillar, ArchitecturePrinciple, ArchitectureStandard, RiskEntry, DispensationEntry, ITStrategy, \
    TechnologyClassification, ITStrategyAttachment, ArchitectureStandardAttachment, TransportType, \
    InterfaceAttachment, FunctionalArea, BusinessGoal, BusinessGoalAttachment, PositionClass, PositionTitle, \
    BusinessUnitAttachment, BusinessStrategy, BusinessObjective, BusinessTactic, BusinessCapability, ITCapability, \
    ITService


class ApplicationAttachmentsInline(admin.TabularInline):
    model = ApplicationAttachment
    extra = 0
    inlines = []


class ApplicationIncomingInterfacesInline(admin.TabularInline):
    model = ApplicationInterface
    fk_name = 'IncomingApplication'
    fields = ('Name',)
    can_delete = False
    extra = 0
    inlines = []


class ApplicationOutgoingInterfacesInline(admin.TabularInline):
    model = ApplicationInterface
    fk_name = 'OutgoingApplication'
    fields = ('Name',)
    can_delete = False
    editable_fields = []
    extra = 0
    inlines = []


class TechnicalContentAttachmentsInline(admin.TabularInline):
    model = TechnicalOwnerContactAttachment
    extra = 0


class ToDoInline(admin.TabularInline):
    model = ToDoItem
    extra = 0
    inlines = []


class ApplicationRoadmapsInline(admin.TabularInline):
    model = ApplicationRoadmap
    extra = 0
    inlines = []


class SuiteRoadmapsInline(admin.TabularInline):
    model = SuiteRoadmap
    extra = 0
    inlines = []


def export_projects_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=silk_projects_export.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    CSVExporter.CSVExportProjects(queryset, writer)
    return response


export_projects_csv.short_description = u"Export Projects to CSV"


def export_applications_camplot_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=silk_applications_camplot.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    CSVExporter.CSVExportApplicationsCAMPlot(queryset, writer)
    return response


export_applications_camplot_csv.short_description = u"Export Applications to CSV, with TIME grading"


class SurveyQuestionInline(NestedStackedInline):
    model = SurveyQuestion
    fields = ('Question',)
    extra = 0


class SurveyInline(NestedStackedInline):
    inlines = [
        SurveyQuestionInline,
    ]
    model = Survey
    extra = 0


class ITStrategyAttachmentsInline(admin.TabularInline):
    model = ITStrategyAttachment
    extra = 0
    inlines = []


class BusinessGoalAttachmentsInline(admin.TabularInline):
    model = BusinessGoalAttachment
    extra = 0
    inlines = []


class BusinessUnitAttachmentsInline(admin.TabularInline):
    model = BusinessUnitAttachment
    extra = 0
    inlines = []


class InterfaceAttachmentsInline(admin.TabularInline):
    model = InterfaceAttachment
    extra = 0
    inlines = []


class ITStrategyAdmin(NestedModelAdmin):
    inlines = [
        ITStrategyAttachmentsInline
    ]


class ArchitectureStandardAttachmentsInline(admin.TabularInline):
    model = ArchitectureStandardAttachment
    extra = 0
    inlines = []


class ArchitectureStandardAdmin(NestedModelAdmin):
    inlines = [
        ArchitectureStandardAttachmentsInline
    ]


class FunctionalAreaAdmin(NestedModelAdmin):
    list_display = ('Name', 'BusinessOwners')
    filter_horizontal = ('BusinessOwnerContacts',)

    def BusinessOwners(self, obj):
        return "\n".join([i.Name for i in obj.BusinessOwnerContacts.all()])


class ApplicationInterfaceAdmin(NestedModelAdmin):
    list_display = (
        'Name', 'InterfaceType', 'TransportType', 'InterfaceDirection', 'IncomingApplication', 'OutgoingApplication')
    search_fields = ('IncomingApplication__Name', 'OutgoingApplication__Name')
    filter_horizontal = (
        'EndUserContacts', 'TechnicalOwnerContacts', 'BusinessOwnerContacts', 'ProjectLeads', 'FunctionalArea')
    inlines = [
        InterfaceAttachmentsInline
    ]


class BusinessTacticInline(admin.TabularInline):
    model = BusinessTactic


class BusinessTacticAdmin(NestedModelAdmin):
    list_display = ('Name', 'BusinessUnit', 'display_BusinessStrategies',
                    'display_BusinessObjectives', 'display_BusinessGoals')
    filter_horizontal = ('BusinessStrategies',)


class BusinessObjectiveInline(admin.TabularInline):
    model = BusinessObjective
    inlines = [
        BusinessTacticInline,
    ]


class BusinessObjectiveAdmin(NestedModelAdmin):
    list_display = ('Name', 'BusinessUnit', 'display_BusinessGoals', 'display_BusinessStrategies')
    filter_horizontal = ('BusinessGoals',)


class BusinessStrategyInline(admin.TabularInline):
    model = BusinessStrategy
    inlines = [
        BusinessObjectiveInline,
    ]
    extra = 0


class BusinessStrategyAdmin(NestedModelAdmin):
    list_display = ('Name', 'BusinessUnit', 'display_BusinessObjectives')
    filter_horizontal = ('BusinessObjectives',)


class BusinessGoalAdmin(NestedModelAdmin):
    list_display = ('Name', 'Year', 'BusinessUnit', 'display_BusinessObjectives',
                    'display_BusinessStrategies', 'display_BusinessTactics')
    inlines = [
        BusinessGoalAttachmentsInline,  # BusinessStrategyInline
    ]


class BusinessCapabilityAdmin(NestedModelAdmin):
    list_display = ('Name', 'Level', 'BusinessCapabilityParent')


class ITCapabilityAdmin(NestedModelAdmin):
    list_display = ('Name', 'Level', 'ITCapabilityParent')


class ITServiceAdmin(NestedModelAdmin):
    list_display = ('Name', 'display_ITCapabilities')


class ApplicationRoleAdmin(NestedModelAdmin):
    list_display = ('Name', 'display_BusinessCapabilities')
    filter_horizontal = ('BusinessCapabilities',)


class ApplicationAdmin(NestedModelAdmin):
    list_display = ('Name', 'display_TechnicalIntegrity', 'display_BusinessValue', 'DispositionType', 'BusinessUnit',
                    'display_ITServices', 'display_TechnicalOwnerContacts',
                    'display_RiskEntries',)  # 'display_applicationtodo' )
    search_fields = ('Name',)
    ordering = ('Name',)
    filter_horizontal = (
        'ITServices', 'ServerRoles', 'EndUserContacts', 'TechnicalOwnerContacts', 'BusinessOwnerContacts',
        'ProjectLeads',
        'UserBases', 'Dependencies')
    inlines = [
        ApplicationAttachmentsInline, ToDoInline, ApplicationRoadmapsInline, ApplicationOutgoingInterfacesInline,
        ApplicationIncomingInterfacesInline,
        # , SurveyInline
    ]
    actions = [export_applications_camplot_csv, ]
    list_filter = (('DispositionType', admin.RelatedOnlyFieldListFilter),
                   ('BusinessUnit', admin.RelatedOnlyFieldListFilter),
                   'technical_integrity',
                   'business_value',
                   )


class SurveyAnswerInline(admin.TabularInline):
    model = SurveyAnswer


class SurveyQuestionAdmin(admin.ModelAdmin):
    search_fields = ('Survey__Application__Name',)
    inlines = [
        SurveyAnswerInline
    ]


class SurveyAdmin(admin.ModelAdmin):
    pass
    # inlines = [
    #   SurveyQuestionInline
    # ]


class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('Question', 'Answer', 'Answerer')
    # list_display=('display_survey',)


class ServerAdmin(admin.ModelAdmin):
    filter_horizontal = ('ServiceAccounts',)


class AppsInlineSuiteAdmin(admin.TabularInline):
    model = Application
    extra = 0
    fields = ('Name',)
    can_delete = False
    readonly_fields = ('Name',)


class ReportAdmin(admin.ModelAdmin):
    ordering = ('Name',)
    filter_horizontal = ('TechnicalOwnerContacts', 'BusinessOwnerContacts', 'ProjectLeads', 'EndUserContacts')


class SuiteAdmin(admin.ModelAdmin):
    list_display = ('Name', 'display_suiteapplications')
    ordering = ('Name',)
    filter_horizontal = ('TechnicalOwnerContacts', 'BusinessOwnerContacts', 'ProjectLeads')
    inlines = [
        AppsInlineSuiteAdmin, SuiteRoadmapsInline
    ]


class ITGroupAdminInline(NestedStackedInline):
    model = ITGroup
    fields = ('ITGroup',)
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'Name', 'Finished', 'PMOSupported', 'Project_Manager', 'StartDate', 'DueDate', 'IT_Groups', 'Business_Units',
        'display_projectapplications')
    ordering = ('Finished', 'DueDate', 'Name',)

    def Project_Manager(self, obj):
        return "\n".join([m.Name for m in obj.ProjectManager.all()])

    def IT_Groups(self, obj):
        return "\n".join([g.Name for g in obj.ITGroup.all()])

    def Business_Units(self, obj):
        return "\n".join([u.Name for u in obj.BusinessUnit.all()])

    actions = [export_projects_csv, ]


class AppsInlineBusinessOwnerContact(admin.TabularInline):
    model = Application.BusinessOwnerContacts.through


class BusinessOwnerContactAdmin(admin.ModelAdmin):
    list_display = ('Name',)
    search_fields = ('Contact__Name',)
    inlines = [
        AppsInlineBusinessOwnerContact,
    ]


class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ('Name', 'BusinessUnitParent', 'BusinessOwnerContact', 'Title')
    search_fields = ('Name',)
    inlines = [
        BusinessUnitAttachmentsInline
    ]

    def Title(self, obj):
        if obj.BusinessOwnerContact is not None:
            return obj.BusinessOwnerContact.Contact.PositionTitle
        else:
            return None


class AppsInlineProjectLead(admin.TabularInline):
    model = Application.ProjectLeads.through
    extra = 0


class AppsInlineProjectManager(admin.TabularInline):
    model = Project.ProjectManager.through
    extra = 0


class ProjectLeadAdmin(admin.ModelAdmin):
    list_display = ('Name',)
    search_fields = ('Contact__Name',)
    inlines = [
        AppsInlineProjectLead,
    ]


class ProjectManagerAdmin(admin.ModelAdmin):
    list_display = ('Name',)
    search_fields = ('Contact__Name',)
    inlines = [
        AppsInlineProjectManager,
    ]


class AppsInlineTechContact(admin.TabularInline):
    model = Application.TechnicalOwnerContacts.through


class TechnicalOwnerContactAdmin(admin.ModelAdmin):
    list_display = ('Name',)
    search_fields = ('Contact__Name',)
    inlines = [
        AppsInlineTechContact, TechnicalContentAttachmentsInline
    ]


class ToDoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.GenericToDoItem is not None:
            obj.Name = obj.GenericToDoItem.Name
        obj.save()


class ContactAdmin(admin.ModelAdmin):
    list_display = ('Name', 'PositionTitle', 'PositionClass')
    search_fields = ('Name',)


class DispensationInline(admin.TabularInline):
    model = DispensationEntry
    extra = 0
    inlines = []


class RiskAdmin(admin.ModelAdmin):
    list_display = ('Name', 'display_riskapplications')
    inlines = [
        DispensationInline,
    ]


class DispensationAdmin(admin.ModelAdmin):
    list_display = ('RiskEntry', 'Finding', 'display_riskapplications', 'Disposition',
                    'DispensationDueDate')


# Register your models here.


admin.site.register(ArchitectureContact)
admin.site.register(ArchitecturePillar)
admin.site.register(ArchitecturePrinciple)
admin.site.register(ArchitectureStandard, ArchitectureStandardAdmin)
admin.site.register(RiskEntry, RiskAdmin)
admin.site.register(DispensationEntry, DispensationAdmin)
admin.site.register(ITStrategy, ITStrategyAdmin)
admin.site.register(TechnologyClassification)
admin.site.register(ArchitectureStandardAttachment)
admin.site.register(ITStrategyAttachment)
admin.site.register(InterfaceAttachment)
admin.site.register(FunctionalArea, FunctionalAreaAdmin)
admin.site.register(ITGroup)
admin.site.register(InformationSource)
admin.site.register(Report, ReportAdmin)
admin.site.register(ApplicationCategory)
admin.site.register(CostCenter)
admin.site.register(ApplicationRoadmap)
admin.site.register(SuiteRoadmap)
admin.site.register(BusinessUnit, BusinessUnitAdmin)
admin.site.register(UserBase)
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyAnswer, SurveyAnswerAdmin)
admin.site.register(ApplicationAttachment)
admin.site.register(TechnicalOwnerContactAttachment)
admin.site.register(GenericToDoItem)
admin.site.register(ToDoItem, ToDoAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(EndUserContact)
admin.site.register(HardwareType)
admin.site.register(ApplicationRole, ApplicationRoleAdmin)
admin.site.register(DispositionType)
admin.site.register(RegulatoryType)
admin.site.register(Network)
admin.site.register(ApplicationEnvironment)
admin.site.register(ServerType)
admin.site.register(OperatingSystem)
admin.site.register(Server, ServerAdmin)
admin.site.register(ServerRole)
admin.site.register(ServiceAccount)
admin.site.register(ServiceAccountType)
admin.site.register(Suite, SuiteAdmin)
admin.site.register(DatabaseType)
admin.site.register(AuthenticationType)
admin.site.register(ApplicationType)
admin.site.register(Site)
admin.site.register(Vendor)
admin.site.register(Project, ProjectAdmin)
admin.site.register(InterfaceDirection)
admin.site.register(InterfaceType)
admin.site.register(TransportType)
admin.site.register(ApplicationInterface, ApplicationInterfaceAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(BusinessOwnerContact, BusinessOwnerContactAdmin)
admin.site.register(TechnicalOwnerContact, TechnicalOwnerContactAdmin)
admin.site.register(ProjectLead, ProjectLeadAdmin)
admin.site.register(ProjectManager, ProjectManagerAdmin)
admin.site.register(BusinessGoal, BusinessGoalAdmin)
admin.site.register(PositionTitle)
admin.site.register(PositionClass)
admin.site.register(BusinessObjective, BusinessObjectiveAdmin)
admin.site.register(BusinessStrategy, BusinessStrategyAdmin)
admin.site.register(BusinessTactic, BusinessTacticAdmin)
admin.site.register(BusinessCapability, BusinessCapabilityAdmin)
admin.site.register(ITCapability, ITCapabilityAdmin)
admin.site.register(ITService, ITServiceAdmin)
