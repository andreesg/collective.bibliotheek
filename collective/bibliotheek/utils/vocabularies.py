#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from collective.bibliotheek import MessageFactory as _
from zope.schema.interfaces import ISource, IContextSourceBinder, IVocabularyFactory
from zope.component.hooks import getSite
from Products.CMFPlone.utils import safe_unicode
from zope.interface import implements, classProvides
from Products.CMFCore.utils import getToolByName
from binascii import b2a_qp

# # # # # # # # # # # # # #
# Vocabularies            #
# # # # # # # # # # # # # #

def _createInsuranceTypeVocabulary():
    insurance_types = {
        "commercial": _(u"Commercial"),
        "indemnity": _(u"Indemnity"),
    }

    for key, name in insurance_types.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createPriorityVocabulary():
    priorities = {
        "low": _(u"low"),
        "medium": _(u"medium"),
        "high": _(u"high"),
        "urgent": _(u"urgent")
    }

    for key, name in priorities.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))

class ObjectVocabulary(object):

    implements(IVocabularyFactory)

    def __init__(self, index):
        self.index = index

    def __call__(self, context, query=None):
        self.context = context
        
        site = getSite()
        self.catalog = getToolByName(site, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex(self.index)
        
        def safe_encode(term):
            if isinstance(term, unicode):
                # no need to use portal encoding for transitional encoding from
                # unicode to ascii. utf-8 should be fine.
                term = term.encode('utf-8')
            return term

        items = [
            SimpleTerm(i, b2a_qp(safe_encode(i)), safe_unicode(i))
            for i in index._index
            if type(i) != list and (query is None or safe_encode(query) in safe_encode(i))
        ]

        return SimpleVocabulary(items)


RoleVocabularyFactory = ObjectVocabulary('titleAuthorImprintCollation_titleAuthor_author_role')
SeriesVocabularyFactory = ObjectVocabulary('seriesNotesISBN_series_series_series')
SubseriesVocabularyFactory = ObjectVocabulary('seriesNotesISBN_series_subseries_subseries')
BiblformVocabularyFactory = ObjectVocabulary('abstractAndSubjectTerms_biblForm')
MaterialtypeVocabularyFactory = ObjectVocabulary('abstractAndSubjectTerms_materialType')
LanguageVocabularyFactory = ObjectVocabulary('abstractAndSubjectTerms_language')
ClassnumberVocabularyFactory = ObjectVocabulary('abstractAndSubjectTerms_classNumber')
