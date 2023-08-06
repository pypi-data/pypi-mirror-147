"""
Testing the biolink model dataclasses + pydandic

tests validators and converters
"""
import pytest
from pydantic import ValidationError

from biolink_model_pydantic.model import Entity, Gene, Publication


def test_gene_xref_to_list_converter():
    """
    Test that passing a string to Entity.provided_by is converted to a list
    """
    gene = Gene(id="MGI:123")
    gene.xref = 'ENSEMBL:ENSMUSG00123567'
    assert gene.xref == ['ENSEMBL:ENSMUSG00123567']


def test_bad_curie():
    """
    a misformatted curie returns a validation error
    """
    with pytest.raises(ValidationError):
        entity = Entity(id="this is not a curie")


def test_missing_required_field_raises_error():
    """
    test missing required field raises error
    """
    with pytest.raises(ValidationError):
        Entity()


def test_bad_curie_in_list():
    """
    Test that misformatted curie in a list returns a validation error
    """
    with pytest.raises(ValidationError):
        pub = Publication(id='PMID:123', mesh_terms=['foo:bar', 'bad_curie'])


def test_bad_curie_prefix(caplog):
    """
    Test that misformatted curie in a list returns a validation error
    """
    gen_ent = Gene(id='NCBIGene:123', in_taxon='taxon:foo')
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[0].msg.startswith("taxon:foo prefix 'taxon' not in curie map")
    assert caplog.records[1].msg.startswith("Consider one of ['NCBITaxon', 'MESH']")


def test_empty_local_id_emits_warning(caplog):
    """
    Test that misformatted curie in a list returns a validation error
    """
    gen_ent = Gene(id='NCBIGene:')
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[0].msg.startswith("NCBIGene: does not have a local identifier")


def test_good_curie():
    """
    Tests that a properly formatted curie works, and
    that a string is equivalent to the Curie type
    """
    entity = Entity(id='HP:0000001')
    assert 'HP:0000001' == entity.id


def test_curie_like_synonym():
    """
    Tests that a synonym that looks a little like a curie won't cause split errors
    """
    entity = Gene(id="MGI:1", synonym=['si:dkey-13i15.1si:dkey-30j22.1'])
    assert entity.synonym == ['si:dkey-13i15.1si:dkey-30j22.1']


def test_taxon():
    gene1 = Gene(id='MGI:1', in_taxon='NCBITaxon:1')
    gene2 = Gene(id='MGI:1', in_taxon=['NCBITaxon:1'])

    assert gene1.in_taxon == gene2.in_taxon
