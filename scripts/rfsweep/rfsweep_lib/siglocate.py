
class SigLocate:
    def __init__(self):
        self.min = -50

    def update(self, data):
        l = [-100]
        for x in data:
            if x > -50:
                l.append(x)
        self.min = max(l)
