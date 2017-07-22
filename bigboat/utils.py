"""
Utilities in the BigBoat API library.

Copyright 2017 ICTU

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from functools import partial, wraps, WRAPPER_ASSIGNMENTS
from past.builtins import basestring

def readonly(*args, **kwargs):
    """
    Register readonly properties for member variables of a class instance.

    Args:
        *args: Variable length list of properties to register as providers of
            read-only access to protected member variables with the same name,
            prefixed with an underscore '_'.
        **kwargs: Arbitrary keyword arguments of properties (keywords) to
            register as providers of read-only access to protected member
            variables with the same name as the argument value.

    Returns:
        A decorator function that applies on a class to provide read-only
        member properties.
    """

    if args and not isinstance(args[0], basestring):
        properties = args[0]
    else:
        properties = args

    aliased_properties = kwargs

    def decorator(subject):
        """
        Register the properties in the class.

        Args:
            subject: The class instance.

        Returns:
            The altered class instance.
        """

        def _get_property(property_name, instance):
            return getattr(instance, property_name)

        for property_name in properties:
            setattr(subject, property_name,
                    property(fget=partial(_get_property, '_' + property_name)))
        for variable_name, property_name in aliased_properties.items():
            setattr(subject, property_name,
                    property(fget=partial(_get_property, '_' + variable_name)))

        return subject

    return decorator

class Inherited(object):
    """
    Indicate that an inherited method whose parent method has documentation.

    This solution is based on the 'Docstring inheritance decorator' Python
    recipe from http://code.activestate.com/recipes/576862/ which is licensed
    under the MIT License (but none of the code was used verbatim).
    """

    _wrappers = tuple(prop for prop in WRAPPER_ASSIGNMENTS if prop != '__doc__')

    def __init__(self, method):
        self._method = method

    def __get__(self, im_self, im_class):
        if im_self is not None:
            method, overridden, doc = self.get_object_parent(im_class, im_self)
        else:
            method, overridden, doc = self.get_class_parent(im_class)

        # Prefer original documentation from the inheriting method.
        if doc is not None:
            method.__doc__ = doc
        elif overridden is not None:
            method.__doc__ = overridden.__doc__

        return method

    def get_object_parent(self, im_class, im_self):
        """
        Determine the parent method using the class and instance context.

        Args:
            im_class: The method's class instance.
            im_self: The method's bound object instance.

        Returns:
            A tuple:
            - The wrapped method.
            - The parent method or `None` if it was not found.
            - The original documentation of the method or `None` if there is no
              documentation on the inheriting method.
        """

        @wraps(self._method, assigned=self._wrappers)
        def wrapper(*args, **kwargs):
            """
            Wrapper for the actual method.
            """

            return self._method(im_self, *args, **kwargs)

        parent = super(im_class, im_self)
        overridden = getattr(parent, self._method.__name__, None)
        return wrapper, overridden, self._method.__doc__

    def get_class_parent(self, im_class):
        """
        Determine the parent method using the class context.

        Args:
            im_class: The method's class instance.

        Returns:
            A tuple:
            - The wrapped method.
            - The parent method or `None` if it was not found.
            - The original documentation of the method or `None` if there is no
              documentation on the inheriting method.
        """

        func = self._method.__func__
        name = func.__name__
        doc = func.__doc__

        @wraps(func, assigned=self._wrappers)
        def wrapper(*args, **kwargs):
            """
            Wrapper for the actual function behind the classmehod.
            """

            return func(im_class, *args, **kwargs)

        parents = im_class.__mro__[1:]
        for parent in parents:
            overridden = getattr(parent, name, None)
            if overridden is not None:
                return wrapper, overridden, doc

        return wrapper, None, doc
