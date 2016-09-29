from chairman.data_mapper.db_connection import *
from chairman.data_mapper.fields import *
import sys


class Mapper:
    @classmethod
    def create_table(cls, model):
        sql_atts = []
        for a in model.Meta._attributes:
            sql_attr = a + ' '
            a_field = getattr(model, a)
            if a_field.field_type == 'foreign key':
                sql_attr += a_field.db_type
                sql_attr += ' references {table_name}({attribute})'.format(table_name=a_field.model.Meta.table_name,
                                                                           attribute=a_field.class_attribute)
            else:
                sql_attr += a_field.db_type
            if not a_field.null:
                sql_attr += ' NOT NULL'
            if a_field.is_primary_key():
                sql_attr += ' PRIMARY KEY'
                sql_atts.insert(0, sql_attr)
            else:
                sql_atts.append(sql_attr)
        table_attributes = ', '.join(sql_atts)
        sql = 'CREATE TABLE IF NOT EXISTS {table_name} ({attributes})'.format(table_name=model.Meta.table_name,
                                                                              attributes=table_attributes)
        DB.execute_sql(sql)

    @classmethod
    def drop_table(cls, model):
        sql = "DROP TABLE IF EXISTS {table_name}".format(table_name=model.Meta.table_name)
        DB.execute_sql(sql)

    @classmethod
    def add_column(cls, model, column_name, attribute):
        sql = "ALTER TABLE IF EXISTS {table_name} ADD COLUMN {attr_name} {attr_type}".format(
                                                                                    table_name=model.Meta.table_name,
                                                                                    attr_name=column_name,
                                                                                    attr_type=attribute.db_type)
        if not attribute.null:
            sql += " NOT NULL"
        if attribute.field_type == 'foreign key':
            sql += ' references {table_name}({attribute})'.format(table_name=model.Meta.table_name,
                                                                  attribute=attribute.class_attribute)
        elif attribute.is_primary_key:
            sql += ' primary key'
        DB.execute_sql(sql)

    @classmethod
    def drop_column(cls, model, column_name):
        sql = "ALTER TABLE IF EXISTS {table_name} DROP COLUMN {column_name}".format(table_name=model.Meta.table_name,
                                                                                    column_name=column_name)
        DB.execute_sql(sql)

    @classmethod
    def save(cls, obj):
        sql_atts = []
        sql_values = []
        if obj._new:
            for a in obj.Meta._attributes:
                if not obj._pk_mapper_created or obj._pk_mapper_created and a != 'id':
                    value = getattr(obj, a, '')
                    if value is not None and not isinstance(value, Field):
                        sql_atts.append(str(a))
                        sql_values.append(str(value))
            sql = "INSERT INTO {table_name} ({attributes}) VALUES ('{values}')".format(
                                                                                        table_name=obj.Meta.table_name,
                                                                                        attributes=', '.join(sql_atts),
                                                                                        values="', '".join(sql_values))
            try:
                if obj._pk_mapper_created:
                    sql += "RETURNING id"
                    obj.id = DB.execute_sql_with_return(sql)
                else:
                    DB.execute_sql(sql)
            except BaseException:
                return False
            return True
        else:
            for a in obj.Meta._attributes:
                if not obj._pk_mapper_created or obj._pk_mapper_created and a != 'id':
                    value = getattr(obj, a)
                    if value is not None and not isinstance(value, Field):
                        sql_values.append("{attribute}='{value}'".format(attribute=a, value=value))
            sql = "UPDATE {table_name} SET {values} WHERE {where}".format(table_name=obj.Meta.table_name,
                                                                          values=', '.join(sql_values),
                                                                          where="{pk}='{pk_value}'".format(
                                                                            pk=obj._pkey_attribute,
                                                                            pk_value=getattr(obj, obj._pkey_attribute)))
            try:
                DB.execute_sql(sql)
            except BaseException:
                return False
            return True

    @classmethod
    def find(cls, model, **kwargs):
        sql_where_atts = []
        for attr in kwargs:
            sql_where_atts.append("{attribute}='{value}'".format(attribute=attr, value=kwargs[attr]))
        sql = "SELECT * FROM {table_name} WHERE {where_atts}".format(table_name=model.Meta.table_name,
                                                                     where_atts=' and '.join(sql_where_atts))
        records = DB.execute_sql_with_return(sql)
        if len(records) > 1:
            kwargs_to_model = []
            for record in records[1:]:
                kw = {}
                for i, att in enumerate(record):
                    kw[records[0][i]] = record[i]
                kw['new'] = False
                kwargs_to_model.append(kw)
            return kwargs_to_model
        else:
            return None

    @classmethod
    def get_all(cls, model):
        sql = "SELECT * FROM {table_name}".format(table_name=model.Meta.table_name)
        records = DB.execute_sql_with_return(sql)
        if len(records) > 1:
            kwargs_to_model = []
            for record in records[1:]:
                kw = {}
                for i, att in enumerate(record):
                    kw[records[0][i]] = record[i]
                kw['new'] = False
                kwargs_to_model.append(kw)
            return kwargs_to_model
        else:
            return None

    @classmethod
    def delete(cls, model, **kwargs):
        sql_where_atts = []
        for attr in kwargs:
            sql_where_atts.append("{attribute}='{value}'".format(attribute=attr, value=kwargs[attr]))
        sql = "DELETE FROM {table_name} WHERE {where_atts}".format(table_name=model.Meta.table_name,
                                                                   where_atts=' and '.join(sql_where_atts))
        try:
            DB.execute_sql(sql)
        except BaseException:
            return False
        return True

    @classmethod
    def delete_all(cls, model):
        sql = "DELETE FROM {table_name}".format(table_name=model.Meta.table_name)
        try:
            DB.execute_sql(sql)
        except BaseException:
            return False
        return True