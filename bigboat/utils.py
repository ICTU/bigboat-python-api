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

from functools import partial
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
