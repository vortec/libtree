from libtree.properties import (set_properties, update_properties)
from libtree.query import get_properties


def xtest_update_properties(per, root):
    properties = get_properties(per, root)

    properties['title'] = 'Root node'
    properties['new'] = 'property'
    update_properties(per, root, properties)

    new_properties = get_properties(per, root)
    assert new_properties['title'] == 'Root node'
    assert new_properties['new'] == 'property'


def test_set_properties(per, root):
    properties = {'title': 'My Root Node'}
    set_properties(per, root, properties)
    assert get_properties(per, root) == properties