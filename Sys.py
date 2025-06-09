import csv
import os
# from rich.console import Console

# 待实现的成绩可视化功能
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# pip install matplotlib

# 存储文件
FILE = "Class\\students.csv"  # csv格式方便统计归纳
INFO = ["学号", "姓名", "数学", "英语", "Python"]
USER_FILE = "Class\\users.csv"
USER_INFO = ["用户名", "密码", "类型"]


# 登录部分
def login_menu():
    print("\n=== 系统登录 ===")
    print("1. 用户登录")
    print("2. 管理员登录")
    print("3. 注册账户")


def load_users():
    users = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            users = list(reader)
    return users


def save_users(users):
    with open(USER_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=USER_INFO)
        writer.writeheader()
        writer.writerows(users)


def register():
    users = load_users()
    username = input("请输入用户名：").strip()
    if any(u["用户名"] == username for u in users):
        print("该用户已存在")
        return

    password = input("请输入密码：").strip()

    # 只能注册用户类型
    users.append({"用户名": username, "密码": password, "类型": "用户"})
    print("注册成功")
    save_users(users)


def login_user(type):
    users = load_users()
    username = input("请输入用户名: ").strip()
    password = input("请输入密码: ").strip()
    user = next(
        (u for u in users if u["用户名"] == username and u["密码"] == password), None
    )
    if user and user["类型"] == type:
        print(f"{'管理员' if type == '管理员' else '用户'}登陆成功")
        return True
    return False


def login():
    while True:
        login_menu()
        # console = Console()
        operation = input("请输入选项：").strip()
        # console.clear()
        if operation == "1":
            if login_user("用户"):
                return "用户"
        elif operation == "2":
            if login_user("管理员"):
                return "管理员"
        elif operation == "3":
            register()
        else:
            print("无效输入")


# 数据处理部分
# 读取学生信息
def load_data():
    students = []
    # 在students.csv文件中读取学生信息
    if os.path.exists(FILE):
        with open(FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            students = list(reader)
    return students


# 保存学生信息
def save_data(students):
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=INFO)  # 填入列名
        writer.writeheader()
        writer.writerows(students)


# 功能部分
# 添加学生信息
def add_student(students):
    student = {"学号": input("请输入学号: ").strip()}
    if any(s["学号"] == student["学号"] for s in students):
        print("该学号已存在！")
        return

    student["姓名"] = input("请输入姓名: ").strip()

    # 从数学开始读取成绩
    for subject in INFO[2:]:
        while True:
            try:
                student[subject] = float(input(f"请输入{subject}成绩: "))
                break
            except ValueError:
                print("请输入有效数字！")

    students.append(student)
    print("学生信息添加成功！")


# 查询学生信息
def query_student(students):
    ID = input("请输入查询学号: ").strip()
    found = None
    for student in students:
        if student["学号"] == ID:
            found = student
            break

    if not found:
        print("未找到该学生！")
        return

    print("\n".join([f"{k}: {v}" for k, v in found.items()]))


# 删除学生信息
def delete_student(students):
    ID = input("请输入删除学号: ").strip()
    for info, student in enumerate(students):
        if student["学号"] == ID:
            del students[info]
            print("删除成功！")
            return
    print("未找到该学生！")


# 打印学生信息
def show_student(students):
    for student in students:
        print(", ".join([f"{k}:{v}" for k, v in student.items()]))


# 功能部分
# 计算平均分
def calculate_average(students):
    if not students:
        print("暂无学生数据！")
        return

    # 将科目填入总分映射
    totals = {subject: 0.0 for subject in INFO[2:]}
    for student in students:
        for subject in INFO[2:]:
            totals[subject] += float(student[subject])

    print("各科平均分:")
    for subject, total in totals.items():
        print(f"{subject}: {total/len(students):.2f}")

    averages = {subject: total / len(students) for subject, total in totals.items()}
    return averages


def show_menu_admin():
    print("\n=== 学生成绩管理系统 ===")
    print("1. 添加学生信息")
    print("2. 查询学生信息")
    print("3. 删除学生信息")
    print("4. 显示所有信息")
    print("5. 统计平均分")
    print("0. 退出系统")


def show_menu_user():
    print("\n=== 学生成绩管理系统 ===")
    print("1. 查询学生信息")
    print("0. 退出系统")


def main():
    user_type = login()
    students = load_data()
    # console = Console()
    # console.clear()

    while True:
        if user_type == "用户":
            show_menu_user()
            operation = input("请输入选项: ").strip()
            console.clear()
            if operation == "1":
                query_student(students)
            elif operation == "0":
                save_data(students)
                print("数据已保存，系统退出！")
                break
            else:
                print("无效输入，请重新选择！")
        else:
            show_menu_admin()
            operation = input("请输入选项: ").strip()
            console.clear()

            if operation == "1":
                add_student(students)
            elif operation == "2":
                query_student(students)
            elif operation == "3":
                show_student(students)
                delete_student(students)
            elif operation == "4":
                show_student(students)
            elif operation == "5":
                calculate_average(students)
            elif operation == "0":
                save_data(students)
                print("数据已保存，系统退出！")
                break
            else:
                print("无效输入，请重新选择！")
        # 延长响应时间
        """try:
            time.sleep(5)
            
        except Exception:
            print("出现异常!")"""
        input("输入任意键返回主菜单")
        console.clear()


if __name__ == "__main__":
    main()
