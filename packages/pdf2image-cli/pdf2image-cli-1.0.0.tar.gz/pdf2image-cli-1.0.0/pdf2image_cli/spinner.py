'''
Spinner
Spinner class that enables Halo. Not yet implemented.

'''

from halo import Halo
import time


class Spinner:
    def __init__(self, color="cyan", spinner="dots") -> None:
        self.spinner = Halo("", color=color, spinner=spinner, enabled=False)
        pass

    def start(self, text=None):
        if text:
            self.spinner.text = text
        self.spinner.enabled = True
        self.spinner.start()

    def changeText(self, text=None):
        self.spinner.text = text

    def succeed(self, text=None):
        self.spinner.succeed(text)

    def stop(self):
        self.spinner.stop()

    def fail(self, text=None):
        self.spinner.fail(text)

    def warn(self, text=None):
        self.spinner.warn(text)

    def info(self, text=None):
        self.spinner.info(text)


if __name__ == "__main__":
    spinner = Spinner()
    spinner.start("Converting PDF")
    time.sleep(2)
    spinner.succeed()
    spinner.start('Saved Image X')
    time.sleep(1)
