from textual.app import ComposeResult
from textual.widgets import Static


class TimerBar(Static):
    """A widget that displays a scale and numbers to mimic the
    classic pomodoro (tomato-shaped) kitchen timer.
    """

    bar_size: int = 60
    bar_mid = int(bar_size / 2)

    def compose(self) -> ComposeResult:
        yield Static("", id="numbers")
        yield Static("", id="scale")

    def on_mount(self) -> None:
        s = "_" * (self.bar_mid)
        # s += "^"
        s += "\u25b2"  #  "BLACK UP-POINTING TRIANGLE"
        s += "_" * (self.bar_mid - 1)
        self.query_one("#scale").update(s)

    def update_bar(self, counter: int) -> None:
        label_interval = 5
        bar = ["." for _ in range(self.bar_size)]
        for i in range(self.bar_size):
            x = counter + (i - self.bar_mid)
            if x < 0:
                x = self.bar_size + x
            elif x > self.bar_size - 1:
                x = abs(self.bar_size - x)
            if x % label_interval == 0:
                sx = str(x)
                if len(sx) == 1:
                    bar[i] = sx
                elif i > 0:
                    #  This puts the second character of the two-digit number
                    #  at the corresponding index.
                    bar[i - 1] = sx[0]
                    bar[i] = sx[1]
        self.query_one("#numbers").update("".join(bar))
