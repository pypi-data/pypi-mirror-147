from simple_ddl_parser import DDLParser

ddl="""
CREATE EXTERNAL TABLE IF NOT EXISTS schema.specific_table LIKE
schema.table_template LOCATION "/path/to/table" 
TBLPROPERTIES ("external.table.purge" = "true")
"""
result = DDLParser(ddl,normalize_names=True).run(output_mode="hql")

import pprint
pprint.pprint(result) 
