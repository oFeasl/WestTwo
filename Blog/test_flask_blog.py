from flask import Flask,redirect,session,request,url_for,render_template
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from werkzeug.wrappers import UserAgentMixin


app=Flask(__name__)
app.secret_key = 'dsaqwesa.,.sad213532szcz[]dsa1213sda,/'
prefix = 'sqlite:///'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'user_data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'user_data.db'))
db=SQLAlchemy(app=app)
UPLOAD_PATH=os.path.join(os.path.dirname(__file__), 'static/video')
AVATAR_PATH=os.path.join(os.path.dirname(__file__), 'static/avatars')
class User_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    password = db.Column(db.String)
    avatar_path = db.Column(db.String)
    self_intro = db.Column(db.String)
    doc_num = db.Column(db.Integer)
    video_num = db.Column(db.Integer)

class Doc_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    md = db.Column(db.Text)
    like = db.Column(db.Integer)
    author = db.Column(db.Integer)

class comment_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forwhich = db.Column(db.Integer)
    body = db.Column(db.String)
    author = db.Column(db.String)

class Video_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    like = db.Column(db.Integer)
    author = db.Column(db.Integer)
    video = db.Column(db.String)


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    doc_id = db.Column(db.Integer)

class Vital_Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usr = db.Column(db.Integer)
    doc = db.Column(db.Integer)
    video = db.Column(db.Integer)

# welcome page
@app.route('/',methods=["GET"])
def hello():
    return render_template("hello_page.html")


# registe page
@app.route('/registered',methods=["GET","POST"])
def registered():
    if(request.method=="POST"):
        note=User_List(user=request.form["username"],password=request.form["password"],avatar_path="default.jpg",self_intro="Null",doc_num=0,video_num=0)
        db.session.add(note)
        Vital_Info.query.get(1).usr+=1
        db.session.commit()
        return redirect('/')
    return render_template("registered_page.html")


