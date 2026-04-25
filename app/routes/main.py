from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示所有開放中的活動列表。
    GET: 呼叫 ActivityModel.get_all() 並渲染 index.html
    """
    pass

@main_bp.route('/activities/<int:activity_id>')
def activity_detail(activity_id):
    """
    顯示單一活動的詳細資訊與報名表單。
    GET: 呼叫 ActivityModel.get_by_id(activity_id) 並渲染 activity.html
    """
    pass

@main_bp.route('/activities/<int:activity_id>/register', methods=['POST'])
def register_activity(activity_id):
    """
    接收學生送出的報名表單。
    POST: 驗證名額是否已滿，未滿則呼叫 RegistrationModel.create() 並重導向至 success 頁面。
    若額滿則重導向回活動頁並顯示錯誤訊息。
    """
    pass

@main_bp.route('/activities/<int:activity_id>/success')
def register_success(activity_id):
    """
    顯示報名成功訊息畫面。
    GET: 渲染 success.html
    """
    pass
