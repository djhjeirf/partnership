import chairman.models
from chairman.models import *
from chairman.data_mapper.migrations.state import state
import importlib, inspect, os


class DBAction:
    pass


class CreateTable(DBAction):
    def __init__(self, table_name):
        self.table_name = table_name


class DropTable(DBAction):
    def __init__(self, table_name):
        self.table_name = table_name


class AddColumn(DBAction):
    def __init__(self, table_name, attribute_name):
        self.table_name = table_name
        self.attributes = attribute_name


class DropColumn(DBAction):
    def __init__(self, table_name, attribute_name):
        self.table_name = table_name
        self.attributes = attribute_name


class Migration(DBAction):
    def __init__(self, diffs):
        self.applied = False
        ops = []
        dif_tables = diffs[0]
        dif_columns = diffs[1]
        for t in dif_tables:
            if t[1] == 'created':
                ops.append(CreateTable(t[0]))
            elif t[1] == 'dropped':
                ops.append(DropTable)
        for c in dif_columns:
            if c[2] == 'added':
                ops.append(AddColumn(t[0], t[1]))
            elif c[2] == 'dropped':
                ops.append(DropColumn(t[0], t[1]))
        files = []
        for file in os.listdir(os.getcwd()):
            if file.startswith('m_'):
                files.append(file)
        if len(dif_tables) > 0 or len(dif_columns) > 0:
            self.ops = ops
            if len(files) == 0:
                new_migration_file_name = 'm_000'
            else:
                new_migration_file_name = int(files[-1][-3:])
            new_migration_file_name += '.py'
            new_migration_file = open(new_migration_file_name, 'w')
            new_migration_file.writelines("dif_tables = " + str(dif_tables) + '\n')
            new_migration_file.writelines("dif_columns = " + str(dif_columns))
        else:
            printt("No changes found")


def diff(new_state, old_state):
    dif_table = []  # Состоит из списков вида ['model_name', 'created/dropped']
    dif_columns = []  # Состоит из списков вида ['model_name', 'attribute_name', 'added/dropped']
    for model_name in new_state:
        if model_name not in old_state:
            dif_table.append([model_name, 'created'])
        else:
            for a in new_state[model_name]:
                if a not in old_state[model_name]:
                    dif_columns.append([model_name, a, 'added'])
    for model_name in old_state:
        if model_name not in new_state:
            dif_table.append([model_name, 'dropped'])
        else:
            for a in new_state:
                if a not in new_state:
                    dif_columns.append([model_name, a, 'dropped'])
    return [dif_table, dif_columns]


def get_new_state():
    state = {}
    module = importlib.import_module('chairman.models')
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, Model) and obj is not Model:
            model_atts = obj.Meta._attributes
            state[obj.__name__] = model_atts
    printt(state)
    return state


def save_state(state):
    state_file = open('state.py', 'w')
    state_file.write("state = " + str(state))


def get_last_migration():
    files = []
    for file in os.listdir(os.getcwd()):
        if file.startswith('m_'):
            files.append(file)
    if len(files) == 0:
        return None
    else:
        return files[-1]
