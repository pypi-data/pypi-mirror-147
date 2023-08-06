# _*_ coding: UTF-8 _*_ 
def sql2df(host,user,password,sql):
    from livy import LivySession, SessionKind
    from requests.auth import HTTPBasicAuth
    import random
    livyname=f"""{user}\n川A{''.join(random.choices(list('ABCDEFGHJKLMNPQRSTUVWXYZ1234567890'), k=5))}"""   
    LIVY_SERVER = f"http://{host}:8998"
    auth = HTTPBasicAuth(user,password)
    with LivySession.create(LIVY_SERVER,
                            auth=auth,
                            verify=False,
                            name=livyname
                           ) as session:
        try:
            session.run(f"df = spark.sql('''{sql}''')")
            df_ = session.download('df')
        except:
            df_=None
            print('请检查SQL代码是否有错!')
    return df_
if __name__ == '__main__':
    pass
