# Fork of Typeshed's stubs to work around explicit export issue
# https://github.com/py-vobject/vobject/issues/53.
from .base import Component
from .base import readComponents as readComponents

def iCalendar() -> Component: ...
def vCard() -> Component: ...
