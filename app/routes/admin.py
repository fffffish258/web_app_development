from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.models import ActivityModel, RegistrationModel, AdminModel
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 登入驗證裝飾器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash("請先登入", "warning")
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    管理者登入頁面與處理。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = AdminModel.get_by_username(username)
        # MVP 階段暫時使用明碼或簡單比對。實務上應該要使用 werkzeug.security.check_password_hash
        if admin and admin['password_hash'] == password: 
            session['admin_logged_in'] = True
            session['admin_username'] = admin['username']
            flash("登入成功", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            flash("帳號或密碼錯誤", "error")
            
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """
    管理者登出處理。
    """
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash("已成功登出", "success")
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def dashboard():
    """
    後台首頁，顯示所有活動管理清單。
    """
    activities = ActivityModel.get_all()
    # 我們需要計算每個活動的報名人數來顯示
    activities_with_counts = []
    for act in activities:
        act_dict = dict(act)
        act_dict['current_count'] = RegistrationModel.count_by_activity_id(act['id'])
        activities_with_counts.append(act_dict)
        
    return render_template('admin/dashboard.html', activities=activities_with_counts)

@admin_bp.route('/activities/new', methods=['GET', 'POST'])
@login_required
def new_activity():
    """
    建立新活動頁面與處理。
    """
    if request.method == 'POST':
        data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'event_time': request.form.get('event_time'),
            'location': request.form.get('location'),
            'capacity': request.form.get('capacity')
        }
        
        if not data['title'] or not data['event_time'] or not data['location'] or not data['capacity']:
            flash("請填寫所有必填欄位", "error")
            return render_template('admin/activity_form.html', activity=data, action="new")
            
        activity_id = ActivityModel.create(data)
        if activity_id:
            flash("活動建立成功", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            flash("活動建立失敗", "error")
            
    return render_template('admin/activity_form.html', activity=None, action="new")

@admin_bp.route('/activities/<int:activity_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_activity(activity_id):
    """
    編輯現有活動頁面與處理。
    """
    activity = ActivityModel.get_by_id(activity_id)
    if not activity:
        flash("找不到該活動", "error")
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'event_time': request.form.get('event_time'),
            'location': request.form.get('location'),
            'capacity': request.form.get('capacity'),
            'is_full': 1 if request.form.get('is_full') == 'on' else 0
        }
        
        if not data['title'] or not data['event_time'] or not data['location'] or not data['capacity']:
            flash("請填寫所有必填欄位", "error")
            # 組合一下原本的 id 讓畫面不報錯
            data['id'] = activity_id
            return render_template('admin/activity_form.html', activity=data, action="edit")
            
        success = ActivityModel.update(activity_id, data)
        if success:
            flash("活動更新成功", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            flash("活動更新失敗", "error")

    return render_template('admin/activity_form.html', activity=activity, action="edit")

@admin_bp.route('/activities/<int:activity_id>/delete', methods=['POST'])
@login_required
def delete_activity(activity_id):
    """
    刪除活動處理。
    """
    success = ActivityModel.delete(activity_id)
    if success:
        flash("活動已刪除", "success")
    else:
        flash("活動刪除失敗", "error")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/activities/<int:activity_id>/participants')
@login_required
def participants(activity_id):
    """
    檢視特定活動的報名名單。
    """
    activity = ActivityModel.get_by_id(activity_id)
    if not activity:
        flash("找不到該活動", "error")
        return redirect(url_for('admin.dashboard'))
        
    participants = RegistrationModel.get_by_activity_id(activity_id)
    return render_template('admin/participants.html', activity=activity, participants=participants)
