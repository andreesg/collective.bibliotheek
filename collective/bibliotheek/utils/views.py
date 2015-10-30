#!/usr/bin/python
# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from collective.bibliotheek import MessageFactory as _
from plone.dexterity.browser.view import DefaultView
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
from zope.interface import alsoProvides
from .interfaces import IFormWidget
from plone.dexterity.browser.edit import DefaultEditForm
from collective.z3cform.datagridfield.interfaces import IDataGridField
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# # # # # # # # # # # # #
# View specific methods #
# # # # # # # # # # # # #

class BookView(DefaultView):
    """ View class """

    template = ViewPageTemplateFile('../bibliotheek_templates/view.pt')

    def checkUserPermission(self):
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self.context):
            return True
        return False
