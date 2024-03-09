import drawsvg
import circlify as circ
import random
import math as m



def sin(phi):
    """ calculactes sin value from degree"""
    return m.sin(phi * m.pi / 180)

def cos(phi):
    """ calculactes cos value from degree"""
    return m.cos(phi * m.pi / 180)

def radius(x, y):
    """calculates radius from x and y"""
    return m.sqrt(x**2 + y**2)
class BubbleRenderer:

    def __init__(self, **kwargs):
        self.frame = None
        self.size = None
        self.data = None
        self.labels = None
        self.cmap = None
        self.packing = None
        self.background_color = None
        self._parse_kwargs(kwargs)

    def render(self):
        self._create_frame()
        self._create_bubbles()
        return self.frame

    def _create_frame(self):
        """Create a frame for the bubble chart"""
        if self.size is None:
            raise ValueError("Size is not set")
        elif int(self.size[0]) < 0 or int(self.size[1]) < 0:
            raise ValueError("Size must be positive")
        self.frame = drawsvg.Drawing(
            width=self.size[0],
            height=self.size[1],
            origin='center',
            style=f"background-color: " + str(self.background_color),
        )

    def _create_bubbles(self):
        circles = []
        if self.packing == 'circle':
            circles = circ.circlify(
                self.data,
                target_enclosure=circ.Circle(x=0, y=0, r=self.size[0] / 2),
                show_enclosure=False,
            )
        elif self.packing == 'rectangle':
            pass
        elif self.packing == 'planets':
            sorted_data = sorted(self.data, reverse=True)
            dPhi = 360 / len(sorted_data)
            Phi = [i * dPhi for i in range(len(sorted_data)-1)]
            for i, data in enumerate(sorted_data):
                if i == 0:
                    circles.append(circ.Circle(x=0, y=0, r=self.size[0] / 3))  # Sun data point
                    continue
                r = (sorted_data[i] / sorted_data[0]) * self.size[0] / 3 # Planet radius
                # polar coordinates
                R = radius( circles[i-1].x, circles[i-1].y) + circles[i-1].r + r
                phi = Phi.pop(0) if i%2 == 0 else Phi.pop(int(len(Phi)/2))
                R = self.fit_R(R, phi, r, circles)
                circle = circ.Circle(x=R * cos(phi), y=R * sin(phi), r=r)
                circles.append(circle)

        if circles is None:
            raise ValueError("Circles could not be created")
        for i, circle in enumerate(circles):
            x = circle.x
            y = circle.y
            r = 0.8 * circle.r
            first_gradient = drawsvg.RadialGradient(
                cx=x,
                cy=y,
                r=r,
                fx=x,
                fy=y,
            )
            first_gradient.add_stop(offset="0%", color=self.cmap[1])
            first_gradient.add_stop(offset="20%", color=self.cmap[1])
            first_gradient.add_stop(offset="80%", color=self.cmap[0])
            first_gradient.add_stop(offset="100%", color=self.background_color)
            self.frame.append(drawsvg.Circle(
                cx=x,
                cy=y,
                r=r,
                fill=first_gradient,
                stroke='black',
                stroke_width=1,
            ))
            self.frame.append(drawsvg.Text(
                text=f"""{self.labels[i]}\n{self.data[i]}""",
                x=x,
                y=y,
                text_anchor="middle",
                font_size=10,
                fill='black',
            ))

    def _create_random_data(self):
        """Create random data for testing"""
        self.data = [random.randint(1, 500) for _ in range(20)]
        self.labels = [f"Label {i}" for i in range(20)]

    def _parse_kwargs(self, kwargs):
        """Parse keyword arguments"""
        if 'size' in kwargs:
            self.size = kwargs['size']
        else:
            self.size = (500, 500)
        if 'data' in kwargs:
            self.data = kwargs['data']
        else:
            self._create_random_data()
        if 'cmap' in kwargs:
            self.cmap = kwargs['cmap']
        if 'background_color' in kwargs:
            self.background_color = kwargs['background_color']
        if 'packing' in kwargs:
            self.packing = kwargs['packing']

    def fit_R(self, R, phi, r, circles):
        d_r = 10
        collided = False
        while not collided:
            x = R * cos(phi)
            y = R * sin(phi)
            for i, circle in enumerate(circles):
                distance = radius(x - circle.x, y - circle.y)
                min_distance = circle.r + r
                if distance <= min_distance:
                    collided = True
                    return R
            R -= d_r



if __name__ == "__main__":
    br = BubbleRenderer(
        size=(500, 500),
        background_color='black',
        cmap=['#C2185B', '#FCE4EC'],
        packing='circle',
    )
    img = br.render()
    img.save_svg("bubble.svg")
