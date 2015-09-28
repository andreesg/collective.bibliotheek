#!/usr/bin/python
# -*- coding: utf-8 -*-


from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter
from plone.app.widgets.dx import AjaxSelectFieldWidget

from plone.app.content.interfaces import INameFromTitle
from plone.dexterity.interfaces import IDexterityContainer
from zope.component import adapts

#
# Plone dependencies
#
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#
# z3c.forms dependencies
#
from z3c.form import group, field
from z3c.form.form import extends
from z3c.form.browser.textlines import TextLinesFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
#from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.autoform.interfaces import IFormFieldProvider
from .utils.source import ObjPathSourceBinder

#
# plone.app.widgets dependencies
#
from plone.app.widgets.dx import DatetimeFieldWidget, RelatedItemsFieldWidget

#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow, IDataGridField
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory


# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit

# # # # # # # # # # # # # # # # # #
# !Bibliotheek specific imports!   #
# # # # # # # # # # # # # # # # # #
from collective.bibliotheek import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *


class ICommonLibrary(model.Schema):
    
    # # # # # # # # # # # # # # # # # # # # # # # #
    # Abstract and subject terms fieldset         #
    # # # # # # # # # # # # # # # # # # # # # # # #
    
    pass


alsoProvides(ICommonLibrary, IFormFieldProvider)

class CommonLibrary(Container):
    implements(ICommonLibrary)
    adapts(IDexterityContainer)

    def __init__(self, context):
        self.context = context

