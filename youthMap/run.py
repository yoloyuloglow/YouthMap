
from flask import Flask
import dbconnect as db

app = Flask(__name__)


from flask import render_template,session, request, flash, jsonify, make_response
import hashlib
import jwt  #pyjwt 패키지
import datetime  # 토큰 만료시간


app.secret_key = 'PANDA'  #jwt 토큰 생성 시 필요한 암호화 문자열

@app.route('/')    
def homepage():
    return render_template('main.html')


@app.route('/like')
def like_page():
    log = session.get('logged_in')
    if log==True:
        return render_template('likes.html')
    else:
        flash('로그인이 필요합니다')
        return render_template('main.html')
        
    
@app.route('/sign_in')
def login():
    msg = request.args.get("msg")   #?
    return render_template('sign_in.html', msg=msg)


@app.route('/sign_up')
def register():
    return render_template('sign_up.html') 

@app.route('/youth_map')
def map():
    return render_template('youth_map.html') 

@app.route('/get_data',methods=['GET'])
def get_data():
    fac_list = []
    
    data = db.select_all_data()
    for i in data:
        idx = i[0]
        city = i[1]
        div = i[2]
        name = i[3]
        add = i[4]
        phone = i[5]
        owner = i[6]
        source = i[7]
        open = i[8]
        created = i[9]
        renewal = i[10]
        lat = i[11]
        git = i[12]

        
        fac_list.append(
            {
            "idx" : idx,
            "city" : city,
            "division" : div,
            "name" : name,
            "address" : add,
            "phone" : phone,
            "owner" : owner,
            "source" : source,
            "open" : open,
            "created" : created,
            "renewal" : renewal,
            "lat" : lat,
            "git" : git
            }
        ) 

    return {'fac_list':fac_list}

@app.route('/get_like', methods = ['GET'])
def get_like():
    log = session.get('id')
    print(log)
    fac_list = []
    # 데이터베이스에서 데이터 가져오기
    data = db.select_like(log)
    print(data)
    for i in data:
        idx = i[0]
        city = i[1]
        div = i[2]
        name = i[3]
        add = i[4]
        phone = i[5]
        owner = i[6]
        source = i[7]
        open = i[8]
        created = i[9]
        renewal = i[10]
        lat = i[11]
        git = i[12]

        
        fac_list.append(
            {
            "idx" : idx,
            "city" : city,
            "division" : div,
            "name" : name,
            "address" : add,
            "phone" : phone,
            "owner" : owner,
            "source" : source,
            "open" : open,
            "created" : created,
            "renewal" : renewal,
            "lat" : lat,
            "git" : git
            }
        ) 
    return {'fac_list':fac_list}

@app.route('/sign_up', methods=['POST'])
def regist():
    if request.method == "POST":
      id_receive = request.form['userid']
      name_receive = request.form['username']
      pw_receive = request.form['userpw']
      pw2_receive = request.form['userpw2']
      email_receive = request.form['useremail']
      address_receive = request.form['userad']
      birth_receive = request.form['userbirth']
      pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()  #sha256
    
    if id_receive == '' and name_receive =='' and pw_receive == '':
       flash("입력되지 않은 값이 있습니다.")
       return render_template('sign_up.html')
  
    if pw_receive != pw2_receive:
       flash("비밀번호가 일치하지 않습니다.")
       return render_template('sign_up.html')
    
    db.insert_data(id_receive,name_receive,pw_hash,email_receive,address_receive,birth_receive)

    flash("회원가입 성공하셨습니다")
    return render_template('sign_in.html')

@app.route('/sign_in', methods=['POST'])

def api_login():
    id_receive = request.form['userid']
    pw_receive = request.form['userpw']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.select_login(id_receive, pw_hash)

    if result:
        print(datetime.datetime.utcnow() + datetime.timedelta(hours=1))
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, app.secret_key, algorithm='HS256')  # .decode('utf-8') 이미 디코드 된거라 필요없어서 에러뜸
        # token을 줍니다.
        if token is not None:
            session['id'] = id_receive
            session['logged_in'] = True
            item = result[0][0]
            flash(f"{item} 님 로그인 성공하셨습니다")
            response = make_response(render_template('main.html',data=item))
            response.set_cookie('token',token)
            return response
        else:
            return render_template('sign_in.html')
        #return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        flash("아이디, 비밀번호가 잘못됐습니다.")
        return render_template('sign_in.html')


@app.route('/sign_out')
def logout():
    if session['logged_in'] == True:
        session['logged_in'] = False
        session.pop('id',None)
    response = make_response(render_template('main.html'))
    response.set_cookie('token', '', expires=0)
    return response


@app.route('/nick', methods=['POST'])
def api_valid():
    token_receive = request.cookies.get('token')
    #print(token_receive)
    try:

        payload = jwt.decode(token_receive, app.secret_key, algorithms=['HS256'])
        id = payload['id']

        userinfo = db.select_id_only(id)

        return jsonify({'result': 'success', 'id': userinfo})
    except jwt.ExpiredSignatureError:
        print('안도미....1')
        session['logged_in'] = False
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        print('안도미....2')
        session['logged_in'] = False
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
    
@app.route('/toggle-like', methods = ['POST'])
def like():
    try:
        data = request.get_json()  
        print(data)
        user_id = data.get('userId')[0][0]
        is_liked = data.get('isLiked')  # 만약 찬하트 -> 빈하트면 false, 빈하트->찬하트면 true가 들어있을 것이다
        fac_id = data.get('facId')
        print(user_id, fac_id,'이건가')
        if(is_liked == True):
            db.insert_like(user_id, fac_id) #삽입
        else:
            db.delete_like(user_id, fac_id) #삭제
        return jsonify({'result':'success'})
    except :
        return jsonify({'result':'fail'})

@app.route('/is-like', methods = ['POST'])
def likecheck():
    try:
        data = request.get_json()  
        print(data)
        user_id = data.get('userId')[0][0]
        fac_id = data.get('facId')
        result = db.select_like_count(user_id, fac_id)
        print(result)
        if result is not None:
            return jsonify({'result':'success'})
        else:
            return jsonify({'result':'fail'})
    except :
        return jsonify({'result':'fail'})


if __name__ == '__main__':
    app.debug = True 