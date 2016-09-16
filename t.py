class A(object):
    def __init__(self):
        self.x = 1

class B(A):
    c = 2

    def __init__(self):
        super(B, self).__init__()
        self.y = 1
        print "self.x=", self.x

    def test(self):
        print "x function"

import ipdb;ipdb.set_trace()   
b=B()
t=B()
b.test()

print "end"
