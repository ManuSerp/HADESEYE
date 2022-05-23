from numpy import real
from sympy import symbols, Eq, solve


def dist_v(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5


def add_mul_vec(a, b, c):
    f = ((a[0]+b[0])**2+(a[1]+b[1])**2)**0.5
    return ((a[0]+b[0])*c/f, (a[1]+b[1])*c/f)


def add_vec(a, b):
    return (a[0]+b[0], a[1]+b[1])


def diff_vec(a, b):
    return (b[0]-a[0], b[1]-a[1])


class model:
    def __init__(self, antenna):
        self.antenna = antenna
        self.a_pos = [0 for i in range(len(antenna))]
        self.a_mesure = [0 for i in range(len(antenna))]

    def calibrate(self, i, coord):
        self.a_pos[i] = coord

    def det_pos(self, dist):
        inter = self.calculate_circle_intersect(dist)
        c = 0
        pr = []
        for x in inter:
            if x is not None:
                pr.append(x)
                c += 1

        if c == len(self.antenna):
            good_points = []

            for i, pt in enumerate(pr):
                except_ray = len(self.antenna)-1-i

                d1 = dist_v(pt[0], self.a_pos[except_ray]) - \
                    self.a_mesure[except_ray]

                d2 = dist_v(pt[1], self.a_pos[except_ray]) - \
                    self.a_mesure[except_ray]

                if d1 < d2:
                    good_points.append([pt[0][1], pt[0][0]])
                else:
                    good_points.append([pt[1][1], pt[1][0]])
                return good_points
        if c == 0:
            good_points = []

            for i in range(len(self.antenna)):
                idx = []
                for j in range(len(self.antenna)):
                    if i != j:
                        idx.append(j)

                p = add_mul_vec(diff_vec(self.a_pos[i], self.a_pos[idx[0]]),
                                diff_vec(
                                    self.a_pos[i], self.a_pos[idx[1]]), dist[i])
                good_points.append(add_vec(p, self.a_pos[i]))
            return good_points

        if c == 1:
            good_points = []
            # c'est pas bon ca car ya deux none on verra plus tard
            for i, x in enumerate(inter):
                if x == None:
                    idx_i = i
            idx = []
            for j in range(len(self.antenna)):
                if idx_i != j:
                    idx.append(j)
            coord_i = add_mul_vec(diff_vec(self.a_pos[idx_i], self.a_pos[idx[0]]),
                                  diff_vec(
                self.a_pos[idx_i], self.a_pos[idx[1]]), dist[idx_i])
            coord_i = add_vec(coord_i, self.a_pos[idx_i])

    def calculate_circle_intersect(self, dist):
        for i, x in enumerate(dist):
            self.a_mesure[i] = x
        inter = [None for i in range(len(self.antenna))]  # 12 13 23
        perm = []
        for i in range(1, len(self.antenna)):
            for j in range(1, len(self.antenna)+1):
                if i != j and j > i:

                    perm.append([i, j])

        for i in range(len(inter)):
            inter[i] = self.intersect(perm[i][0]-1, perm[i][1]-1)

        print(inter)
        return inter

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
        if len(sol) == 0:
            return None
        return sol


if __name__ == "__main__":
    m = model(["0", "1", "2"])
    m.calibrate(0, [0, 0])
    m.calibrate(1, [0.5, 1])
    m.calibrate(2, [1, 0])
    # m.calculate_circle_intersect([1.3, 1.3, 1.3])
    m.det_pos([0.4, 0.4, 0.4])
