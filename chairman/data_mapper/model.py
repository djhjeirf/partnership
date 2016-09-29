from chairman.data_mapper.fields import *
from chairman.data_mapper.mapper import *
import re, itertools, collections
from collections import OrderedDict


class ModelBase(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __init__(cls, name, bases, classdict):
        if 'Meta' in classdict:
            Meta = classdict['Meta']
        else:
            class Meta:
                pass

        # Присваиваем имя таблицы, если не задано
        if 'Meta' in classdict and classdict['Meta'].table_name == '' or 'Meta' not in classdict:
            words = re.findall('[A-Z][^A-Z]*', name)
            if words:
                Meta.table_name = '_'.join(words).lower()
            else:
                Meta.table_name = name

        # Нужен ли первичный ключ от модели + записываем все пользовательские атрибуты в список (только от Field)
        need_id = True
        attributes = []
        for attr in classdict:
            if isinstance(classdict[attr], Field):
                if classdict[attr].is_primary_key():
                    setattr(cls, '_pkey_attribute', str(attr))
                    setattr(cls, '_pk_mapper_created', False)
                    need_id = False
                attributes.append(attr)
        if need_id:
            setattr(cls, 'id', PKFieldSerial()) # Вот как важно не забыть, если можно ()
            setattr(cls, '_pk_mapper_created', True)
            setattr(cls, '_pkey_attribute', 'id')
            attributes.append('id')
        Meta._attributes = attributes
        setattr(cls, 'Meta', Meta)  # Оно перезаписывает Meta, если существует
        super().__init__(name, bases, classdict)


class Model(metaclass=ModelBase):
    class Meta:
        table_name = ''  # Для бд
        _attributes = []  # Заполнится само

    def __init__(self, *args, **kwargs):
        self._new = kwargs.get('new', True)
        attributes = self.Meta._attributes[:]
        if args:
            atts = list(zip(attributes, args))
            for a in atts:  # [0] - атрибут, [1] - значение
                if a[0] in attributes:
                    self.try_to_save_value(a[0], a[1])
        if kwargs:
            if 'id' in kwargs and self._new:
                del kwargs['id']
            for attr in list(kwargs):
                if attr in attributes:
                    self.try_to_save_value(attr, kwargs[attr])
                    attributes.remove(str(attr))
            for attr in attributes:
                setattr(self, attr, None)
        self.delete = self._delete
        # Проверить оставшиеся атрибуты на nullable или нет

    def save(self):
        if Mapper.save(self):  # После сохранения автоматически созданное поле id будет заполнено из бд
            self._new = False

    @classmethod
    def find(cls, **kwargs):
        kw = Mapper.find(cls, **kwargs)
        if kw:
            objects = []
            for k in kw:
                obj = cls(**k)
                objects.append(obj)
            return objects
        else:
            return None

    @classmethod
    def get_all(cls):
        kw = Mapper.get_all(cls)
        if kw:
            objects = []
            for k in kw:
                obj = cls(**k)
                objects.append(obj)
            return objects
        else:
            return None

    @classmethod
    def delete(cls, **kwargs):
        Mapper.delete(cls, **kwargs)

    @classmethod
    def delete_all(cls):
        Mapper.delete_all(cls)

    def _delete(self):
        kwargs = {}
        for a in self.Meta._attributes:
            kwargs[a] = getattr(self, a)
        self.__class__.delete(**kwargs)

    def set_new_values(self, **kwargs):
        for a in kwargs:
            if a in self.Meta._attributes:
                self.try_to_save_value(a, kwargs[a][0])

    def try_to_save_value(self, attribute_name, attribute_value):  # От POST может приходить []
        # TODO Преобразование даты в обе? стороны Могли остаться ошибки
        if isinstance(attribute_value, list):
            value = attribute_value[0]
        else:
            if attribute_name.startswith('_'):
                value = None
            else:
                value = attribute_value
        attr_field = getattr(self.__class__, attribute_name)
        if attr_field.is_field_type(value):
            setattr(self, attribute_name, value)
        else:
            if value != '' and value is not None:
                if attr_field.field_type == 'int' or attr_field.field_type == 'serial':
                    setattr(self, attribute_name, int(value))
                elif attr_field.field_type == 'float':
                    setattr(self, attribute_name, float(value))
                elif attr_field.field_type == 'date':
                    if isinstance(value, str):
                        setattr(self, attribute_name, value)
                    else:
                        setattr(self, attribute_name, value.strftime("%d-%m-%Y"))
                elif attr_field.field_type == 'foreign key':
                    if attr_field.link_type == 'int':
                        setattr(self, attribute_name, int(value))
                    elif attr_field.link_type == 'float':
                        setattr(self, attribute_name, float(value))
