import collections

from graphql_relay.connection.arrayconnection import (
    connectionFromArray
)
from graphql_relay.connection.connection import (
    connectionArgs
)
from graphene.core.fields import Field
from graphene.utils import cached_property
from graphene.relay.utils import get_relay


class ConnectionField(Field):
    def __init__(self, field_type, resolve=None, description=''):
        super(ConnectionField, self).__init__(field_type, resolve=resolve, 
                                              args=connectionArgs, description=description)

    def resolve(self, instance, args, info):
        resolved = super(ConnectionField, self).resolve(instance, args, info)
        if resolved:
            assert isinstance(resolved, collections.Iterable), 'Resolved value from the connection field have to be iterable'
            return connectionFromArray(resolved, args)

    @cached_property
    def type(self):
        object_type = self.get_object_type()
        relay = get_relay(object_type._meta.schema)
        assert issubclass(object_type, relay.Node), 'Only nodes have connections.'
        return object_type.connection