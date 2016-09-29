from chairman.data_mapper.model import *
from chairman.models import *
import os

old_state = {'model1': ['a1', 'a2'], 'model2': ['a1']}
new_state = {'model1': ['a1', 'a2', 'a3'], 'model3': ['a1']}

print_sql_result(Rightholder.get_owner_id('rgr tesefdfe ffg 11-11-2044'))