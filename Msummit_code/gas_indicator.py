import PySimpleGUI as sg
import math
import random
from time import sleep

def Map(func, sequence, *argc):
    """
    map function with extra argument, not for tuple
    """
    if isinstance(sequence, list):
        return list(map(lambda i:func(i, *argc), sequence))
    return func(sequence, *argc)

def add(number1, number2):
    """
    Add two number
    """
    return number1 + number1

def limit(number):
    """
    Limit angle in range 0 ~ 360
    """
    return number if 0<=number<=360 else 0 if number<low else 360

class Clock():
    """
    Draw background circle or arc
    All angles defined as clockwise from negative x-axis.
    """
    def __init__(self, center_x=0, center_y=0, radius=100, start_angle=0,
        stop_angle=360, fill_color='white', line_color='black', line_width=2):

        instance = Map(isinstance, [center_x, center_y, radius, start_angle,
            stop_angle, line_width], (int, float)) + Map(isinstance,
            [fill_color, line_color], str)
        if False in instance:
            raise ValueError
        start_angle, stop_angle = limit(start_angle), limit(stop_angle)
        self.all = [center_x, center_y, radius, start_angle, stop_angle,
            fill_color, line_color, line_width]
        self.figure = []
        self.new()

    def new(self):
        """
        Draw Arc or circle
        """
        x, y, r, start, stop, fill, line, width = self.all
        start, stop = (180-start, 180-stop) if stop<start else (180-stop, 180-start)
        if start == stop%360:
            self.figure.append(draw.DrawCircle((x, y), r, fill_color=fill,
                line_color=line, line_width=width))
        else:
            self.figure.append(draw.DrawArc((x-r, y+r), (x+r, y-r), stop-start,
                start, style='arc', arc_color=fill))

    def move(self, delta_x, delta_y):
        """
        Move circle or arc in clock by delta x, delta y
        """
        if False in Map(isinstance, [delta_x, delta_y], (int, float)):
            raise ValueError
        self.all[0] +=  delta_x
        self.all[1] +=  delta_y
        for figure in self.figure:
            draw.MoveFigure(figure, delta_x, delta_y)


class Tick():
    """
    Create tick on click for minor tick, also for major tick
    All angles defined as clockwise from negative x-axis.
    """
    def __init__(self, center_x=0, center_y=0, start_radius=90, stop_radius=100,
        start_angle=0, stop_angle=360, step=6, line_color='black', line_width=2):

        instance = Map(isinstance, [center_x, center_y, start_radius,
            stop_radius, start_angle, stop_angle, step, line_width],
            (int, float)) + [Map(isinstance, line_color, (list, str))]
        if False in instance:
            raise ValueError
        start_angle, stop_angle = limit(start_angle), limit(stop_angle)
        self.all = [center_x, center_y, start_radius, stop_radius,
            start_angle, stop_angle, step, line_color, line_width]
        self.figure = []
        self.new()

    def new(self):
        """
        Draw ticks on clock
        """
        (x, y, start_radius, stop_radius, start_angle, stop_angle, step,
            line_color, line_width) = self.all
        start_angle, stop_angle = (180-start_angle, 180-stop_angle
            ) if stop_angle<start_angle else (180-stop_angle, 180-start_angle)
        for i in range(start_angle, stop_angle+1, step):
            start_x = x + start_radius*math.cos(i/180*math.pi)
            start_y = y + start_radius*math.sin(i/180*math.pi)
            stop_x  = x +  stop_radius*math.cos(i/180*math.pi)
            stop_y  = y +  stop_radius*math.sin(i/180*math.pi)
            self.figure.append(draw.DrawLine((start_x, start_y),
                (stop_x, stop_y), color=line_color, width=line_width))

    def move(self, delta_x, delta_y):
        """
        Move ticks by delta x and delta y
        """
        if False in Map(isinstance, [delta_x, delta_y], (int, float)):
            raise ValueError
        self.all[0] += delta_x
        self.all[1] += delta_y
        for figure in self.figure:
            draw.MoveFigure(figure, delta_x, delta_y)

