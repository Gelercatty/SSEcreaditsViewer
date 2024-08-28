from bs4 import BeautifulSoup

def parse_grades(html_path):
    # 读取HTML文件
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')

    # 查找包含成绩信息的表格
    table = soup.find('table', class_='table table-head-fixed table-hover')
    rows = table.find_all('tr')[1:]  # 排除表头

    # 解析每一行，提取成绩信息
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 9:  # 确保是完整的行
            record = {
                'index': cols[0].text.strip(),
                'academic_year': cols[1].text.strip(),
                'semester': cols[2].text.strip(),
                'course_code': cols[3].text.strip(),
                'course_name': cols[4].text.strip(),
                'course_nature': cols[5].text.strip(),
                'credits': cols[6].text.strip(),
                'class_hours': cols[7].text.strip(),
                'grade': cols[8].text.strip()
            }
            data.append(record)

    return data

def parse_personal_info(html_path):
    # 读取HTML文件
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')

    # 定位到包含个人信息的区域
    personal_info_div = soup.find('div', class_='card-body').find('div', class_='col-sm-10')
    info_rows = personal_info_div.find_all('p', class_='text-muted text-sm')

    # 提取信息
    personal_info = {}
    labels = ['学号', '身份证号', '学院', '层次', '性别', '政治面貌', '专业', '学制', '学籍状态', '年级', '班级', '入学日期']
    for row in info_rows:
        text = row.get_text(strip=True)
        for label in labels:
            if label in text:
                personal_info[label] = text.split('：')[-1].strip()
    #删掉身份证，
    personal_info.pop('身份证号')
    return personal_info
class person():

    target_optional_public_all = 13
    target_optional_public_online = 9
    sumerize_res = {}

    def __init__(self,html_path) -> None:
        self.personal_info = parse_personal_info(html_path)
        self.greades = parse_grades(html_path)

        if(self.personal_info['专业'] == '智能体育工程'):
            self.target_optional = 16
        else:
            self.target_optional = 18

    def sumerize(self):
        got_needed = 0
        num_needed = 0
        got_optional = 0
        num_optional = 0
        got_public = 0
        num_public = 0
        got_public_online = 0
        num_public_online = 0
        public_id = []
        public_online_id = []
        four_history = {
            "中国近现代史纲要": 0,

        }
        country_security = {
            "大学生国家安全教育（在线）" : 0,
        }
        
        labors = 0


        for grade in self.greades:
            if(grade['course_nature'] == '必修'):
                got_needed += float(grade['credits'])
                num_needed += 1
            elif(grade['course_nature'] == '选修'):
                got_optional += float(grade['credits'])
                num_optional += 1
            elif(grade['course_nature'] == '公选'):
                #看看名字里面有没有带（在线）
                if("（在线）" in grade['course_name']):
                    got_public_online += float(grade['credits'])
                    num_public_online += 1
                    public_online_id.append(grade['index'])
                else:
                    got_public += float(grade['credits'])
                    num_public += 1
                    public_id.append(grade['index'])

                if(grade['course_name'] in four_history):
                    four_history[grade['course_name']] = 1

                if(grade['course_name'] in country_security):
                    country_security[grade['course_name']] = 1

                if("劳动" in grade['course_name'] ):
                    labors += 1
        self.sumerize_res = {
            "got_needed": got_needed,
            "num_needed": num_needed,
            "got_optional": got_optional,
            "num_optional": num_optional,
            "got_public": got_public,
            "num_public": num_public,
            "got_public_online": got_public_online,
            "num_public_online": num_public_online,
            "public_id": public_id,
            "public_online_id": public_online_id,
            "four_history": four_history,
            "country_security": country_security,
            "labors": labors,
        }
        return
                

if __name__ == "__main__":
    #test class
    p = person(r"E:\aconnda\PROJ\Django\SSEclassScore\可信电子成绩单服务平台.html")
    p.sumerize()
    print(p.sumerize_res)