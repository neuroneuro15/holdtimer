import pyglet
from pyglet.window import key
from collections import OrderedDict
import click


class TimerLabel(pyglet.text.Label):

    fmt = "{self.name}: ({self.npressed}) {self.time:.2f}"

    def __init__(self, name='', start_time=0, active=False, *args, **kwargs):
        super(TimerLabel, self).__init__(*args, **kwargs)
        self.name = name
        self.npressed = 0
        self.time = start_time
        self.active = active
        self.text = self.fmt.format(self=self)
        pyglet.clock.schedule(self.update)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if value:
            self.npressed += 1
        self._active = value

    def update(self, dt):
        if self.active:
            self.time += dt

    def draw(self, *args, **kwargs):
        self.text = self.fmt.format(self=self)
        super(self.__class__, self).draw(*args, **kwargs)




class TimerApp(pyglet.window.Window):

    start_x_offset = 10
    start_y_offset = 80

    def __init__(self, *args, **kwargs):
        super(TimerApp, self).__init__(*args, **kwargs)
        self.directions_label = pyglet.text.Label('Key Counter + Timer, by N. A. Del Grosso\nPress and Hold Any Key To Start Timing!\n(Escape to exit, backspace to reset)',
                                                  x= 50,
                                                  y=self.height - 20,
                                                  multiline=True,
                                                  width=self.width - 50)
        self.global_timer = pyglet.text.Label('Total Running Time: {:.2f}'.format(0), x=self.width // 2, y=0, anchor_x='center')
        self.global_timer.time = 0.
        pyglet.clock.schedule(self.update_global_timer)
        self.timers = OrderedDict()
        self.curr_y = self.height - self.start_y_offset
        self.curr_x = self.start_x_offset
        self.text_size = 16

    def update_global_timer(self, dt):
        self.global_timer.time += dt
        self.global_timer.text = 'Total Running Time: {:.2f}'.format(self.global_timer.time)

    def on_draw(self):
        self.clear()
        self.directions_label.draw()
        self.global_timer.draw()
        for timer in self.timers.values():
            timer.draw()


    def on_key_press(self, sym, mod):

        if sym == key.ESCAPE:
            self.close()

        if sym == key.BACKSPACE:
            for timer in self.timers.values():
                 pyglet.clock.unschedule(timer.update)
            self.timers = {}
            self.curr_x = self.start_x_offset
            self.curr_y = self.height - self.start_y_offset

            self.global_timer.time = 0.
            return

        try:
            self.timers[sym].active = True
        except KeyError:
            if self.curr_y < self.text_size * 1.5:
                self.curr_y = self.height - 80
                self.curr_x += self.width // 2
            self.curr_y -= int(self.text_size * 1.5)

            self.timers[sym] = TimerLabel(name=key.symbol_string(sym), active=True,
                                          x=self.curr_x, y=self.curr_y, font_size=self.text_size)

    def on_key_release(self, sym, mod):
        if self.timers:
            self.timers[sym].active = False



def main():
    win = TimerApp()
    pyglet.app.run()


@click.command()
def run():
    main()



if __name__ == '__main__':
    main()