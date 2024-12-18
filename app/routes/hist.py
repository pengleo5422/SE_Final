from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app.models.issue import Issue
from app.models.comment import Comment
from app.models.favorite import Favorite
from app.models.vote import Vote
from app import db
from datetime import datetime
hist_bp = Blueprint('hist', __name__)

@hist_bp.route('/history', methods=['GET'])
def history():
    user_id = current_user.userID

    posted_issues = Issue.get_posted_issues_by_user(user_id)
    commented_issues = Comment.get_commented_issues_by_user(user_id)
    favorited_issues = Favorite.get_favorited_issues_by_user(user_id)
    voted_issues = Vote.get_voted_issues_by_user(user_id)
    
    # 預設顯示全部互動過的議題
    all_issues = set(posted_issues + commented_issues + favorited_issues + voted_issues)

    issues_info = []
    for issue in all_issues:
        icons = []
        # 根據issue的status及是否為本人userID判定icon
        if issue.userID == user_id:
            if issue.status == 1:
                # 創建icon
                icons.append('<img src="https://img.icons8.com/?size=100&id=42862&format=png&color=000000">')

            elif issue.status == 0:
                # 暫存icon
                icons.append('<img src="https://img.icons8.com/?size=100&id=9_NQcM4E-KeP&format=png&color=000000">')

        if issue in commented_issues:
            icons.append('<img src="https://img.icons8.com/?size=100&id=WK5zjEkjX6HF&format=png&color=000000">')
        if issue in voted_issues:
            icons.append('<img src="https://img.icons8.com/?size=100&id=GiNJOdKO-eaC&format=png&color=000000">')
        if issue in favorited_issues:
            icons.append('<img src="https://img.icons8.com/?size=100&id=8ggStxqyboK5&format=png&color=000000">')

        preview_length = 50
        preview = issue.description[:preview_length] + '...' if len(issue.description) > preview_length else issue.description

        is_expired = issue.deadline and issue.deadline < datetime.utcnow()
        issues_info.append({
            'issueID': issue.issueID,
            'title': issue.title,
            'preview': preview,
            'icons': ' '.join(icons),
            'is_expired': is_expired,
            'status': issue.status
        })

    return render_template('history.html', issues=issues_info)


@hist_bp.route('/history/filter', methods=['GET'])
def history_filter():
    user_id = current_user.userID
    filter_type = request.args.get('filter', None)
    
    posted_issues = Issue.get_posted_issues_by_user(user_id)
    commented_issues = Comment.get_commented_issues_by_user(user_id)
    favorited_issues = Favorite.get_favorited_issues_by_user(user_id)
    voted_issues = Vote.get_voted_issues_by_user(user_id)

    # 新增tmp及created篩選條件
    if filter_type == 'tmp':
        # 選擇issue.status為0且userID等於user_id的議題
        target_issues = [issue for issue in posted_issues if issue.status == 0 and issue.userID == user_id]
    elif filter_type == 'created':
        # 選擇issue.status為1且userID等於user_id的議題
        target_issues = [issue for issue in posted_issues if issue.status == 1 and issue.userID == user_id]
    elif filter_type == 'commented':
        target_issues = commented_issues
    elif filter_type == 'favorited':
        target_issues = favorited_issues
    elif filter_type == 'voted':
        target_issues = voted_issues
    else:
        # 無篩選條件，顯示全部
        target_issues = set(posted_issues + commented_issues + favorited_issues + voted_issues)

    issues_data = []
    for issue in target_issues:
        icons = []
        # 根據issue的status及是否為本人userID判定icon
        if issue.userID == user_id:
            if issue.status == 1:
                # 創建icon
                icons.append('<img src="https://img.icons8.com/?size=100&id=42862&format=png&color=000000">')
            elif issue.status == 0:
                # 暫存icon
                icons.append('<img src="https://img.icons8.com/?size=100&id=9_NQcM4E-KeP&format=png&color=000000">')

        if issue in commented_issues:
            icons.append('<img src="https://img.icons8.com/?size=100&id=WK5zjEkjX6HF&format=png&color=000000">')
        if issue in voted_issues:
            icons.append('<img src="https://img.icons8.com/?size=100&id=GiNJOdKO-eaC&format=png&color=000000">')
        if issue in favorited_issues:
            icons.append('<img src="https://img.icons8.com/?size=100&id=8ggStxqyboK5&format=png&color=000000">')

        preview_length = 50
        preview = issue.description[:preview_length] + '...' if len(issue.description) > preview_length else issue.description
        
        is_expired = issue.deadline and issue.deadline < datetime.utcnow()

        issues_data.append({
            'issueID': issue.issueID,
            'title': issue.title,
            'preview': preview,
            'icons': icons,
            'is_expired': is_expired,
            'status': issue.status
        })

    return jsonify(issues_data)
