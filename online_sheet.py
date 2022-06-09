import os

import gspread

cur_path = os.path.abspath(os.path.dirname(__file__))
gc = gspread.service_account(filename=cur_path + "/service_account.json")
sh = gc.open("测试报告")


def get_online_sheet_data(project_name: str) -> dict:
    worksheet = sh.worksheet(project_name)
    worksheet_result = worksheet.get_all_records()
    worksheet_result_value = [d['子项'] for d in worksheet_result]
    # 测试人员
    tester = worksheet_result_value[0]
    # 计划测试时间
    planning_test_time = worksheet_result_value[1]
    # 实际测试时间
    actual_test_time = worksheet_result_value[2]
    # 提测延期时长
    sm_test_time_delay = worksheet_result_value[3]
    # 需求变更次数
    requirements_change_times = worksheet_result_value[4]
    # 需求变更备注
    remark_requirements_change = worksheet_result_value[5]
    # 接口变更次数
    interface_change_times = worksheet_result_value[6]
    # 接口变更备注
    remark_interface_change = worksheet_result_value[7]
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
    worksheet = sh.worksheet(project_name)
    interface_data_list = []
    interface_data_url_list = worksheet.col_values(2)[15:]
    interface_data_name_list = worksheet.col_values(1)[15:]
    for i, j in zip(interface_data_name_list, interface_data_url_list):
        interface_data_list.append([i, j])
    return interface_data_list


def get_not_hidden_project_name_list() -> list:
    not_hidden_project_name_list = []
    fetch_sheet_metadata = sh.fetch_sheet_metadata()
    for i in fetch_sheet_metadata['sheets']:
        try:
            if i['properties']['hidden']:
                continue
        except KeyError:
            not_hidden_project_name_list.append(i['properties']['title'])
    return not_hidden_project_name_list

if __name__ == '__main__':
    project_name = '【220413】场景优化专项-平台功能'
    worksheet = sh.worksheet(project_name)
    result = worksheet.get_all_records()
    result_value = [d['子项'] for d in result]
    # interface_data_url_list = [d['接口URL'] for d in result if d['接口URL'] != '']
    # interface_data_name_list = [d['接口名称'] for d in result if d['接口名称'] != '']
    print(result)
    print(result_value)
    # print(interface_data_url_list)
    # print(interface_data_name_list)



