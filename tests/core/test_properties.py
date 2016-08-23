# Copyright (c) 2016 Fabian Kochem


import pytest

from libtree.core.properties import (get_inherited_properties,
                                     get_inherited_property_value,
                                     get_nodes_by_property_dict,
                                     get_nodes_by_property_key,
                                     get_nodes_by_property_value,
                                     set_properties,
                                     set_property_value, update_properties)


def test_get_nodes_by_property_dict(cur, root):
    query = {
        'boolean': False,
        'type': 'root'
    }
    results = get_nodes_by_property_dict(cur, query)
    ids = {child.id for child in results}
    assert ids == {root.id}


def test_get_nodes_by_property_key(cur, root, nd2, nd2_1_1):
    ids = {child.id for child in get_nodes_by_property_key(cur, 'boolean')}
    assert root.id in ids
    assert nd2.id in ids
    assert nd2_1_1.id in ids


def test_get_nodes_by_property_value(cur, root, nd2_1_1):
    results = get_nodes_by_property_value(cur, 'boolean', False)
    ids = {child.id for child in results}
    assert root.id in ids
    assert nd2_1_1.id in ids


def test_get_inherited_property_value(cur, nd2):
    assert get_inherited_property_value(cur, nd2, 'integer') == 1


def test_get_inherited_properties_no_inheritance(cur, root):
    expected = {
        'type': 'root',
        'boolean': False,
        'integer': 1,
        'dict': {'key': 'value'},
        'list': [{'abc': 2}]
    }
    assert get_inherited_properties(cur, root) == expected


def test_get_inherited_properties_simple_inheritance(cur, nd2):
    expected = {
        'title': 'Node 2',
        'type': 'nd2',
        'boolean': True,
        'foo': 'bar',
        'integer': 1,
        'dict': {'another key': 'another value'},
        'list': [{'abc': 2}]
    }
    assert get_inherited_properties(cur, nd2.id) == expected


def test_get_inherited_properties_multiple_inheritance(cur, nd2_1_1):
    expected = {
        'title': 'Node 2-1-1',
        'type': 'nd2_1_1',
        'boolean': False,
        'integer': 1,
        'foo': 'bar',
        'dict': {'key': 'yet another value'},
        'list': [{'def': 4}]
    }
    assert get_inherited_properties(cur, nd2_1_1) == expected


def test_update_properties(cur, root):
    properties = root.properties.copy()
    properties['title'] = 'Root node'
    properties['new'] = 'property'
    root = update_properties(cur, root.id, properties)

    assert root.properties['title'] == 'Root node'
    assert root.properties['new'] == 'property'


def test_update_properties_only_allows_dict(cur, root):
    with pytest.raises(TypeError):
        update_properties(cur, root, [])


def test_set_properties(cur, root):
    properties = {'title': 'My Root Node'}
    root = set_properties(cur, root.id, properties)
    assert root.properties == properties


def test_set_properties_only_allows_dict(cur, root):
    with pytest.raises(TypeError):
        set_properties(cur, root, [])


def test_set_property_value(cur, root):
    root = set_property_value(cur, root.id, 'title', 'Root')
    assert root.properties['title'] == 'Root'
