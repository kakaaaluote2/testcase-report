import csv

import pandas as pd
import streamlit as st

from bug import get_bug_data, get_chart_index_and_data
from bug_until import get_ci_time

# 设置测试报告基本数据
# 禅道项目名
product_name = "【220426】美区商城-积分兑换 "
test_person = "Link"
planning_test_time = "2022.4.7-2022.4.8"
actual_test_time = "2022.4.7-2022.4.11"
# 提测提前时长及备注
sm_test_time_advance = 0
remark_sm_test_time_advance = "提前提测备注"
# 提测延期长及备注
sm_test_time_delay = 0
remark_sm_test_time_delay = "延期提测备注"
# 处于CI环境时长，默认为0表示bug的最晚解决时间-最早创建时间
ci_time = 0
remark_ci_time = "ci环境时长备注"
# 需求变更次数
requirements_change_times = 0
remark_requirements_change = "需求变更备注"
# 接口变更次数
interface_change_times = 0
remark_interface_change = "接口变更备注"

# 禅道项目bug链接
remark_ = "https://zentao.vesync.cn/zentao/bug-browse-402.html"


st.set_page_config(page_title=f"测试报告")
st.header(f'{product_name}项目测试报告')
st.subheader('测试结论')
st.write(f'{product_name}CI环境完成测试，测试结果：**`测试通过`**')
st.write(f'- 测试人员 {test_person}')
st.write(f'- 计划时间 **{planning_test_time}**')
st.write(f'- 实际时间 **{actual_test_time}**')
st.subheader('测试覆盖的接口')

# 读取xlsx文件
csv_file = open('api.csv', 'r', encoding="UTF-8")
reader = csv.reader(csv_file)
result = []
api_sheet_columns = []
for item in reader:
    if reader.line_num == 1:
        api_sheet_columns = item
    else:
        result.append(item)

df = pd.DataFrame(data=result, columns=api_sheet_columns)
st.table(df)

st.subheader('测试总结')

bug_data = get_bug_data(product_name)
bug_data_list = bug_data[0]
damping_bug_list = bug_data[1]
damping_bug_greater_than_one_day_list = bug_data[2]
damping_bug_greater_than_half_day_and_less_than_one_day_list = bug_data[3]
damping_bug_less_than_half_day_list = bug_data[4]
secondary_defect_bug_list = bug_data[5]
not_solved_bug_list = bug_data[6]
# 初始化表格bug数据
# 阻塞性bug
damping_bug_num = len(damping_bug_list)
damping_bug_id_list = []
for bug in damping_bug_list:
    damping_bug_id_list.append(bug["bug_id"])
remark_damping_bug = "bugID:" + str(damping_bug_id_list)
# 阻塞性bug超过一天
damping_bug_greater_than_one_day_num = len(damping_bug_greater_than_one_day_list)
damping_bug_greater_than_one_day_id_list = []
for bug in damping_bug_greater_than_one_day_list:
    damping_bug_greater_than_one_day_id_list.append(bug["bug_id"])
remark_damping_bug_greater_than_one_day = "bugID:" + str(damping_bug_greater_than_one_day_id_list)
# 阻塞性bug超过半天小于一天
damping_bug_greater_than_half_day_and_less_than_one_day_num = \
    len(damping_bug_greater_than_half_day_and_less_than_one_day_list)
damping_bug_greater_than_half_day_and_less_than_one_day_id_list = []
for bug in damping_bug_greater_than_half_day_and_less_than_one_day_list:
    damping_bug_greater_than_half_day_and_less_than_one_day_id_list.append(bug["bug_id"])
remark_damping_bug_greater_than_half_day_and_less_than_one_day = \
    "bugID:" + str(damping_bug_greater_than_half_day_and_less_than_one_day_id_list)
# 阻塞性bug小于半天
damping_bug_less_than_half_day_num = len(damping_bug_less_than_half_day_list)
damping_bug_less_than_half_day_id_list = []
for bug in damping_bug_less_than_half_day_list:
    damping_bug_less_than_half_day_id_list.append(bug["bug_id"])
