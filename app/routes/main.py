from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from app import db
from app.models.user import User
from app.models.issue import Issue
import logging
import os
from werkzeug.utils import secure_filename
# 設置日誌記錄
logging.basicConfig(level=logging.DEBUG)

login_manager = LoginManager()

def configure_routes(app):
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        # Return the user object for the given user_id
        return User.query.get(int(user_id))
    
    @app.route('/')
    def home():
        """首頁"""
        return render_template('login.html')

    @app.route('/index')
    def index():
        """首頁"""
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """註冊"""
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])
            idPhoto = ""
            profileData = ""
            idPhoto_filename = ""
            profileData_filename = ""
            authenticationStatus = False  # 'authenticationStatus' in request.form
            is_admin = False
            if email == 'admin@mail.com':
                is_admin = True
                authenticationStatus = True      

            else:
                # 儲存圖片檔案
                idPhoto = request.files['id_front']
                profileData = request.files['id_back']
                idPhoto_fname = secure_filename(idPhoto.filename)
                profileData_fname = secure_filename(profileData.filename)
                idPhoto.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], idPhoto_fname))
                profileData.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], profileData_fname))

            
            new_user = User(
                name=name,
                email=email,
                password=password,
                idPhoto=idPhoto_fname,
                authenticationStatus=authenticationStatus,
                profileData=profileData_fname,
                is_admin=is_admin
            )
            logging.error(f"錯誤")
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

    @app.route('/propose', methods=['GET', 'POST'])
    @login_required
    def propose():
        """新增問題"""
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

    @app.route('/member/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def member(user_id):
        """會員資料"""
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

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """登入"""
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('登入成功', 'success')
                if user.is_admin:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('index', user_id=user.userID))
            else:
                flash('帳號或密碼錯誤', 'danger')
                return render_template('login.html', error='帳號或密碼錯誤')
        
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        """登出"""
        logout_user()
        flash('您已登出', 'success')
        return redirect(url_for('login'))

    @app.route('/seconded', methods=['GET'])
    def seconded():
        """附議頁面"""
        return render_template('seconded.html')

    @app.route('/member/<int:user_id>/change_password', methods=['POST'])
    @login_required
    def change_password(user_id):
        """修改密碼"""
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

    @app.route('/member/<int:user_id>/update_profile', methods=['POST'])
    @login_required
    def update_profile(user_id):
        """更新使用者資料"""
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

    @app.route('/admin_dashboard')
    @login_required
    def admin_dashboard():
        """管理員儀表板"""
        return render_template('member_homepage.html')

    @app.route('/member_manage')
    @login_required
    def member_manage():
        """會員管理"""
        users = User.query.filter_by(is_admin=False).all()
        return render_template('member_manage.html', users=users)

    @app.route('/propose_manage')
    @login_required
    def propose_manage():
        """議題管理"""
        return render_template('propose_manage.html')

    @app.route('/propose_category_manage')
    @login_required
    def propose_category_manage():
        """議題類別管理"""
        return render_template('propose_category_manage.html')

    @app.route('/member_auth/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def member_auth(user_id):
        """會員審核"""
        user = User.query.get_or_404(user_id)
        
        if request.method == 'POST':
            user.authenticationStatus = 'authenticationStatus' in request.form
            
            try:
                db.session.commit()
                flash('會員認證狀態已更新', 'success')
            except Exception as e:
                db.session.rollback()
                logging.error(f"會員認證狀態更新失敗: {e}")
                flash('會員認證狀態更新失敗', 'danger')
            
            return redirect(url_for('member_manage'))
        
        return render_template('member_auth.html', user=user)

    @app.route('/approve/<int:user_id>', methods=['GET'])
    @login_required
    def approve(user_id):
        """審核會員"""
        user = User.query.get_or_404(user_id)
        user.authenticationStatus = True
        
        try:
            db.session.commit()
            flash('會員已審核通過', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f"會員審核失敗: {e}")
            flash('會員審核失敗', 'danger')
        
        return redirect(url_for('member_manage'))

    @app.route('/reject/<int:user_id>', methods=['GET'])
    @login_required
    def reject(user_id):
        """退件會員"""
        user = User.query.get_or_404(user_id)
        user.authenticationStatus = False
        
        try:
            db.session.commit()
            flash('會員已退件', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f"會員退件失敗: {e}")
            flash('會員退件失敗', 'danger')
        
        return redirect(url_for('member_manage'))