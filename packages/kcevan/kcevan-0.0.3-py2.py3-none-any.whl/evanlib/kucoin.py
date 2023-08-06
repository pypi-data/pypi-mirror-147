# _*_ coding: UTF-8 _*_ 
'''
@Project->File: user_portrait->file2
@Author: Simon.li
@Time: 2022/4/14 14:52
@Description: 
@Edition: V1
'''
def sql2df(host,user,password,sql):
    from livy import LivySession, SessionKind
    from requests.auth import HTTPBasicAuth
    import random
    license_plate_num = [
        "A","B","C","D","E","F","G","H",
        "J","K","L","M","N","P","Q","R",
        "S","T","U","V","W","X","Y","Z",
        "1","2","3","4","5","6","7","8","9","0"]
    livyname=f"""川A.{''.join(random.choices(license_plate_num, k=5))}  {user}"""    
    LIVY_SERVER = f"http://{host}:8998"
    auth = HTTPBasicAuth(user,password)
    with LivySession.create(LIVY_SERVER,
                            auth=auth,
                            kind=SessionKind.SQL,
                            verify=False,
                            name=livyname
                           ) as session:
        df_=session.download_sql(sql)
    return df_
if __name__ == '__main__':
    pass
