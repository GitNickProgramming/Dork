# -*- coding: utf-8 -*-
"""Pytest Fixtures and utility methods for Dork.
"""
import pytest


def has_a(obj, attr):
    """has an attribute"""
    assert attr in vars(obj), f"{obj} has no {attr}"


def has_method(obj, method):
    """has a method"""
    assert hasattr(obj, method), f"{obj} has no {method}"


def is_a(obj, clazz):
    """Determines if an object is an instance of clazz.

        Basically a pytest `isinstance()' wrapper

    Args:
        obj (object): An instance of an object.
        clazz (type): The type of which obj is an instance.

    """

    if not isinstance(obj, (clazz)):
        pytest.fail(
            "{object} should be an instance of {clazz}".format(
                object=obj, clazz=clazz
            )
        )


def has_many(clz_instance, obj_key):
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
    clazz = clz_instance.__class__

    if obj_key not in vars(clz_instance):
        pytest.fail("{object} has no {key}".format(object=clazz, key=obj_key))

    contained = getattr(clz_instance, obj_key, None)
    if contained is None or "__getitem__" not in vars(type(contained)):
        pytest.fail(
            "{clazz}'s {key} should be a list-like object".format(
                clazz=clazz, key=obj_key
            )
        )
