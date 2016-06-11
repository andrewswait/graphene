from .field import Field, InputField
from .argument import Argument
from ..utils.orderedtype import OrderedType


# UnmountedType ?

class TypeProxy(OrderedType):
    '''
    This class acts a proxy for a Graphene Type, so it can be mounted
    as Field, InputField or Argument.

    Instead of doing
    >>> class MyObjectType(ObjectType):
    >>>     my_field = Field(String(), description='Description here')

    You can actually do
    >>> class MyObjectType(ObjectType):
    >>>     my_field = String(description='Description here')

    So is simpler to use.
    '''

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super(TypeProxy, self).__init__()

    def get_type(self):
        return self._meta.graphql_type

    def as_field(self):
        return Field(
            self.get_type(),
            *self.args,
            _creation_counter=self.creation_counter,
            **self.kwargs
        )

    def as_inputfield(self):
        return InputField(
            self.get_type(),
            *self.args,
            _creation_counter=self.creation_counter,
            **self.kwargs
        )

    def as_argument(self):
        return Argument(
            self.get_type(),
            *self.args,
            _creation_counter=self.creation_counter,
            **self.kwargs
        )

    def as_mounted(self, cls):
        from .inputobjecttype import InputObjectType
        from .objecttype import ObjectType
        from .interface import Interface

        if issubclass(cls, (ObjectType, Interface)):
            inner = self.as_field()
        elif issubclass(cls, (InputObjectType)):
            inner = self.as_inputfield()
        else:
            raise Exception('TypedProxy "{}" cannot be mounted in {}'.format(self.get_type(), cls))

        return inner