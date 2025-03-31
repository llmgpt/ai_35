"""
计算GPA
"""
# 课程数据（学分，成绩）
courses = [
    {"credit": 4, "score": 73},  # 英语
    {"credit": 1, "score": 81},  # 工程伦理
    {"credit": 2, "score": 66},  # 中国特色社会主义理论与实践研究
    {"credit": 1, "score": 83},  # 自然辩证法概论
    {"credit": 3, "score": 72},  # 机器学习
    {"credit": 3, "score": 73},  # 软件体系结构
    {"credit": 3, "score": 78},  # 算法设计与分析
    {"credit": 3, "score": 60},  # 数理统计与数据分析
    {"credit": 3, "score": 70},  # 矩阵论
    {"credit": 1, "score": 65},  # 计算机技术实践
    {"credit": 2, "score": 86},  # 数字图像处理
    {"credit": 2, "score": 86},  # 高级计算机网络
    {"credit": 1, "score": 83},  # 论文写作指导
    {"credit": 6, "score": 65.6},  # 专业实践
]


def score_to_gpa(score):
    """将百分制成绩转换为4分制绩点"""
    if score >= 90:
        return 4.0
    elif 85 <= score < 90:
        return 3.7
    elif 80 <= score < 85:
        return 3.3
    elif 75 <= score < 80:
        return 3.0
    elif 70 <= score < 75:
        return 2.7
    elif 65 <= score < 70:
        return 2.3
    elif 60 <= score < 65:
        return 2.0
    else:
        return 0.0


total_credits = 0
total_weighted_gpa = 0.0

for course in courses:
    credit = course["credit"]
    score = course["score"]
    gpa = score_to_gpa(score)

    total_credits += credit
    total_weighted_gpa += credit * gpa

gpa_result = total_weighted_gpa / total_credits

print(f"总学分: {total_credits}")
print(f"GPA: {gpa_result:.2f}")