# login page
@app.route('/login',methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        try:
            judge=(User_List.query.filter_by(user=request.form['username']).first().password==request.form['password'])
        except:
            return render_template("login_failed_page.html")
        if(judge==False):
            return render_template("login_failed_page.html")
        else:
            session['username']=request.form['username'] # identity authentication
            session['id']=User_List.query.filter_by(user=request.form['username']).first().id # 获得登录者在数据库中的次序
            return redirect(url_for('Main'))
    else:
        return render_template("login_page.html")


# personal page
@app.route('/personal',methods=["GET","POST"])
def personal():
    username=session['username']
    intro=User_List.query.get(session['id']).self_intro
    avatar_path=User_List.query.get(session['id']).avatar_path
    if(request.method=="GET"):
        return render_template("personal_page.html",username=username,intro=intro,avatar_path=avatar_path)
    else:
        session['username']=request.form['username']
        username=request.form['username']
        intro=request.form['intro']
        avatar=request.files.get('avatar')
        avatar.save(os.path.join(AVATAR_PATH,secure_filename(avatar.filename)))
        
        User_List.query.get(session['id']).user=request.form['username']
        User_List.query.get(session['id']).self_intro=request.form['intro']
        User_List.query.get(session['id']).avatar_path=avatar.filename
        db.session.commit()
        return render_template("personal_page.html",username=username,intro=intro,avatar_path=avatar.filename)
    

# logout page
@app.route('/logout',methods=["GET"])
def logout():
    del session['username']
    del session['id']
    return redirect(url_for('login'))


# change password
@app.route('/change',methods=["GET","POST"])
def change():
    username=session['username']
    userid=session['id']
    old_password=User_List.query.get(userid).password
    if(request.method=="POST"):
        if(request.form['old_password']==old_password):
            User_List.query.get(userid).password=request.form['new_password']
            db.session.commit()
        else:
            return render_template("change_password_error_page1.html",username=username)
        return redirect('Main')
    else:
        return render_template("change_password_page1.html",username=username)


# main page after login
@app.route('/Main',methods=["GET"])
def Main():
    try:#identity authentication first
        usn = session['username']
        return render_template("main_page.html",username=usn)
    except:#identity authentication failed
        return render_template('without_login_page.html')


# blog page
@app.route('/blog',methods=["GET","POST"])
def blog():
    if request.method=="GET":
        try:#identity authentication first
            usn = session['username']
            return render_template("blog_page.html",username=usn)
        except:#identity authentication failed
            return render_template('without_login_page.html')
    else:
        note = Doc_list(md=request.form['text'] ,title=request.form['Title'],like=0,author=session['id']) # 存入数据库
        db.session.add(note)
        Vital_Info.query.get(1).doc+=1
        User_List.query.get(session['id']).doc_num+=1
        db.session.commit()
        return redirect('Main')


# upload video page
@app.route('/video',methods=["GET","POST"])
def video():
    if request.method=="GET":
        try:#identity authentication first
            usn = session['username']
            return render_template("upload_video_page.html",username=usn)
        except:#identity authentication failed
            return render_template('without_login_page.html')
    else:
        video_file=request.files.get('file')
        video_file.save(os.path.join(UPLOAD_PATH,secure_filename(video_file.filename)))
        note = Video_list(video=video_file.filename,title=request.form.get('title'),like=0,author=session['id']) # 存入数据库
        db.session.add(note)
        Vital_Info.query.get(1).video+=1
        User_List.query.get(session['id']).video_num+=1
        db.session.commit()
        flash("Upload success!")
        return redirect('Main')


# view whole Video
@app.route('/view_video',methods=["GET"])
def view_video():
    blog=[]
    i=1
    while(1):
        try:
            video=Video_list.query.get(i)
            blog.append(video.title)
            i=i+1
        except:
            break
    return render_template("view_video_page.html",blog=blog)


# view whole Doc
@app.route('/view',methods=["GET","POST"])
def view():
    blog=[]
    blog_id=[]
    i=1
    try:
        temp_list=Doc_list.query.all()
        Max=temp_list[len(temp_list)-1].id
    except:
        Max=Vital_Info.query.get(1).doc
    for i in range(1,Max+2):
        try:
            doc=Doc_list.query.get(i)
            blog.append(doc.title)
            blog_id.append(doc.id)
            i=i+1
        except:
            pass

    return render_template("view_page.html",blog=blog,blog_id=blog_id)

# view my Doc
@app.route('/mywork',methods=["GET"])
def mywork():
    blog=[]
    blog_id=[]
    i=1
    try:
        temp_list=Doc_list.query.all()
        Max=temp_list[len(temp_list)-1].id
    except:
        Max=Vital_Info.query.get(1).doc
    for i in range(1,Max+2):
        try:
            if Doc_list.query.get(i).author==session['id']:
                doc=Doc_list.query.get(i)
                blog.append(doc.title)
                blog_id.append(doc.id)
            i=i+1
        except:
            pass
    return render_template("my_work_page.html",blog=blog,blog_id=blog_id)


# del doc page
@app.route('/del_doc/<int:doc_id>',methods=["POST"])
def Del_Doc(doc_id):
    doc=Doc_list.query.get(doc_id)
    try:
        doc2=Collection.query.filter_by(doc_id=doc_id).first()
        db.session.delete(doc2)
    except:
        pass
    db.session.delete(doc)
    db.session.commit()
    return redirect('/mywork')


# edit page
@app.route('/edit/<int:id>',methods=["GET","POST"])
def edit(id):
    if(request.method=="GET"):
        text=Doc_list.query.get(id)
        return render_template("edit_page.html",title=text.title,body=text.md,username=session['username'],blogid=id)
    else:
        Doc_list.query.get(id).title=request.form['Title']
        Doc_list.query.get(id).md=request.form['text']
        db.session.commit()
        return redirect(url_for('Main'))


# browse page
@app.route('/browse/<int:id>')
def browse(id):
    body=Doc_list.query.get(id).md
    title=Doc_list.query.get(id).title
    likenum=Doc_list.query.get(id).like
    all_coment=comment_list.query.all()
    comenter=[]
    this_coment=[]
    for i in all_coment:
        if i.forwhich==id:
            this_coment.append(i.body)
            comenter.append(i.author)
    return render_template('browse_page.html',id=id,body=body,title=title,username=session['username'],likenum=likenum,comments=this_coment,commenter=comenter)


# browse video page
@app.route('/browse_video/<int:id>')
def browse_video(id):
    video_name=Video_list.query.get(id).video
    return render_template("video_page.html",video_name=video_name,video_id=id)


# like
@app.route('/like/<int:doc_id>',methods=["POST"])
def like(doc_id):
    Doc_list.query.get(doc_id).like+=1
    db.session.commit()
    return redirect(url_for('browse',id=doc_id))


# comment
@app.route('/coment/<int:doc_id>',methods=["POST"])
def coment(doc_id):
    forwhich=doc_id
    body=request.form['coment']
    coment=comment_list(forwhich=forwhich,body=body,author=session['username'])
    db.session.add(coment)
    db.session.commit()
    return redirect(url_for('browse',id=doc_id))

# collect
@app.route('/collect/<int:doc_id>',methods=["POST"])
def collect(doc_id):
    collect=Collection(author_id=session['id'],doc_id=doc_id)
    db.session.add(collect)
    db.session.commit()
    return redirect(url_for('browse',id=doc_id))


# view_collection
@app.route('/view_Collection')
def view_coll():
    all_collection=Collection.query.all()
    blog=[]
    blog_id=[]
    print(all_collection)
    for i in all_collection:
        if(i.author_id==session['id']):
            blog.append(Doc_list.query.get(i.doc_id).title)
            blog_id.append(i.doc_id)
    return render_template('collection_page.html',blog=blog,blog_id=blog_id)



if __name__=="__main__":
    try:
        db.create_all()
        if Vital_Info.query.get(1):
            pass
        else:
            info=Vital_Info(usr=0,doc=0,video=0)
            db.session.add(info)
            db.session.commit()
    except:
        pass
    app.run(debug=1)
    # app.run(host="0.0.0.0",port=5000)
    
