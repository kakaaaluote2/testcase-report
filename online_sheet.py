import os

import gspread

import pandas as pd
import requests

import pytz
import xlrd

cur_path = os.path.abspath(os.path.dirname(__file__))
gc = gspread.service_account(filename=cur_path + "\\service_account.json")


def get_online_sheet_data(project_name: str) -> dict:

    sh = gc.open("测试报告")
    worksheet = sh.worksheet(project_name)
    # 测试人员
    tester = worksheet.acell('B2').value
    # 计划测试时间
    planning_test_time = worksheet.acell('B3').value
    # 实际测试时间
    actual_test_time = worksheet.acell('B4').value
    # 提测延期时长
    sm_test_time_delay = worksheet.acell('B5').value
    # 需求变更次数
    requirements_change_times = worksheet.acell('B6').value
    # 需求变更备注
    remark_requirements_change = worksheet.acell('B7').value
    # 接口变更次数
    interface_change_times = worksheet.acell('B8').value
    # 接口变更备注
    remark_interface_change = worksheet.acell('B9').value
    # 风险
    risks = worksheet.row_values(10)[1:]
    # 问题
    questions = worksheet.row_values(11)[1:]
    # 建议
    advices = worksheet.row_values(12)[1:]
    # 禅道项目链接
    zentao_link = worksheet.acell('B13').value
    data_list = [
        'tester', 'planning_test_time', 'actual_test_time', 'sm_test_time_delay', 'requirements_change_times',
        'remark_requirements_change', 'interface_change_times', 'remark_interface_change', 'risks', 'questions',
        'advices', 'zentao_link'
    ]
    data = [
        tester, planning_test_time, actual_test_time, sm_test_time_delay, requirements_change_times,
        remark_requirements_change, interface_change_times, remark_interface_change, risks, questions,
        advices, zentao_link
    ]
    data_dict = dict(zip(data_list, data))
    return data_dict


def get_interface_data(project_name: str):
    sh = gc.open("测试报告")
    worksheet = sh.worksheet(project_name)
    interface_data_list = []
    interface_data_url_list = worksheet.col_values(2)[15:]
    interface_data_name_list = worksheet.col_values(1)[15:]
    for i, j in zip(interface_data_name_list, interface_data_url_list):
        interface_data_list.append([i, j])
    return interface_data_list


if __name__ == '__main__':
    project_name = "【220413】场景优化专项-平台功能"
    data_dict = get_online_sheet_data(project_name)
    print(data_dict)