remark_damping_bug_less_than_half_day = \
    "bugID:" + str(damping_bug_less_than_half_day_id_list)
# 二次缺陷bug
secondary_defect_num = len(secondary_defect_bug_list)
damping_secondary_defect_bug_id_list = []
for bug in secondary_defect_bug_list:
    damping_secondary_defect_bug_id_list.append(bug["bug_id"])
remark_secondary_defect_bug = "bugID:" + str(damping_secondary_defect_bug_id_list)
# 总bug
total_bug_num = len(bug_data_list)
total_bug_id_list = []
for bug in bug_data_list:
    total_bug_id_list.append(bug["bug_id"])
remark_total_bug_id = "bugID:" + str(total_bug_id_list)
# 禅道遗留未解决bug
not_solved_bug_num = len(not_solved_bug_list)
not_solved_bug_id_list = []
for bug in not_solved_bug_list:
    not_solved_bug_id_list.append(bug["bug_id"])
remark_not_solved_bug = "bugID:" + str(not_solved_bug_id_list)

ci_time_final = get_ci_time(bug_data_list)
if ci_time != 0:
    ci_time_final = ci_time
bug_index = ('提测提前时长（小时）', '提测延期时长（小时）', '阻塞性bug数量', '阻塞性bug修复时长超过1天的数量',
             '阻塞性bug修复时长超过半天小于1天的数量', '阻塞性bug修复时长小于半天的数量', '二次缺陷数量',
             '总bug数量', '禅道遗留未解决bug', '项目处于CI环境时长（天）', '需求变更次数', '接口变更次数')
bug_data = [
    (sm_test_time_advance, remark_sm_test_time_advance),
    (sm_test_time_delay, remark_sm_test_time_delay),
    (damping_bug_num, remark_damping_bug),
    (damping_bug_greater_than_one_day_num, remark_damping_bug_greater_than_one_day),
    (damping_bug_greater_than_half_day_and_less_than_one_day_num,
     remark_damping_bug_greater_than_half_day_and_less_than_one_day),
    (damping_bug_less_than_half_day_num, remark_damping_bug_less_than_half_day),
    (secondary_defect_num, remark_secondary_defect_bug),
    (total_bug_num, remark_),
    (not_solved_bug_num, remark_not_solved_bug),
    (ci_time_final, remark_ci_time),
    (requirements_change_times, remark_requirements_change),
    (interface_change_times, remark_interface_change),
]

# 生成表格
df = pd.DataFrame(data=bug_data, index=bug_index, columns=('数据', '备注'))
st.table(df)

st.subheader('Bug生成和解决时间分布图')
index = get_chart_index_and_data(bug_data_list, 'bug_created_date')[0]
for i, value in enumerate(index):
    index[i] = str(index[i])
bug_num_list = get_chart_index_and_data(bug_data_list, 'bug_created_date')[1]
annotations_df = pd.DataFrame(
    bug_num_list,
    index=index,
    columns=["每小时生成bug数量"]
)
# annotations_df.index = pd.to_datetime(annotations_df.index)
# st.write(annotations_df)
st.line_chart(annotations_df)
bug_data_list.sort(key=lambda x: x["bug_solved_date"])
for bug in bug_data_list:
    if bug["bug_solved_date"] == "0000-00-00 00:00:00":
        bug_data_list.remove(bug)
index = get_chart_index_and_data(bug_data_list, 'bug_solved_date')[0]
for i, value in enumerate(index):
    index[i] = str(index[i])
bug_num_list = get_chart_index_and_data(bug_data_list, 'bug_solved_date')[1]
annotations_df = pd.DataFrame(
    bug_num_list,
    index=index,
    columns=["每小时解决bug数量"]
)
# annotations_df.index = pd.to_datetime(annotations_df.index)
# st.write(annotations_df)
st.line_chart(annotations_df)