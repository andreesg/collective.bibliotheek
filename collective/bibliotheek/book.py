#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Zope dependencies
#
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter

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

from .utils.source import ObjPathSourceBinder

#
# plone.app.widgets dependencies
#
from plone.app.widgets.dx import DatetimeFieldWidget, RelatedItemsFieldWidget

#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
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

# # # # # # # # # # # # #
# # # # # # # # # # # # #
# Book schema           #
# # # # # # # # # # # # #
# # # # # # # # # # # # #

class IBook(form.Schema):

    priref = schema.TextLine(
        title=_(u'priref'),
        required=False
    )
    dexteritytextindexer.searchable('priref')

    text = RichText(
        title=_(u"Body"),
        required=False
    )

    # # # # # # # # # # # # # # # # # # # # # # # #
    # Title, author, imprint, collation fieldset  #
    # # # # # # # # # # # # # # # # # # # # # # # #
    
    model.fieldset('title_author', label=_(u'Title, author, imprint, collation'), 
        fields=['titleAuthorImprintCollation_titleAuthor_article', 'titleAuthorImprintCollation_titleAuthor_title',
                'titleAuthorImprintCollation_titleAuthor_statementOfRespsib', 'titleAuthorImprintCollation_titleAuthor_author',
                'titleAuthorImprintCollation_titleAuthor_illustrator',
                'titleAuthorImprintCollation_titleAuthor_corpAuthor', 'titleAuthorImprintCollation_edition_edition',
                'titleAuthorImprintCollation_imprint_place', 'titleAuthorImprintCollation_imprint_publisher',
                'titleAuthorImprintCollation_imprint_year', 'titleAuthorImprintCollation_imprint_placePrinted',
                'titleAuthorImprintCollation_imprint_printer', 'titleAuthorImprintCollation_sortYear_sortYear',
                'titleAuthorImprintCollation_collation_pagination', 'titleAuthorImprintCollation_collation_illustrations',
                'titleAuthorImprintCollation_collation_dimensions', 'titleAuthorImprintCollation_collation_accompanyingMaterial']
    )

    titleAuthorImprintCollation_titleAuthor_article = schema.TextLine(
        title=_(u'Article'),
        required=False
    )
    dexteritytextindexer.searchable('titleAuthorImprintCollation_titleAuthor_article')

    titleAuthorImprintCollation_titleAuthor_title = ListField(title=_(u'Title'),
        value_type=DictRow(title=_(u'Title'), schema=ITitle),
        required=False)
    form.widget(titleAuthorImprintCollation_titleAuthor_title=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('titleAuthorImprintCollation_titleAuthor_title')

    titleAuthorImprintCollation_titleAuthor_statementOfRespsib = schema.TextLine(
        title=_(u'Statement of respsib.'),
        required=False
    )
    dexteritytextindexer.searchable('titleAuthorImprintCollation_titleAuthor_statementOfRespsib')

    titleAuthorImprintCollation_titleAuthor_author = ListField(title=_(u'Author'),
        value_type=DictRow(title=_(u'Author'), schema=IAuthor),
        required=False)
    form.widget(titleAuthorImprintCollation_titleAuthor_author=DataGridFieldFactory)
    dexteritytextindexer.searchable('titleAuthorImprintCollation_titleAuthor_author')

    titleAuthorImprintCollation_titleAuthor_illustrator = ListField(title=_(u'Illustrator'),
        value_type=DictRow(title=_(u'Illustrator'), schema=IIllustrator),
        required=False)
    form.widget(titleAuthorImprintCollation_titleAuthor_illustrator=DataGridFieldFactory)
    dexteritytextindexer.searchable('titleAuthorImprintCollation_titleAuthor_illustrator')

    titleAuthorImprintCollation_titleAuthor_corpAuthor = schema.TextLine(
        title=_(u'Corp.author'),
        required=False
    )
    dexteritytextindexer.searchable('titleAuthorImprintCollation_titleAuthor_corpAuthor')

    # Edition
    titleAuthorImprintCollation_edition_edition = schema.TextLine(
        title=_(u'Edition'),
        required=False
    )
    dexteritytextindexer.searchable('titleAuthorImprintCollation_edition_edition')

    # Imprint
    titleAuthorImprintCollation_imprint_place = ListField(title=_(u'Place'),
        value_type=DictRow(title=_(u'Place'), schema=IPlace),
        required=False)
    form.widget(titleAuthorImprintCollation_imprint_place=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('titleAuthorImprintCollation_imprint_place')

    titleAuthorImprintCollation_imprint_publisher = ListField(title=_(u'Publisher'),
        value_type=DictRow(title=_(u'Publisher'), schema=IPublisher),
        required=False)
    form.widget(titleAuthorImprintCollation_imprint_publisher=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('titleAuthorImprintCollation_imprint_publisher')

    titleAuthorImprintCollation_imprint_year = schema.TextLine(
        title=_(u'Year'),
        required=False
    )
    dexteritytextindexer.searchable('titleAuthorImprintCollation_imprint_year')

    titleAuthorImprintCollation_imprint_placePrinted = ListField(title=_(u'Place printed'),
        value_type=DictRow(title=_(u'Place printed'), schema=IPlacePrinted),
        required=False)
    form.widget(titleAuthorImprintCollation_imprint_placePrinted=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('titleAuthorImprintCollation_imprint_placePrinted')

    titleAuthorImprintCollation_imprint_printer = ListField(title=_(u'Printer'),
        value_type=DictRow(title=_(u'Printer'), schema=IPrinter),
        required=False)
    form.widget(titleAuthorImprintCollation_imprint_printer=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('titleAuthorImprintCollation_imprint_printer')

    # Sort year
    titleAuthorImprintCollation_sortYear_sortYear = schema.TextLine(
        title=_(u'Sort year'),
        required=False
    )
    dexteritytextindexer.searchable('titleAuthorImprintCollation_sortYear_sortYear')

    # Collation
    titleAuthorImprintCollation_collation_pagination = schema.TextLine(
        title=_(u'Pagination'),
        required=False
    )
    dexteritytextindexer.searchable('titleAuthorImprintCollation_collation_pagination')


    titleAuthorImprintCollation_collation_illustrations = schema.TextLine(
        title=_(u'Illustrations'),
        required=False
    )
    dexteritytextindexer.searchable('titleAuthorImprintCollation_collation_illustrations')


    titleAuthorImprintCollation_collation_dimensions = schema.TextLine(
        title=_(u'Dimensions'),
        required=False
    )
    dexteritytextindexer.searchable('titleAuthorImprintCollation_collation_dimensions')

    titleAuthorImprintCollation_collation_accompanyingMaterial = ListField(title=_(u'Accompanying material'),
        value_type=DictRow(title=_(u'Accompanying material'), schema=IAccompanyingMaterial),
        required=False)
    form.widget(titleAuthorImprintCollation_collation_accompanyingMaterial=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('titleAuthorImprintCollation_collation_accompanyingMaterial')


    # # # # # # # # # # # # # # # # # # # # # # # #
    # Series, notes, ISBN fieldset                #
    # # # # # # # # # # # # # # # # # # # # # # # #
    
    model.fieldset('series_notes_isbn', label=_(u'Series, notes, ISBN'), 
        fields=['seriesNotesISBN_series_series', 'seriesNotesISBN_series_subseries',
                'seriesNotesISBN_notes_bibliographicalNotes', 'seriesNotesISBN_ISBN_ISBN',
                'seriesNotesISBN_ISBN_ISSN', 'seriesNotesISBN_conference_conference']
    )

    seriesNotesISBN_series_series = ListField(title=_(u'Series'),
        value_type=DictRow(title=_(u'Series'), schema=ISeries),
        required=False)
    form.widget(seriesNotesISBN_series_series=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('seriesNotesISBN_series_series')

    seriesNotesISBN_series_subseries = ListField(title=_(u'Subseries'),
        value_type=DictRow(title=_(u'Series'), schema=ISubseries),
        required=False)
    form.widget(seriesNotesISBN_series_subseries=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('seriesNotesISBN_series_subseries')

    # Notes
    seriesNotesISBN_notes_bibliographicalNotes = ListField(title=_(u'Bibliographical notes'),
        value_type=DictRow(title=_(u'Bibliographical notes'), schema=IBibliographicalNotes),
        required=False)
    form.widget(seriesNotesISBN_notes_bibliographicalNotes=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('seriesNotesISBN_notes_bibliographicalNotes')

    # ISBN
    seriesNotesISBN_ISBN_ISBN = ListField(title=_(u'ISBN'),
        value_type=DictRow(title=_(u'ISBN'), schema=IISBN),
        required=False)
    form.widget(seriesNotesISBN_ISBN_ISBN=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('seriesNotesISBN_ISBN_ISBN')

    seriesNotesISBN_ISBN_ISSN = ListField(title=_(u'ISSN'),
        value_type=DictRow(title=_(u'ISSN'), schema=IISSN),
        required=False)
    form.widget(seriesNotesISBN_ISBN_ISSN=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('seriesNotesISBN_ISBN_ISSN')

    # Conference
    seriesNotesISBN_conference_conference = ListField(title=_(u'Conference'),
        value_type=DictRow(title=_(u'Conference'), schema=IConference),
        required=False)
    form.widget(seriesNotesISBN_conference_conference=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('seriesNotesISBN_conference_conference')

    # # # # # # # # # # # # # # # # # # # # # # # #
    # Abstract and subject terms fieldset         #
    # # # # # # # # # # # # # # # # # # # # # # # #
    
    model.fieldset('abstract_subject_terms', label=_(u'Abstract and subject terms'), 
        fields=['abstractAndSubjectTerms_materialType', 'abstractAndSubjectTerms_biblForm',
                'abstractAndSubjectTerms_language', 'abstractAndSubjectTerms_level',
                'abstractAndSubjectTerms_notes', 'abstractAndSubjectTerms_classNumber',
                'abstractAndSubjectTerms_subjectTerm', 'abstractAndSubjectTerms_personKeywordType',
                'abstractAndSubjectTerms_geographicalKeyword', 'abstractAndSubjectTerms_period',
                'abstractAndSubjectTerms_startDate', 'abstractAndSubjectTerms_endDate',
                'abstractAndSubjectTerms_digitalReferences_reference', 'abstractAndSubjectTerms_abstract_abstract']
    )

    abstractAndSubjectTerms_materialType = ListField(title=_(u'Material type'),
        value_type=DictRow(title=_(u'Material type'), schema=IMaterialType),
        required=False)
    form.widget(abstractAndSubjectTerms_materialType=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_materialType')


    abstractAndSubjectTerms_biblForm = ListField(title=_(u'Bibl. form'),
        value_type=DictRow(title=_(u'Bibl. form'), schema=IBiblForm),
        required=False)
    form.widget(abstractAndSubjectTerms_biblForm=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_biblForm')

    abstractAndSubjectTerms_language = ListField(title=_(u'Language'),
        value_type=DictRow(title=_(u'Language'), schema=ILanguage),
        required=False)
    form.widget(abstractAndSubjectTerms_language=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_language')


    abstractAndSubjectTerms_level = schema.TextLine(
        title=_(u'Level'),
        required=False
    )
    dexteritytextindexer.searchable('abstractAndSubjectTerms_level')


    abstractAndSubjectTerms_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(abstractAndSubjectTerms_notes=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_notes')

    abstractAndSubjectTerms_classNumber = ListField(title=_(u'Class number'),
        value_type=DictRow(title=_(u'Class number'), schema=IClassNumber),
        required=False)
    form.widget(abstractAndSubjectTerms_classNumber=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_classNumber')

    abstractAndSubjectTerms_subjectTerm = ListField(title=_(u'Subject term'),
        value_type=DictRow(title=_(u'Subject term'), schema=ISubjectTerm),
        required=False)
    form.widget(abstractAndSubjectTerms_subjectTerm=DataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_subjectTerm')

    abstractAndSubjectTerms_personKeywordType = ListField(title=_(u'Person keyword type'),
        value_type=DictRow(title=_(u'Person keyword type'), schema=IPersonKeywordType),
        required=False)
    form.widget(abstractAndSubjectTerms_personKeywordType=DataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_personKeywordType')

    abstractAndSubjectTerms_geographicalKeyword = ListField(title=_(u'Geographical keyword'),
        value_type=DictRow(title=_(u'Geographical keyword'), schema=IGeographicalKeyword),
        required=False)
    form.widget(abstractAndSubjectTerms_geographicalKeyword=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_geographicalKeyword')

    abstractAndSubjectTerms_period = ListField(title=_(u'Period'),
        value_type=DictRow(title=_(u'Period'), schema=IPeriod),
        required=False)
    form.widget(abstractAndSubjectTerms_period=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_period')

    abstractAndSubjectTerms_startDate = schema.TextLine(
        title=_(u'Start date'),
        required=False
    )
    dexteritytextindexer.searchable('abstractAndSubjectTerms_startDate')

    abstractAndSubjectTerms_endDate = schema.TextLine(
        title=_(u'End date'),
        required=False
    )
    dexteritytextindexer.searchable('abstractAndSubjectTerms_endDate')

    # Digital references

    abstractAndSubjectTerms_digitalReferences_reference = ListField(title=_(u'Digital references'),
        value_type=DictRow(title=_(u'Digital references'), schema=IDigitalReferences),
        required=False)
    form.widget(abstractAndSubjectTerms_digitalReferences_reference=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_digitalReferences_reference')

    # Abstract
    abstractAndSubjectTerms_abstract_abstract = ListField(title=_(u'Abstract'),
        value_type=DictRow(title=_(u'Abstract'), schema=IAbstract),
        required=False)
    form.widget(abstractAndSubjectTerms_abstract_abstract=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('abstractAndSubjectTerms_abstract_abstract')

    # # # # # # # # # #
    # Reproductions   #
    # # # # # # # # # #
    model.fieldset('reproductions', label=_(u'Reproductions'), 
        fields=['reproductions_reproduction']
    )

    # Reproduction
    reproductions_reproduction = ListField(title=_(u'Reproduction'),
        value_type=DictRow(title=_(u'Reproduction'), schema=IReproduction),
        required=False)
    form.widget(reproductions_reproduction=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('reproductions_reproduction')


    # # # # # # # # # # # # # # # # # # # # #
    # Exhibitions, auctions, collections    #
    # # # # # # # # # # # # # # # # # # # # #
    model.fieldset('exhibitions_auctions_collections', label=_(u'Exhibitions, auctions, collections'), 
        fields=['exhibitionsAuctionsCollections_exhibition', 'exhibitionsAuctionsCollections_auction',
                'exhibitionsAuctionsCollections_collection']
    )

    # Exhibition
    exhibitionsAuctionsCollections_exhibition = ListField(title=_(u'Exhibition'),
        value_type=DictRow(title=_(u'Exhibition'), schema=IExhibition),
        required=False)
    form.widget(exhibitionsAuctionsCollections_exhibition=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('exhibitionsAuctionsCollections_exhibition')

    # Auction
    exhibitionsAuctionsCollections_auction = ListField(title=_(u'Auction'),
        value_type=DictRow(title=_(u'Auction'), schema=IAuction),
        required=False)
    form.widget(exhibitionsAuctionsCollections_auction=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('exhibitionsAuctionsCollections_auction')

    # Collection
    exhibitionsAuctionsCollections_collection = ListField(title=_(u'Collection'),
        value_type=DictRow(title=_(u'Collection'), schema=ICollection),
        required=False)
    form.widget(exhibitionsAuctionsCollections_collection=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('exhibitionsAuctionsCollections_collection')


    # # # # # # # # # # # # # # # # # # # # #
    # Relations                             #
    # # # # # # # # # # # # # # # # # # # # #

    model.fieldset('relations', label=_(u'Relations'), 
        fields=['relations_volume', 'relations_analyticalCataloguing_recordNo',
                'relations_analyticalCataloguing_volume', 'relations_analyticalCataloguing_title', 'relations_analyticalCataloguing_partOf',
                'relations_analyticalCataloguing_consistsOf', 'relations_museumObjects', 'relations_relatedMuseumObjects']
    )

    relations_volume = schema.TextLine(
        title=_(u'Volume'),
        required=False
    )
    dexteritytextindexer.searchable('relations_volume')

    relations_analyticalCataloguing_recordNo = schema.TextLine(
        title=_(u'record no.'),
        required=False
    )
    dexteritytextindexer.searchable('relations_analyticalCataloguing_recordNo')

    relations_analyticalCataloguing_volume = schema.TextLine(
        title=_(u'Volume'),
        required=False
    )
    dexteritytextindexer.searchable('relations_analyticalCataloguing_volume')

    relations_analyticalCataloguing_title = schema.TextLine(
        title=_(u'Title'),
        required=False
    )
    dexteritytextindexer.searchable('relations_analyticalCataloguing_title')

    # Analytical cataloguing
    relations_analyticalCataloguing_partOf = ListField(title=_(u'Part of'),
        value_type=DictRow(title=_(u'Part of'), schema=IPartOf),
        required=False)
    form.widget(relations_analyticalCataloguing_partOf=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('relations_analyticalCataloguing_partOf')

    relations_analyticalCataloguing_consistsOf = ListField(title=_(u'Consists of'),
        value_type=DictRow(title=_(u'Consists of'), schema=IConsistsOf),
        required=False)
    form.widget(relations_analyticalCataloguing_consistsOf=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('relations_analyticalCataloguing_consistsOf')

    # Museum objects
    relations_museumObjects = ListField(title=_(u'Museum objects'),
        value_type=DictRow(title=_(u'Museum objects'), schema=IMuseumObjects),
        required=False)
    form.widget(relations_museumObjects=DataGridFieldFactory)
    dexteritytextindexer.searchable('relations_museumObjects')

    relations_relatedMuseumObjects = RelationList(
        title=_(u'Museum objects'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder()
        ),
        required=False
    )

    # # # # # # # # # # # # # # # # # # # # #
    # Free fields and numbers               #
    # # # # # # # # # # # # # # # # # # # # #

    model.fieldset('free_fields_numbers', label=_(u'Free fields and numbers'), 
        fields=['freeFieldsAndNumbers_freeFields', 'freeFieldsAndNumbers_otherNumber',
                'freeFieldsAndNumbers_PPN']
    )

    # Free fields
    freeFieldsAndNumbers_freeFields = ListField(title=_(u'Free fields'),
        value_type=DictRow(title=_(u'Free fields'), schema=IFreeFields),
        required=False)
    form.widget(freeFieldsAndNumbers_freeFields=DataGridFieldFactory)
    dexteritytextindexer.searchable('freeFieldsAndNumbers_freeFields')

    freeFieldsAndNumbers_otherNumber = ListField(title=_(u'Other number'),
        value_type=DictRow(title=_(u'Other number'), schema=IOtherNumber),
        required=False)
    form.widget(freeFieldsAndNumbers_otherNumber=DataGridFieldFactory)
    dexteritytextindexer.searchable('freeFieldsAndNumbers_otherNumber')

    freeFieldsAndNumbers_PPN = schema.TextLine(
        title=_(u'PPN'),
        required=False
    )
    dexteritytextindexer.searchable('freeFieldsAndNumbers_PPN')

    # # # # # # # # # # # # # # # # # # # # #
    # Copies and shelf marks                #
    # # # # # # # # # # # # # # # # # # # # # 

    model.fieldset('copies_and_shelf_marks', label=_(u'Copies and shelf marks'), 
        fields=['copiesAndShelfMarks_defaultShelfMark', 'copiesAndShelfMarks_copyDetails']
    )

    copiesAndShelfMarks_defaultShelfMark = schema.TextLine(
        title=_(u'Default shelf mark'),
        required=False
    )
    dexteritytextindexer.searchable('copiesAndShelfMarks_defaultShelfMark')

    # Copy details
    copiesAndShelfMarks_copyDetails = ListField(title=_(u'Copy details'),
        value_type=DictRow(title=_(u'Copy details'), schema=ICopyDetails),
        required=False)
    form.widget(copiesAndShelfMarks_copyDetails=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('copiesAndShelfMarks_copyDetails')





    

# # # # # # # # # # # # # #
# Book declaration        #
# # # # # # # # # # # # # #

class Book(Container):
    grok.implements(IBook)
    pass

# # # # # # # # # # # # # #
# Book add/edit views   # 
# # # # # # # # # # # # # #

class AddForm(add.DefaultAddForm):
    template = ViewPageTemplateFile('bibliotheek_templates/add.pt')
    def update(self):
        super(AddForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if widget.__name__ in ['titleAuthorImprintCollation_title', 'titleAuthorImprintCollation_titleAuthor_author',
                                        'titleAuthorImprintCollation_titleAuthor_illustrator', 'titleAuthorImprintCollation_imprint_place',
                                        'titleAuthorImprintCollation_imprint_publisher', 'titleAuthorImprintCollation_imprint_placePrinted',
                                        'titleAuthorImprintCollation_collation_accompanyingMaterial']:
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('bibliotheek_templates/edit.pt')
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if widget.__name__ in ['titleAuthorImprintCollation_title', 'titleAuthorImprintCollation_titleAuthor_author',
                                        'titleAuthorImprintCollation_titleAuthor_illustrator', 'titleAuthorImprintCollation_imprint_place',
                                        'titleAuthorImprintCollation_imprint_publisher', 'titleAuthorImprintCollation_imprint_placePrinted',
                                        'titleAuthorImprintCollation_collation_accompanyingMaterial']:
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)





