from chairman.data_mapper.model import *
import psycopg2
import unittest


class TestModel2(Model):
    pk = TextField('pk', primary_key=True)
    att1 = IntegerField('att1')


class TestModel(Model):
    att1 = TextField('qwe')
    fkey = ForeignKey('fkey', TestModel2)


class TestMapper(unittest.TestCase):
    def setUp(self):
        self.test_model_auto_pk = TestModel
        self.test_model_user_pk = TestModel2
        self.t11 = TestModel(att1='rgrgrg')
        self.t21 = TestModel2(pk='pk_1', att1=123)
        self.t22 = TestModel2(pk='pk_2', att1=9)
        Mapper.create_table(self.test_model_user_pk)
        Mapper.create_table(self.test_model_auto_pk)

    def test_insert(self):
        self.assertRaises(psycopg2.DatabaseError, self.t21.save())


class TestModels(unittest.TestCase):
    def setUp(self):
        self.test_model_auto_pk = TestModel
        self.test_model_user_pk = TestModel2
        self.t11 = TestModel(att1='rgrgrg')
        self.t21 = TestModel2(pk='pk_1', att1=123)
        self.t22 = TestModel2(pk='pk_2', att1=9)
        Mapper.create_table(self.test_model_user_pk)
        Mapper.create_table(self.test_model_auto_pk)

    def test_find(self):
        Mapper.delete(TestModel2, pk='pk_2')
        self.t22.save()
        self.assertEqual(TestModel2.find(pk='pk_2')[0].pk, 'pk_2')


class TestFields(unittest.TestCase):
    def setUp(self):
        self.test_model_auto_pk = TestModel
        self.test_model_user_pk = TestModel2
        self.text_field = TextField('tname')
        self.int_field = IntegerField('iname')
        self.pk_field = PKFieldSerial()
        self.foreign_key_field = ForeignKey('fkname', self.test_model_auto_pk)

    def test_is_field_type(self):
        self.assertTrue(self.text_field.is_field_type('text'))
        self.assertTrue(self.int_field.is_field_type(123))
        self.assertTrue(self.pk_field.is_field_type(123))
        self.assertTrue(self.foreign_key_field.is_field_type(123))

    def test_foreign_key_for_auto_created_id(self):
        self.assertTrue(self.foreign_key_field.field_type == 'foreign key')
        self.assertTrue(self.foreign_key_field.db_type == 'integer')
        self.assertTrue(self.foreign_key_field.link_type == 'int')

    def test_foreign_key_user_created(self):
        self.assertTrue(self.test_model_auto_pk.fkey.field_type == 'foreign key')
        self.assertTrue(self.test_model_auto_pk.fkey.db_type == 'text')
        self.assertTrue(self.test_model_auto_pk.fkey.link_type == 'str')

if __name__ == '__main__':
    unittest.main()
