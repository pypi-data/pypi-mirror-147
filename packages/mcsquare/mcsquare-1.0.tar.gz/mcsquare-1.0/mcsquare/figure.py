from PIL import Image


class MapSquare:
    pics = ['Baikal-500-500.jpg']

    def __init__(self, pic=None, sx=0, sy=0):
        if not pic:
            pic = MapSquare.pics[0]
        try:
            im = Image.open(pic)
        except FileNotFoundError:
            print(f'FileNotFound: {pic}')
            return
        self.image = im.load()
        self.x = im.size[0]
        self.y = im.size[1]
        if sx == 0:
            sx, sy = im.size
        self.dx = self.x / sx
        self.dy = self.y / sy
        self.pix = []
        self.sx = sx
        self.sy = sy
        for _ in range(sx):
            self.pix.append([0] * sy)
        # print(self.pix)
        for i in range(self.x):
            for j in range(self.y):
                r, g, b = self.image[i, j]
                self.pix[int(i / self.dx)][int(j / self.dy)] = int((r < 10) and (g < 70) and (b > 220))

    def color_state(self, px, py):
        res = 0
        x = min(self.sx - 1, abs(px))
        y = min(self.sy - 1, abs(py))
        try:
            res = self.pix[x][self.sy - y - 1]
        except IndexError:
            print(x, self.sy - y - 1)
        return res

    def get_size(self):
        return self.x, self.y


if __name__ == '__main__':
    pic = MapSquare('Baikal-500-500.jpg', 500, 500)
    print(pic.get_size())
