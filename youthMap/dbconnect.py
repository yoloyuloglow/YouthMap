import oracledb 


def dbcon():
    return oracledb.connect(user="계정 이름", password="비번", dsn="주소")   # DB에 연결 (호스트이름 대신 IP주소 가능)

def insert_data(id, name, passwd, email, address, birth):
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"insert into user_db(id, name, passwd, email, address, birth) values ('{id}','{name}','{passwd}','{email}','{address}','{birth}')")
        db.commit()  # commit 을 해야 db에 적용이 됩니다
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()

def select_all():
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        con.execute("select * from user_db")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret

def select_all_data():
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        con.execute("select * from youth_build")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret

def select_login(id, passwd):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"select * from user_db where id='{id}' and passwd = '{passwd}'")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret
    
    
def select_id(id):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"select * from user_db where id='{id}'")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret

def select_id_only(id):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"select id from user_db where id='{id}'")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()
        return ret

def update_ll(idx, latit, longit):
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"update youth_build set latitude='{latit}',longitude='{longit}' where idx ='{idx}'")
        db.commit()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()

def select_name(idx, name):
    ret = []
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"select name from youth_build where idx='{idx}'")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)
    finally:
        con.close(),
        db.close()
        return ret
    
def insert_like(id, idx):  #유저 아이디랑 시설 번호
    
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"insert into user_favorites(user_id, facility_id) values ('{id}','{idx}')")
        db.commit()  
    except Exception as e:
        print('db error:',e)
    finally:
        con.close()
        db.close()

def select_like_count(id, idx):
    ret = None
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"select * from user_favorites where user_id='{id}' AND facility_id='{idx}'")
        ret = con.fetchone()
    except Exception as e:
        print('db error:',e)    
    finally:
        con.close()
        db.close()
        return ret

def delete_like(id, idx):
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"delete from user_favorites where user_id='{id}' and facility_id='{idx}'")
        db.commit() 
    except Exception as e:
        print('db error:',e)    
    finally:
        con.close()
        db.close()

def select_like(id):
    ret = None
    try:
        db = dbcon()
        con = db.cursor()
        con.execute(f"select youth_build.* from youth_build join user_favorites on youth_build.idx = user_favorites.facility_id where user_id='{id}'")
        ret = con.fetchall()
    except Exception as e:
        print('db error:',e)    
    finally:
        con.close()
        db.close()
        return ret