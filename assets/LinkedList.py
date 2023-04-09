 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from typing import Optional, Callable
from dataclasses import dataclass

class LinkedList:
    def __init__(self, iterable=None):
        self.leftmost: Optional[LinkedListElement] = None
        self.rightmost: Optional[LinkedListElement] = None

        if iterable is not None:
            for el in iterable:
                self.insertRight(el)

    def insertLeft(self, element):
        new: LinkedListElement = LinkedListElement(element)
        if self.rightmost is None:  
            self.leftmost = new
            self.rightmost = new
        elif self.leftmost is not None:
            new.next = self.leftmost
            self.leftmost.previous = new
            self.leftmost = new

    def insertRight(self, element):
        new: LinkedListElement = LinkedListElement(element)
        if self.leftmost is None:  
            self.leftmost = new
            self.rightmost = new
        elif self.rightmost is not None:
            new.previous = self.rightmost
            self.rightmost.next = new
            self.rightmost = new
            
    def __iter__(self):
        if self.leftmost is None:
            return

        current = self.leftmost
        while True:
            yield current.element

            current = current.next
            if current is None:
                break

    def __len__(self):
        return len([True for _ in self])

    def removeElement(self, element, onRemove=None, removeAll: bool = False):
        shouldRemove = (lambda current: current.element == element or current == element)
        self.removeWith(shouldRemove=shouldRemove, onRemove=onRemove, removeAll=removeAll)

    def removeWith(self, shouldRemove: Callable[["LinkedListElement"], bool],
                   onRemove: Callable = None, removeAll: bool = False):
        if self.leftmost is None:
            return
        current = self.leftmost
        while current is not None:
            if shouldRemove(current):
                if current.previous is not None:
                    current.previous.next = current.next
                else:
                    self.leftmost = current.next

                if current.next is not None:
                    current.next.previous = current.previous
                else:
                    self.rightmost = current.previous

                if onRemove is not None:
                    onRemove(current.element)
                current.element = None

                if not removeAll:
                    return
            current = current.next



@dataclass
class LinkedListElement:
    element: any
    previous: Optional["LinkedListElement"] = None
    next: Optional["LinkedListElement"] = None
