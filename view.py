from flask import Flask, render_template, request, redirect, url_for, flash
from utools import person  # Import your class from the module where it's defined
from werkzeug.utils import secure_filename
import time
import os
app = Flask(__name__)
UPLOAD_FOLDER = './uploaded/files'
app.secret_key = os.urandom(16)
ALLOWED_EXTENSIONS = {'html'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有文件部分')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            timestamp = int(time.time())
            session_id = request.cookies.get('session') or 'default'


            filename = secure_filename(f'{session_id}_{timestamp}_{file.filename}')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # 使用 person 类处理文件并获取结果
            return redirect(url_for('viewer', path=filename))
        

    else:
        return '''
        <!doctype html>
        <title>上传新的成绩单</title>
        <h1>上传新的成绩单</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=上传>
        </form>
        '''

# @app.route('/viewer')
# def index():
#     # Create an instance of the 'person' class with the path to your HTML file
#     student = person(r"E:\aconnda\PROJ\Django\SSEclassScore\可信电子成绩单服务平台.html")
#     student.sumerize()

#     public_online_detail = []
#     public_detail = []
#     for id in student.sumerize_res['public_id']:
    
#         #prase the class name and credits for return
#         public_detail.append(
#             {'name':student.greades[int(id)-1]['course_name'],
#              'credits':student.greades[int(id)-1]['credits']})
#     for id in student.sumerize_res['public_online_id']:
#         #prase the class name and credits for return
#         public_online_detail.append(
#             {'name':student.greades[int(id)-1]['course_name'],
#              'credits':student.greades[int(id)-1]['credits']})
#     # Pass the summarized data to the HTML template



#     return render_template('viewer.html', data=student.sumerize_res, personal_info=student.personal_info
#                            ,target_optional=student.target_optional,target_optional_public_all=student.target_optional_public_all,
#                            target_optional_public_online=student.target_optional_public_online,
#                            public_detail=public_detail,public_online_detail=public_online_detail)

@app.route('/viewer')
def viewer():
    filename = request.args.get('path')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    student = person(file_path)
    student.sumerize()

    public_online_detail = []
    public_detail = []
    for id in student.sumerize_res['public_id']:
        public_detail.append({
            'name': student.greades[int(id)-1]['course_name'],
            'credits': student.greades[int(id)-1]['credits']
        })
    for id in student.sumerize_res['public_online_id']:
        public_online_detail.append({
            'name': student.greades[int(id)-1]['course_name'],
            'credits': student.greades[int(id)-1]['credits']
        })

    return render_template('viewer.html', data=student.sumerize_res, personal_info=student.personal_info,
                           target_optional=student.target_optional, target_optional_public_all=student.target_optional_public_all,
                           target_optional_public_online=student.target_optional_public_online,
                           public_detail=public_detail, public_online_detail=public_online_detail,
                           file_path=file_path)

@app.route('/cleanup', methods=['POST'])
def cleanup():
    filepath = request.form.get('filepath')
    print(filepath)
    if filepath:
        try:
            # os.remove(filepath)  # 尝试删除文件
            # # 可以加入更多的清理逻辑，比如数据库记录更新等
            # print(f'已删除文件 {filepath}')
            for file in os.listdir(UPLOAD_FOLDER):
                os.remove(os.path.join(UPLOAD_FOLDER, file))
        except FileNotFoundError:
            print("failed")  # 文件已经被删除或不存在
    else:
        print("failed1")
    return '', 204  # 返回一个空的响应


if __name__ == '__main__':
    app.run(debug=True)
