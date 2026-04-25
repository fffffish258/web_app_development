from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.models import ActivityModel, RegistrationModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示所有開放中的活動列表。
    """
    activities = ActivityModel.get_all()
    return render_template('index.html', activities=activities)

@main_bp.route('/activities/<int:activity_id>')
def activity_detail(activity_id):
    """
    顯示單一活動的詳細資訊與報名表單。
    """
    activity = ActivityModel.get_by_id(activity_id)
    if not activity:
        flash("找不到該活動", "error")
        return redirect(url_for('main.index'))
    
    current_count = RegistrationModel.count_by_activity_id(activity_id)
    return render_template('activity.html', activity=activity, current_count=current_count)

@main_bp.route('/activities/<int:activity_id>/register', methods=['POST'])
def register_activity(activity_id):
    """
    接收學生送出的報名表單。
    """
    activity = ActivityModel.get_by_id(activity_id)
    if not activity:
        flash("找不到該活動", "error")
        return redirect(url_for('main.index'))

    if activity['is_full']:
        flash("報名失敗，名額已滿", "error")
        return redirect(url_for('main.activity_detail', activity_id=activity_id))

    # 取得表單資料
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # 基本輸入驗證
    if not name or not student_id or not email or not phone:
        flash("請填寫所有必填欄位", "error")
        return redirect(url_for('main.activity_detail', activity_id=activity_id))

    # 再次檢查報名人數，防止超額
    current_count = RegistrationModel.count_by_activity_id(activity_id)
    if current_count >= activity['capacity']:
        ActivityModel.update_full_status(activity_id, 1)
        flash("報名失敗，名額剛好滿了", "error")
        return redirect(url_for('main.activity_detail', activity_id=activity_id))

    data = {
        'activity_id': activity_id,
        'name': name,
        'student_id': student_id,
        'email': email,
        'phone': phone
    }

    # 寫入資料庫
    reg_id = RegistrationModel.create(data)
    if reg_id:
        # 檢查報名後是否達上限，若達到則更新活動狀態為已滿
        new_count = current_count + 1
        if new_count >= activity['capacity']:
            ActivityModel.update_full_status(activity_id, 1)
        
        return redirect(url_for('main.register_success', activity_id=activity_id))
    else:
        flash("系統錯誤，報名失敗", "error")
        return redirect(url_for('main.activity_detail', activity_id=activity_id))


@main_bp.route('/activities/<int:activity_id>/success')
def register_success(activity_id):
    """
    顯示報名成功訊息畫面。
    """
    activity = ActivityModel.get_by_id(activity_id)
    if not activity:
        return redirect(url_for('main.index'))
    return render_template('success.html', activity=activity)
