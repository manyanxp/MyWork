class Test(object):
    def __init__(self):
        self.events = []

    def __iadd__(self, sender):
        self.events.append(sender)
        return self.events

    def __isub__(self, sender):
        self.events.append(sender)
        return self.events

    def __call__(self, sender):
        for a in self.events:
            print(a)


class Test2(object):
    val = 0
    def __int__(self):
        pass

    def __iadd__(self, sender):
        self.val = self.val + sender
        return self.val

    def __call__(self, sender):
        print(self.val + sender)

class Prod:
    value = []
    def __init__(self, value):
        self.value = value

    def __iadd__(self, sender):
        self.value.append(sender)
        for a in self.value:
            print(a)
        return self

    def function(self, other):
        for a in self.value:
            print(a)

    def __call__(self, other):
        for a in self.value:
            print(a)
        #return x

if __name__ == "__main__":
    #f = Test()
    #f += "1"
    #f += "2"

    #f("")

    #x = Prod()
    #x(3)
    #x(4)
    #x += 5
    #x(6)

    t = Test2()
    t += 2
    t(3)


