from libtree.properties import (get_inherited_properties,
                                get_inherited_property_value,
                                set_properties, set_property_value,
                                update_properties)
import pytest


def test_get_inherited_property_value(per, node2):
    assert get_inherited_property_value(per, node2, 'integer') == 1


def test_get_inherited_properties_no_inheritance(per, root):
    expected = {
        'title': 'Root',
        'type': 'root',
        'boolean': False,
        'integer': 1
    }
    assert get_inherited_properties(per, root) == expected


def test_get_inherited_properties_simple_inheritance(per, node2):
    expected = {
        'title': 'Node 2',
        'type': 'node2',
        'boolean': True,
        'foo': 'bar',
        'integer': 1
    }
    assert get_inherited_properties(per, node2.id) == expected


def test_get_inherited_properties_multiple_inheritance(per, node2_1_1):
    expected = {
        'title': 'Node 2-1-1',
        'type': 'node2_1_1',
        'boolean': False,
        'integer': 1,
        'foo': 'bar'
    }
    assert get_inherited_properties(per, node2_1_1) == expected


def test_update_properties(per, root):
    properties = root.properties.copy()
    properties['title'] = 'Root node'
    properties['new'] = 'property'
    root = update_properties(per, root.id, properties)

    assert root.properties['title'] == 'Root node'
    assert root.properties['new'] == 'property'


def test_update_properties_only_allows_dict(per, root):
    with pytest.raises(TypeError):
        update_properties(per, root, [])


def test_set_properties(per, root):
    properties = {'title': 'My Root Node'}
    root = set_properties(per, root.id, properties)
    assert root.properties == properties


def test_set_properties_only_allows_dict(per, root):
    with pytest.raises(TypeError):
        set_properties(per, root, [])


def test_set_property_value(per, root):
    root = set_property_value(per, root.id, 'title', 'Root')
    assert root.properties['title'] == 'Root'
