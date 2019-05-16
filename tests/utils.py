# -*- coding: utf-8 -*-
"""Pytest Fixtures and utility methods for Dork.
"""
import pytest


def is_a(obj, clazz):
    """Determines if an object is an instance of clazz.

        Basically a pytest `isinstance()' wrapper

    Args:
        obj (object): An instance of an object.
        clazz (type): The type of which obj is an instance.

    """
    if not isinstance(obj, (clazz,)):
        pytest.fail(
            "{object} should be an instance of {clazz}".format(
                object=obj, clazz=clazz
            )
        )


def has_many(clazz, clz_key, obj, obj_key):
    """Determines if an obj responds to a `has_many' relationship.

        [obj] 0..N ==> 1 [clazz]

        Given a class(clazz), and an object(obj),
        The class should have many objects.

        Given an object(obj), and a key,
        The object should reference it's class through the key

        Given a class(clazz), and a plural key (clz_key),
        The class should refence it's objects though the plural key.

    Args:
        clazz(object): The type of the container class.
        obj (object): An instance of the contained object.
        clz_key (str): The key to which clazz should respond.
        obj_key (str): The key to which object should respond.

    """
    obj_instance = obj()
    clz_instance = clazz()
    if clz_key not in vars(obj_instance):
        pytest.fail("{object} has no {key}".format(object=obj, key=clz_key))

    if obj_key not in vars(clz_instance):
        pytest.fail("{object} has no {key}".format(object=clazz, key=obj_key))

    container = getattr(obj_instance, clz_key, None)
    if not isinstance(container, clazz):
        pytest.fail(
            "A(n) {object}'s {key} should referer to a {clazz}".format(
                object=obj, key=clz_key, clazz=clazz
            )
        )

    contained = getattr(clz_instance, obj_key, None)
    if contained is None or "__getitem__" not in vars(type(contained)):
        pytest.fail(
            "{clazz}'s {key} should be a list-like object".format(
                clazz=clazz, key=obj_key
            )
        )
