#!/usr/bin/python
# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone.dexterity.browser.view import DefaultView


from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from collective.bibliotheek import MessageFactory as _
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
from zope.interface import alsoProvides
from .interfaces import IFormWidget
from plone.dexterity.browser.edit import DefaultEditForm
from collective.z3cform.datagridfield.interfaces import IDataGridField
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from Acquisition import aq_inner
from zc.relation.interfaces import ICatalog

# # # # # # # # # # # # #
# View specific methods #
# # # # # # # # # # # # #

class LibraryView(DefaultEditForm):
    """ View class """

    template = ViewPageTemplateFile('../bibliotheek_templates/library_view.pt')

    def update(self):
        super(LibraryView, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

    def checkUserPermission(self):
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self.context):
            return True
        return False

    def getRelatedObjects(self):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)

        source_object = self.context

        relations = catalog.findRelations(
            dict(to_id=intids.getId(aq_inner(source_object)),
                from_attribute="documentation_documentation")
        )

        structure = ""
        for rel in list(relations):
            from_object = rel.from_object
            title = getattr(from_object, 'title', '')
            obj_number = getattr(from_object, 'identification_identification_objectNumber', '')
            url = from_object.absolute_url()
            structure += "<p><a href='%s'><span>%s</span> - <span>%s</span></a></p>" %(url, obj_number, title)

        return structure

class BookView(DefaultEditForm):
    """ View class """

    template = ViewPageTemplateFile('../bibliotheek_templates/view.pt')

    def update(self):
        super(BookView, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

    def checkUserPermission(self):
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self.context):
            return True
        return False