class Pointer():
    """
    Draw pointer of clock
    All angles defined as clockwise from negative x-axis.
    """
    def __init__(self, center_x=0, center_y=0, angle=0, inner_radius=20,
        outer_radius=80, outer_color='white', pointer_color='blue',
        origin_color='black', line_width=2):

        instance = Map(isinstance, [center_x, center_y, angle, inner_radius,
            outer_radius, line_width], (int, float)) + Map(isinstance,
            [outer_color, pointer_color, origin_color], str)
        if False in instance:
            raise ValueError

        self.all = [center_x, center_y, angle, inner_radius, outer_radius,
            outer_color, pointer_color, origin_color, line_width]
        self.figure = []
        self.new(degree=angle)

    def new(self, degree=0):
        """
        Draw new pointer by angle, erase old pointer if exist
        degree defined as clockwise from negative x-axis.
        """
        (center_x, center_y, angle, inner_radius, outer_radius,
            outer_color, pointer_color, origin_color, line_width) = self.all
        if self.figure != []:
            for figure in self.figure:
                draw.DeleteFigure(figure)
            self.figure = []
        d = degree - 90
        self.all[2] = degree
        dx1 = int(2*inner_radius*math.sin(d/180*math.pi))
        dy1 = int(2*inner_radius*math.cos(d/180*math.pi))
        dx2 = int(outer_radius*math.sin(d/180*math.pi))
        dy2 = int(outer_radius*math.cos(d/180*math.pi))
        self.figure.append(draw.DrawLine((center_x-dx1, center_y-dy1),
            (center_x+dx2, center_y+dy2),
            color=pointer_color, width=line_width))
        self.figure.append(draw.DrawCircle((center_x, center_y), inner_radius,
            fill_color=origin_color, line_color=outer_color, line_width=line_width))

    def move(self, delta_x, delta_y):
        """
        Move pointer with delta x and delta y
        """
        if False in Map(isinstance, [delta_x, delta_y], (int, float)):
            raise ValueError
        self.all[:2] = [self.all[0]+delta_x, self.all[1]+delta_y]
        for figure in self.figure:
            draw.MoveFigure(figure, delta_x, delta_y)

class Meter():
    """
    Create Meter
    All angles defined as count clockwise from negative x-axis.
    Should create instance of clock, pointer, minor tick and major tick first.
    """
    def __init__(self, center=(0, 0), clock=None, pointer=None,
            minor_tick=None, major_tick=None):
        self.center_x, self.center_y = self.center = center
        self.clock = clock
        self.minor_tick = minor_tick
        self.major_tick = major_tick
        self.pointer = pointer
        self.dx = self.dy = 1

    def move(self, delta_x, delta_y):
        """
        Move Meter to move all componenets in meter.
        """
        self.center_x, self.center_y =self.center = (
            self.center_x+delta_x, self.center_y+delta_y)
        if self.clock:
            self.clock.move(delta_x, delta_y)
        if self.minor_tick:
            self.minor_tick.move(delta_x, delta_y)
        if self.major_tick:
            self.major_tick.move(delta_x, delta_y)
        if self.pointer:
            self.pointer.move(delta_x, delta_y)

    def change(self, degree=0, step=1, delay=0.01):
        """
        Change position of meter
        """
        x, y = self.center_x, self.center_y
        if self.pointer:
            angle = self.pointer.all[2]
            step = step if degree >= angle else -step
            for d in range(angle, degree, step):
                self.pointer.new(degree=d)
                x += self.dx
                y += self.dy
                if abs(x)>220:
                    self.dx = -self.dx
                if abs(y)>140:
                    self.dy = -self.dy
                self.move(self.dx, self.dy)
                window.Refresh()
                sleep(delay)
            self.pointer.new(degree=degree)
            window.Refresh()

layout = [
    [sg.Button('Quit', size=(6, 1), font=('Courier New', 16), key='Quit',
        enable_events=True)],
    [sg.Graph((643, 483), (-321, -241), (321, 241), key='-Graph-')]]
window = sg.Window('Meter', layout=layout, finalize=True, no_titlebar=True)
draw = window.find_element('-Graph-')

start_angle = 45
stop_angle = 270
clock = Clock(start_angle=start_angle, stop_angle=stop_angle)
minor_tick = Tick(start_angle=start_angle, stop_angle=stop_angle, line_width=2)
major_tick = Tick(start_angle=start_angle, stop_angle=stop_angle, line_width=5,
    start_radius=80, step=30)
pointer = Pointer(angle=start_angle, inner_radius=10, outer_radius=75,
    pointer_color='white', line_width=5)
meter = Meter(clock=clock, minor_tick=minor_tick, major_tick=major_tick,
    pointer=pointer)

while True:

    event, values = window.read(timeout=10)

    if event == 'Quit':
        break

    degree = random.randint(start_angle, stop_angle)
    meter.change(degree)

window.close()