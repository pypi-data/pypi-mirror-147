# _*_ coding: UTF-8 _*_ 
from hdfs import InsecureClient
import pandas as pd
from livy import LivySession, SessionKind
from requests.auth import HTTPBasicAuth
import random

class kcspark():
    def __init__(self,host,user,password,**kw):
        self.host=host
        self.user=user
        self.password=password
        for k,w in kw.items():
            setattr(self,k,w)
    def hdfs2df(self,folder_):
        fname=''
        client = InsecureClient('http://172.26.2.116:50070', user='evan.tang')
        for f in client.list(f'/user/{self.user}/{folder_}'):
            if f.split('.')[-1]=='csv':
                fname=f
        with client.read(f'/user/{self.user}/{folder_}/{fname}', encoding = 'utf-8') as reader:
            df = pd.read_csv(reader,index_col=0)
        return df            
    def sql2df(self,sql):
        seq=''.join(random.choices(list('ABCDEFGHJKLMNPQRSTUVWXYZ12345678901234567890'), k=5))
        livyname=f"""{self.user}川A{seq}"""   
        LIVY_SERVER = f"http://{self.host}:8998"
        auth = HTTPBasicAuth(self.user,self.password)
        path=f'hdfs:///user/{self.user}/{seq}'
        with LivySession.create(LIVY_SERVER,
                                auth=auth,
                                verify=False,
                                name=livyname,
                                driver_memory="10g"
                               ) as session:
            try:
                session.run(f"""df=spark.sql('''{sql}''')""")
                session.run(f"""df.repartition(1).write.format('com.databricks.spark.csv').mode('overwrite').save('{path}',header = 'true')""")
                df_=self.hdfs2df(seq)
                session.run("""fs = (sc._jvm.org.apache.hadoop.fs.FileSystem.get(sc._jsc.hadoopConfiguration()))""")
                session.run(f"""fs.delete(sc._jvm.org.apache.hadoop.fs.Path('{path}'), True)""")
            except:
                print('查询失败！')
                df_=None
        return df_
if __name__ == '__main__':
    pass
