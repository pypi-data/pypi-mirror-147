"""
Created on Tue May  4 15:59:03 2021

@author: Braxton Brown
"""
from math import log
import time
import sys
from types import GeneratorType


class ProgressBar:
    def __init__(self, items, completed=0, maxlen=25, char='█', show_on_update=True, ips=1, lsttime=None, lr=0.1, use_average=(False, 1000)):
        '''
        Progress Bar that shows usefull information about the progress of a task.

        Parameters
        ----------
        items : int
            The number of items to be completed.
        completed : int, optional
            The number of items that have been completed. Defaults to 0.
        maxlen : int, optional
            The maximum length of the progress bar. The default is 25.
        char : str, optional
            The character to be used for the progress bar. The default is '█'.
        show_on_update : bool, optional
            Whether or not to show the progress bar when updating. The default is True.
        ips : float, optional
            The initial items per second. The default is 1.
        lsttime : float, optional
            The last time the progress bar was updated. The default is None.
        lr : float, optional
            The learning rate. The default is 0.1.
        use_average[use_average, number of times to save] : iterable, optional
            Whether or not to use the average of the items per second. The default is (False, 1000).
        '''
        self.completed = completed
        if hasattr(items, '__iter__') and not isinstance(items, GeneratorType):
            self.items = len(items)
            self.enums = items
        else:
            self.items = items
        self.maxlen = maxlen
        self.pos = 0
        self.char = char
        self.items_per_sec = ips
        self.last_time = lsttime or 0
        self.lr = lr
        self.show_on_update = show_on_update
        if use_average[0]:
            self.use_average = use_average
            self.times = [None for i in range(use_average[1])]
            self.average_count = 0
        else:
            self.use_average = False

    def __repr__(self):
        return str(self.pos)

    def __value__(self):
        return self.pos

    def __add__(self, other):
        return self.completed + other

    def __sub__(self, other):
        return self.completed - other

    def __mul__(self, other):
        return self.completed * other

    def __div__(self, other):
        return self.completed / other

    def __iter__(self):
        for i in range(self.items):
            self.update()
            yield self.enums[i]

    def __iadd__(self, other):
        self.update(other)
        return self

    def format_time(self):
        '''
        Formats the time left to completion in format hh:mm:ss.
        '''
        secs = (self.items-self.completed)/self.items_per_sec
        return f'{int(secs//3600)}:{int(secs//60)%60:02}:{int(secs%60):02} '

    def show(self):
        '''
        Shows the progress bar.
        '''
        st = ''
        if self.items:
            st = 'Eta: ' + self.format_time() + '| '
            ips = self.items_per_sec
            st += str(round(ips, 2)) + ' items/s' if ips > 1 else str(round(1/ips, 2)) + ' s/item'

        sys.stdout.write(
            f'\r{f"{str(self.completed).rjust(int(log(self.items,10)+.5))}/{self.items}" if self.items else ""} \
{str(round(self.pos*100,2)).ljust(5)}% \
[{(self.char*int(self.pos*self.maxlen)).ljust(self.maxlen)}] {st}\t')

    def update(self, n=1):
        '''
        Updates the progress bar.

        Parameters
        ----------
        n : int, optional
            The number of items completed since previous call. Defaults to 1.
        '''
        completed = self.completed + n
        if self.items:
            t = time.perf_counter() - self.last_time if self.last_time else self.items_per_sec
            if t != 0 or completed == self.completed:
                if self.use_average:
                    self.times[self.average_count] = t
                    self.average_count += 1
                    self.average_count %= self.use_average[1]
                    self.items_per_sec = sum(self.times[:min(completed, len(self.times))])/min(completed, len(self.times))
                else:
                    self.items_per_sec += self.lr * (n/t - self.items_per_sec)
                self.last_time = time.perf_counter()
                self.completed = completed
                self.pos = completed/self.items
            elif completed == self.items:
                self.completed = completed
                self.pos = completed/self.items
        else:
            self.pos = completed
        if self.show_on_update:
            self.show()


if __name__ == '__main__':
    for i in ProgressBar(range(2000), use_average=(True, 100)):
        time.sleep(.69)
