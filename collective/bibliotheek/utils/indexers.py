
from plone.indexer.decorator import indexer
from ..book import IBook

@indexer(IBook)
def titleAuthorImprintCollation_titleAuthor_author_role(object, **kw):
    try:
        if hasattr(object, 'titleAuthorImprintCollation_titleAuthor_author'):
            terms = []
            items = object.titleAuthorImprintCollation_titleAuthor_author
            if items:
                for item in items:
                    if item['roles']:
                        for term in item['roles']:
                            if term:
                                terms.append(term)

            return terms
        else:
            return []
    except:
        return []


@indexer(IBook)
def seriesNotesISBN_series_series_series(object, **kw):
    try:
        if hasattr(object, 'seriesNotesISBN_series_series'):
            terms = []
            items = object.seriesNotesISBN_series_series
            if items:
                for item in items:
                    if item['series']:
                        for term in item['series']:
                            if term:
                                terms.append(term)

            return terms
        else:
            return []
    except:
        return []

@indexer(IBook)
def seriesNotesISBN_series_subseries_subseries(object, **kw):
    try:
        if hasattr(object, 'seriesNotesISBN_series_subseries'):
            terms = []
            items = object.seriesNotesISBN_series_subseries
            if items:
                for item in items:
                    if item['subseries']:
                        for term in item['subseries']:
                            if term:
                                terms.append(term)

            return terms
        else:
            return []
    except:
        return []

@indexer(IBook)
def abstractAndSubjectTerms_biblForm(object, **kw):
    try:
        if hasattr(object, 'abstractAndSubjectTerms_biblForm'):
            return object.abstractAndSubjectTerms_biblForm
        else:
            return []
    except:
        return []

@indexer(IBook)
def abstractAndSubjectTerms_materialType(object, **kw):
    try:
        if hasattr(object, 'abstractAndSubjectTerms_materialType'):
            return object.abstractAndSubjectTerms_materialType
        else:
            return []
    except:
        return []

@indexer(IBook)
def abstractAndSubjectTerms_language(object, **kw):
    try:
        if hasattr(object, 'abstractAndSubjectTerms_language'):
            return object.abstractAndSubjectTerms_language
        else:
            return []
    except:
        return []

@indexer(IBook)
def abstractAndSubjectTerms_classNumber(object, **kw):
    try:
        if hasattr(object, 'abstractAndSubjectTerms_classNumber'):
            return object.abstractAndSubjectTerms_classNumber
        else:
            return []
    except:
        return []

@indexer(IBook)
def abstractAndSubjectTerms_geographicalKeyword(object, **kw):
    try:
        if hasattr(object, 'abstractAndSubjectTerms_geographicalKeyword'):
            return object.abstractAndSubjectTerms_geographicalKeyword
        else:
            return []
    except:
        return []

