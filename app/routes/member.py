from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, LoginManager
from app import db
from app.models.user import User

member_bp = Blueprint('member', __name__)

@member_bp.route('/member/<int:user_id>', methods=['GET', 'POST'])
@login_required
def member(user_id):
        """會員資料"""
        if current_user.userID != user_id:
            flash('您無權訪問此頁面', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.get_or_404(user_id)
        
        return render_template('usrProfile.html', user=user)

@member_bp.route('/member/<int:user_id>/change_password', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    """修改密碼"""
    if current_user.userID != user_id:
        flash('您無權修改此使用者的密碼', 'd')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    old_password = request.form['old-password']
    new_password = request.form['new-password']
    confirm_password = request.form['confirm-password']
    
    # 檢查舊密碼是否正確
    if not check_password_hash(user.password, old_password):
        flash('舊密碼不正確', 'd')
        return redirect(url_for('member.editpwd', user_id=user_id))
        
    user.password = generate_password_hash(new_password)
    
    try:
        db.session.commit()
        flash('密碼已更新', 'd')
    except Exception as e:
        db.session.rollback()
        flash('密碼更新失敗', 'd')
    
    return redirect(url_for('member.editpwd', user_id=user.userID))

@member_bp.route('/member/<int:user_id>/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
        """更新使用者資料"""
        if current_user.userID != user_id:
            flash('您無權修改此使用者的資料', 'p')
            return redirect(url_for('login'))
        
        user = User.query.get_or_404(user_id)
        user.name = request.form['name']
        new_email = request.form['email']

        # 檢查電子郵件是否已經存在
        if User.query.filter_by(email=new_email).first():
            flash('該電子郵件已經被使用', 'p')
            return redirect(url_for('member.memberedit', user_id=user.userID))
        
        user.email = new_email
        
        try:
            db.session.commit()
            flash('資料已更新', 'p')
        except:
            db.session.rollback()
            flash('資料更新失敗', 'p')
        
        return redirect(url_for('member.memberedit', user_id=user.userID))

@member_bp.route('/member/<int:user_id>/editpwd', methods=['GET', 'POST'])
@login_required
def editpwd(user_id):
        if current_user.userID != user_id:
            flash('您無權訪問此頁面', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.get_or_404(user_id)

        return render_template('editPWD.html', user=user)

@member_bp.route('/member/<int:user_id>/memberedit', methods=['GET', 'POST'])
@login_required
def memberedit(user_id):
        if current_user.userID != user_id:
            flash('您無權訪問此頁面', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.get_or_404(user_id)    
        
        return render_template('memberedit.html', user=user)