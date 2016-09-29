import sys


class Field:
    field_type = 'field'

    def __init__(self, name,  alt_name=None, null=True, primary_key=False):
        self.null = null
        self.name = name
        self.primary_key = primary_key
        self.alt_name = alt_name

    @classmethod
    def is_field_type(cls, obj):
        if obj.__class__.__name__ == cls.field_type:
            return True
        else:
            return False

    def is_primary_key(self):
        return self.primary_key

    @classmethod
    def get_type(cls):
        return cls.field_type

    def __str__(self):
        return str(self.field_type)


class PKFieldSerial(Field):
    field_type = 'serial'
    db_type = 'serial'

    def is_field_type(cls, obj):
        if obj.__class__.__name__ == 'int':
            return True
        else:
            return False

    def __init__(self, name='id', null=False, primary_key=True):
        super(PKFieldSerial, self).__init__(name, null=null, primary_key=primary_key)


class TextField(Field):
    field_type = 'str'
    db_type = 'text'


class FloatField(Field):
    field_type = 'float'
    db_type = 'real'


class IntegerField(Field):
    field_type = 'int'
    db_type = 'integer'


class DateField(Field):
    field_type = 'date'
    db_type = 'date'

    def is_field_type(cls, obj):
        if obj.__class__.__name__ == 'text':
            return True
        else:
            return False


class ForeignKey(Field):
    field_type = 'foreign key'
    db_type = 'foreign key'

    def __init__(self, name, alt_name, model, null=True):
        self.model = model
        self.class_attribute = model._pkey_attribute
        self.link_type = getattr(model, model._pkey_attribute).field_type
        self.db_type = getattr(model, model._pkey_attribute).db_type
        if self.link_type == 'serial':
            self.link_type = 'int'
            self.db_type = 'integer'
        super(ForeignKey, self).__init__(name, alt_name=alt_name, null=null)

    def is_field_type(self, obj):
        if obj.__class__.__name__ == self.link_type:
            return True
        else:
            return False

    def is_primary_key(self):
        return False
