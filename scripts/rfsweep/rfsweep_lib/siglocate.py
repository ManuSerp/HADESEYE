
class SigLocate:
    def __init__(self):
        self.min = -50

    def update(self, data):
        l = [-100]
        for x in data:
            if x > -50:
                l.append(x)
        if abs(max(l)-self.min) < 100:
            self.min = max(l)
        print(self.min)
