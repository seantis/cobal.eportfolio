import uuid

from sqlalchemy import String
from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.postgresql import base as postgresql_base

class UUID(TypeDecorator):
    impl = String
    impl.length = 36
         
    def process_bind_param(self, value, dialect):
        if value and isinstance(value, uuid.UUID):
            return str(value)
        elif value and isinstance(value, basestring):
            return str(uuid.UUID(value))
        return None
         
    def process_result_value(self, value, dialect):
        if value:
            return uuid.UUID(value)
        return None
         
    def copy(self):
        return UUID(self.impl.length)
        
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return postgresql_base.UUID()
        return String(36)