dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
cursor=con.cursor()