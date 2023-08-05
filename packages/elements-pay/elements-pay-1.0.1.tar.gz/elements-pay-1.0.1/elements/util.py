from __future__ import absolute_import

import logging

from elements import six

from elements.elements_object import ElementsObject


logger = logging.getLogger("elements")


def convert_to_elements_object(data):
    if isinstance(data, list):
        return [convert_to_elements_object(elem) for elem in data]

    if isinstance(data, dict):
        klass_name = data.get("type")
        if isinstance(klass_name, six.string_types):
            klass = get_object_class(klass_name)
        else:
            klass = ElementsObject
        instance = klass()
        for k, v in six.iteritems(data):
            super(ElementsObject, instance).__setitem__(
                k, convert_to_elements_object(v)
            )
        return instance

    return data


def get_object_class(klass_name):
    # avoid circular dependency
    from elements.object_types import OBJECT_TYPES

    return OBJECT_TYPES.get(klass_name, ElementsObject)


def log_debug(message, **params):
    _log(logging.DEBUG, message, **params)


def log_info(message, **params):
    _log(logging.INFO, message, **params)


def log_error(message, **params):
    _log(logging.ERROR, message, **params)


def _log(level, message, **params):
    def _fmt(key, val):
        return "{key}={val}".format(key=key, val=val)

    props = dict(message=message, **params)
    fmt_msg = " ".join([_fmt(k, v) for k, v in sorted(props.items())])
    logger.log(level, fmt_msg)
