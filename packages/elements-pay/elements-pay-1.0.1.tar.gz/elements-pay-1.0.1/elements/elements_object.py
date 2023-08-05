from __future__ import absolute_import


class ElementsObject(dict):
    def __init__(self):
        super(ElementsObject, self).__init__()

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as err:
            raise AttributeError(*err.args)
