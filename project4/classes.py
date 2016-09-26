from func import get_input_function

class Storage(object):
    obj = None
    items = None
    player = None

    @classmethod
    def __new__(cls, *args):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
            cls.player = []
            cls.items = []
        return cls.obj

class Player(object):
    def __init__(self, name, num, pset):
        self.name = name
        self.num = num
        self.pset = pset
        
    @classmethod
    def construct(cls, name, num, pset):
        return Player(name, num, pset)

    def properties(self):
        print(self.name, self.num, self.pset)

class Ships(object):
    def __init__(self, name, xyz):
        self.name = name
        self.alive = True
        self.xyz = xyz

    @classmethod
    def construct(cls, name, *xyz):
        return Ships(name, xyz)

    def properties(self):
        print(self.name, self.xyz, self.alive)
