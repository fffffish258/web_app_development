from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    管理者登入頁面與處理。
    GET: 渲染 admin/login.html
    POST: 驗證帳號密碼，成功則寫入 session 並重導向至 /admin/
    """
    pass

@admin_bp.route('/logout')
def logout():
    """
    管理者登出處理。
    GET: 清除 session，重導向至 /admin/login
    """
    pass

@admin_bp.route('/')
def dashboard():
    """
    後台首頁，顯示所有活動管理清單。
    GET: 呼叫 ActivityModel.get_all() 並渲染 admin/dashboard.html
    """
    pass

@admin_bp.route('/activities/new', methods=['GET', 'POST'])
def new_activity():
    """
    建立新活動頁面與處理。
    GET: 渲染 admin/activity_form.html
    POST: 呼叫 ActivityModel.create()，成功後重導向至 /admin/
    """
    pass

@admin_bp.route('/activities/<int:activity_id>/edit', methods=['GET', 'POST'])
def edit_activity(activity_id):
    """
    編輯現有活動頁面與處理。
    GET: 取得活動資料並渲染 admin/activity_form.html
    POST: 呼叫 ActivityModel.update()，成功後重導向至 /admin/
    """
    pass

@admin_bp.route('/activities/<int:activity_id>/delete', methods=['POST'])
def delete_activity(activity_id):
    """
    刪除活動處理。
    POST: 呼叫 ActivityModel.delete()，成功後重導向至 /admin/
    """
    pass

@admin_bp.route('/activities/<int:activity_id>/participants')
def participants(activity_id):
    """
    檢視特定活動的報名名單。
    GET: 呼叫 RegistrationModel.get_by_activity_id(activity_id) 並渲染 admin/participants.html
    """
    pass
