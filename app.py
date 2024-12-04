from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models.user import User
from app.models.issue import Issue
from app.models.notification import Notification
from app.forms.registration_form import IssueForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
from config import Config
import logging
from sqlalchemy import text
from app import create_app

app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 設置日誌記錄
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

# 註冊
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        #password = generate_password_hash(request.form['password'])
        password = request.form['password']
        #idPhoto = request.form['id_front_path']  # files
        authenticationStatus = False  # 'authenticationStatus' in request.form
        #profileData = request.form['id_back_path']  # files
        is_admin = False
        if email == 'admin@mail.com':
            is_admin = True
            authenticationStatus = True
        
        new_user = User(
            name=name,
            email=email,
            password=password,
            #idPhoto=idPhoto,
            authenticationStatus=authenticationStatus,
            #profileData=profileData,
            is_admin=is_admin
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('註冊成功', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"註冊失敗: {e}")
            flash('註冊失敗', 'danger')
    
    return render_template('register.html')

# 新增問題
@app.route('/propose', methods=['GET', 'POST'])
@login_required
def propose():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_issue = Issue(
            title=title,
            description=description,
            user_id=current_user.userID
        )
        
        try:
            db.session.add(new_issue)
            db.session.commit()
            flash('問題已新增', 'success')
            return redirect(url_for('home'))
        except:
            db.session.rollback()
            flash('新增問題失敗', 'danger')
    
    return render_template('propose.html')

#會員
@app.route('/member/<int:user_id>', methods=['GET', 'POST'])
@login_required
def member(user_id):
    if current_user.userID != user_id:
        flash('您無權訪問此頁面', 'danger')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        user.idPhoto = request.form['idPhoto']
        user.authenticationStatus = 'authenticationStatus' in request.form
        user.profileData = request.form['profileData']
        
        try:
            db.session.commit()
            flash('資料已更新', 'success')
        except:
            db.session.rollback()
            flash('更新失敗', 'danger')

        return redirect(url_for('member', user_id=user.userID))
    
    return render_template('member.html', user=user)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#登入
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.password==password: #check_password_hash(user.password, password)
            login_user(user)
            flash('登入成功', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('member', user_id=user.userID))
        else:
            flash('帳號或密碼錯誤', 'danger')
            return render_template('login.html', error='帳號或密碼錯誤')
    
    return render_template('login.html')

'''
@app.route('/api/proposals/latest', methods=['GET'])
def get_latest_proposals():
    proposals = Proposal.query.order_by(Proposal.date.desc()).limit(10).all()
    return jsonify([proposal.to_dict() for proposal in proposals])

@app.route('/api/proposals/popular', methods=['GET'])
def get_popular_proposals():
    proposals = Proposal.query.order_by(Proposal.support_count.desc()).limit(10).all()
    return jsonify([proposal.to_dict() for proposal in proposals])

@app.route('/api/proposals/completed', methods=['GET'])
def get_completed_proposals():
    proposals = Proposal.query.filter_by(status='completed').order_by(Proposal.date.desc()).limit(10).all()
    return jsonify([proposal.to_dict() for proposal in proposals])
'''

#登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已登出', 'success')
    return redirect(url_for('login'))

@app.route('/seconded', methods=['GET'])
def seconded():
    return render_template('seconded.html')

#修改密碼
@app.route('/member/<int:user_id>/change_password', methods=['POST'])
@login_required
def change_password(user_id):
    if current_user.userID != user_id:
        flash('您無權修改此使用者的密碼', 'danger')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    new_password = request.form['new_password']
    user.password = generate_password_hash(new_password)
    
    try:
        db.session.commit()
        flash('密碼已更新', 'success')
    except:
        db.session.rollback()
        flash('密碼更新失敗', 'danger')
    
    return redirect(url_for('member', user_id=user.userID))

#使用者資料更新
@app.route('/member/<int:user_id>/update_profile', methods=['POST'])
@login_required
def update_profile(user_id):
    if current_user.userID != user_id:
        flash('您無權修改此使用者的資料', 'danger')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    user.name = request.form['name']
    user.email = request.form['email']
    user.idPhoto = request.form['idPhoto']
    user.authenticationStatus = 'authenticationStatus' in request.form
    user.profileData = request.form['profileData']
    
    try:
        db.session.commit()
        flash('資料已更新', 'success')
    except:
        db.session.rollback()
        flash('資料更新失敗', 'danger')
    
    return redirect(url_for('member', user_id=user.userID))

#---------------------------------------------------
#admin_dashboard
@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('member_homepage.html')

@app.route('/member_manage')
@login_required
def member_manage():
    # 獲取所有會員資料
    users = User.query.filter_by(is_admin=False).all()
    return render_template('member_manage.html', users=users)

@app.route('/propose_manage')
@login_required
def propose_manage():
    return render_template('propose_manage.html')

@app.route('/propose_category_manage')
@login_required
def propose_category_manage():
    return render_template('propose_category_manage.html')

@app.route('/maintenance_notice', methods=['GET', 'POST'])
@login_required
def maintenance_notice():
    if request.method == 'POST':
        content = request.form['content']
        new_notice = Notification(
            userID=current_user.userID,
            notificationTime=datetime.now(),
            content=content
        )
        
        try:
            db.session.add(new_notice)
            db.session.commit()
            flash('公告已發布', 'success')
        except:
            db.session.rollback()
            flash('公告發布失敗', 'danger')
    
    notices = Notification.query.order_by(Notification.notificationTime.desc()).all()
    return render_template('maintenance_notice.html', notices=notices)


if __name__ == '__main__':
    with app.app_context():
        # 檢查資料庫連接
        try:
            db.session.execute(text('SELECT 1'))
            logging.info("資料庫連接成功")
        except Exception as e:
            logging.error(f"資料庫連接失敗: {e}")

        db.create_all()  # Create tables
    app.run(debug=True)