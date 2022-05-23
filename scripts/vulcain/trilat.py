from numpy import real
from sympy import symbols, Eq, solve


class model:
    def __init__(self, antenna):
        self.antenna = antenna
        self.a_pos = [0 for i in range(len(antenna))]
        self.a_mesure = [0 for i in range(len(antenna))]

    def calibrate(self, i, coord):
        self.a_pos[i] = coord

    def calculate(self, dist):
        for i, x in enumerate(dist):
            self.a_mesure[i] = x
        inter = [False for i in range(len(self.antenna))]  # 12 13 23
        perm = []
        for i in range(1, len(self.antenna)):
            for j in range(1, len(self.antenna)+1):
                if i != j and j > i:

                    perm.append([i, j])
        print(perm)
        # for i in range(len(inter)):
        #     inter[i] = self.intersect()

    def intersect(self, a, b):
        x = symbols('x', real=True)
        y = symbols('y', real=True)
        # expr = (x-self.a_pos[a][0])**2 + (((self.a_mesure[b]**2-(x-self.a_pos[b][0])**2)
        #                                    ** 0.5)+self.a_pos[b][1]-self.a_pos[a][1])**2 - (self.a_mesure[a]**2)

        eq1 = Eq((x-self.a_pos[a][0])**2 +
                 (y-self.a_pos[a][1])**2-self.a_mesure[a]**2, 0)
        eq2 = Eq((x-self.a_pos[b][0])**2 +
                 (y-self.a_pos[b][1])**2-self.a_mesure[b]**2, 0)
        sol = solve([eq1, eq2], [x, y])
        return sol


if __name__ == "__main__":
    m = model(["0", "1", "2"])
    m.calibrate(0, [0, 0])
    m.calibrate(1, [1, 1])
    m.calculate([0.7, 0.7])
    # m.intersect(0, 1)
