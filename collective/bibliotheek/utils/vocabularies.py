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

def _createSubjectTypeVocabulary():
    
    names = {
        "object name": _(u"object name"),
        "animal": _(u"animal"),
        "plant": _(u"plant"),
        "activity": _(u"activity"),
        "event": _(u"event"),
        "subject": _(u"subject"),
        "concept": _(u"concept"),
        "people": _(u"people"),
        "cultural affinity": _(u"cultural affinity"),
        "category": _(u"category")
    }

    terms = []
    terms.append(SimpleTerm(value="No value", token=str("No value"), title=u" "))

    for key, name in names.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        terms.append(term)
    
    return terms

class createSubjectTypeVocabulary(object):
    
    implements(IVocabularyFactory)
  
    def __init__(self):
        pass

    def __call__(self, context):

        names = {
            "object name": _(u"object name"),
            "animal": _(u"animal"),
            "plant": _(u"plant"),
            "activity": _(u"activity"),
            "event": _(u"event"),
            "subject": _(u"subject"),
            "concept": _(u"concept"),
            "people": _(u"people"),
            "cultural affinity": _(u"cultural affinity"),
            "category": _(u"category")
        }

        terms = []
        terms.append(SimpleTerm(value="No value", token=str("No value"), title=u" "))

        for key, name in names.items():
            term = SimpleTerm(value=key, token=str(key), title=name)
            terms.append(term)
        
        return SimpleVocabulary(terms)



priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))

class ATVMVocabulary(object):
    implements(IVocabularyFactory)
    def __init__(self, name):
        self.name = name

    def __call__(self, context):
        portal = getSite()
        try:
            atvm = getToolByName(portal, 'portal_vocabularies')
            units = atvm.getVocabularyByName(self.name)
            terms = []
        except:
            units = []
            terms = []
            pass

        for term in units:
            if units[term]:
                terms.append(SimpleVocabulary.createTerm(
                    term, term.encode('utf-8'), _(units[term].title)))

        return SimpleVocabulary(terms)

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
GeokeywordVocabularyFactory = ObjectVocabulary('abstractAndSubjectTerms_geographicalKeyword')
LoanVocabularyFactory = ObjectVocabulary('copiesAndShelfMarks_copyDetails_loan')
SiteVocabularyFactory = ObjectVocabulary('copiesAndShelfMarks_copyDetails_site')
SubjectTypeVocabularyFactory = ObjectVocabulary('abstractAndSubjectTerms_subjectTerm_subjectType')
PropernameVocabularyFactory = ObjectVocabulary('abstractAndSubjectTerms_subjectTerm_properName')


PlacePrintedVocabularyFactory = ObjectVocabulary('titleAuthorImprintCollation_imprint_placesPrinted')
SubjectTermTypeVocabularyFactory = ATVMVocabulary('SubjectTermType')
ObjectStatusVocabularyFactory = ATVMVocabulary('ObjectStatus')
PersonKeywordTypeVocabularyFactory = ATVMVocabulary('PersonKeywordType')
subjecttype_vocabulary = createSubjectTypeVocabulary()
