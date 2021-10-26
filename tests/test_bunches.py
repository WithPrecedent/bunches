"""
test_bunches: tests classes in bunches
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2020-2021, Corey Rayburn Yung
License: Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0)

ToDo:
    test_catalog: complete tests
    test_proxy
    test_library
    
"""
import dataclasses

import bunches


@dataclasses.dataclass
class TestClass(object):
    
    name: str = 'something'


def test_listing():
    listing = bunches.Listing(contents = ['a', 'b', 'c'])
    assert listing[1] == 'b'
    listing.add(item = 'd')
    assert listing[3] == 'd'
    listing.insert(2, 'zebra')
    assert listing[2] == 'zebra'
    listing.append('e')
    assert listing[5] == 'e'
    listing.extend(['f', 'g'])
    assert listing[7] == 'g'
    sub_listing = listing.subset(
        include = ['a', 'b', 'c', 'd', 'zebra'],
        exclude = 'd')
    assert sub_listing.contents == ['a', 'b', 'zebra', 'c']
    sub_listing.remove('c')
    assert sub_listing.contents == ['a', 'b', 'zebra']
    listing.clear()
    return

def test_hybrid():
    hybrid = bunches.Hybrid(contents = ['a', 'b', 'c'])
    hybrid.setdefault(value = 'No')
    assert hybrid.get('tree') == 'No'
    assert hybrid[1] == 'b'
    hybrid.add(item = 'd')
    assert hybrid[3] == 'd'
    hybrid.insert(2, 'zebra')
    assert hybrid[2] == 'zebra'
    sub_hybrid = hybrid.subset(
        include = ['a', 'b', 'c', 'd', 'zebra'],
        exclude = 'd')
    assert sub_hybrid.contents == ['a', 'b', 'zebra', 'c']
    sub_hybrid.remove('c')
    assert sub_hybrid.contents == ['a', 'b', 'zebra']
    assert hybrid[0] == 'a'
    assert hybrid['zebra'] == 2
    hybrid.append('b')
    assert hybrid['b'] == [1, 5]
    assert hybrid.values() == tuple(['a', 'b', 'zebra', 'c', 'd', 'b'])
    assert hybrid.keys() == tuple(['a', 'b', 'zebra', 'c', 'd', 'b'])
    hybrid.remove('b')
    assert hybrid.contents == ['a', 'zebra', 'c', 'd', 'b']
    hybrid.clear()
    test_class = TestClass()
    hybrid.add(test_class)
    assert hybrid.keys() == tuple(['something'])
    assert hybrid.values() == tuple([test_class])
    return

def test_dictionary():
    alt_created = bunches.Dictionary.fromkeys(
        keys = ['a', 'b', 'c'], 
        value = 'tree')
    assert alt_created['a'] == 'tree'
    dictionary = bunches.Dictionary(
        contents = {'a': 'b', 'c': 'd'}, 
        default_factory = 'Nada')
    assert dictionary.get('f') == 'Nada'
    assert dictionary['a'] == 'b'
    dictionary.add({'e': 'f'})
    assert dictionary['e'] == 'f'
    subset = dictionary.subset(include = ['a', 'e'])
    assert subset.keys() == tuple(['a', 'e'])
    assert subset.values() == tuple(['b', 'f'])
    return

def test_catalog():
    catalog = bunches.Catalog()
    return
 
if __name__ == '__main__':
    test_listing()
    test_hybrid()
    test_dictionary()
    test_catalog()
   