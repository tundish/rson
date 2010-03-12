from unittest import TestCase
import os
from json import loads as sysloads
from rson import loads as newloads


class TestParser(TestCase):

    def test_parser(self):
        sourcedir = os.path.join(os.path.dirname(__file__), '..', 'styles')
        strings = [open(os.path.join(sourcedir, x), 'rb').read() for x in os.listdir('styles') if x.endswith('json')]

        for s in strings:
            self.assert_(sysloads(s) == newloads(s))

    def test_python_syntax(self):
        ''' Test a limited subset of Python syntax,
            after modifying "=" to be ":".
            Also, this is probably the easiest way to
            test triple quote processing.
        '''
        teststr = '''

# Comment goes here

x = 27
y = [1, 2, 3, {"z": 42}]


    # Although comments cannot go after other data,
    # they can be arbitrarily indented.

m = """
Now is the time for all good men
to come to the aid of their country.
"""

w = ["""test""",
     """triple""",
     {"""quotes""":"ok?"}]

num1 = 0x100
num2 = 0b101010
num3 = 0o455
num5 = 0.1
num6 = 01.2
num7 = .2

'''
        testdict = {}
        exec teststr in testdict
        del testdict['__builtins__']

        self.assertEquals(testdict, newloads(teststr.replace('=', ':')))


    def test_various(self):
        ae, l = self.assertEquals, newloads
        ae(l('a:[]\n x'), {'a':['x']})
        ae(l('[a,b]:[c,d]'), {('a','b'):['c', 'd']})
        ae(l('{[a,b]:[1,2,3], 0:1}:[c,d]'), {((0, 1), (('a', 'b'), (1, 2, 3)),):['c', 'd']})
        ae(l('a:b\n c'), {'a': {'b': 'c'}})
        ae(l('a:b\n c\n d'), {'a': {'b': ['c', 'd']}})
