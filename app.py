import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
from pylab import mpl

from bug_sql import get_bug_data, get_chart_index_and_data
from online_sheet import get_online_sheet_data, get_interface_data

# 设置中文字体格式
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# project_name = "【220413】场景优化专项-平台功能"

st.set_page_config(page_title=f"测试报告")

project_name = st.text_input('请输入禅道项目名', "【220413】场景优化专项-平台功能")

sheet_data_dict = get_online_sheet_data(project_name)

# 设置测试报告基本数据
tester = sheet_data_dict['tester']
planning_test_time = sheet_data_dict['planning_test_time']
actual_test_time = sheet_data_dict['actual_test_time']

# 提测延期时长
sm_test_time_delay = sheet_data_dict['sm_test_time_delay']

# 需求变更次数
requirements_change_times = int(sheet_data_dict['requirements_change_times'])
remark_requirements_change = sheet_data_dict['remark_requirements_change']
# 接口变更次数
interface_change_times = int(sheet_data_dict['interface_change_times'])
remark_interface_change = sheet_data_dict['remark_interface_change']
risks = sheet_data_dict['risks']
questions = sheet_data_dict['questions']
advices = sheet_data_dict['advices']

# 禅道项目bug链接
remark_total_bug_num = sheet_data_dict['zentao_link']


st.header(f'{project_name} 测试报告')
st.subheader('测试结论')
st.write(f'- {project_name}CI环境完成测试，测试结果：**`测试通过`**')
st.write(f'- 测试人员 **{tester}**')
st.write(f'- 计划时间 **{planning_test_time}** 天')
st.write(f'- 实际时间 **{actual_test_time}** 天')
st.write(f'- 提测延期时长 **{sm_test_time_delay}** 天')
st.subheader('测试总结')

bug_data = get_bug_data(project_name)

if not bug_data:
    raise ValueError("请输入正确的项目名")

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
remark_damping_bug = ""
for bug in damping_bug_list:
    damping_bug_id_list.append(bug["bug_id"])
if damping_bug_id_list:
    remark_damping_bug = "bugID:" + str(damping_bug_id_list)
# 阻塞性bug超过一天
damping_bug_greater_than_one_day_num = len(damping_bug_greater_than_one_day_list)
damping_bug_greater_than_one_day_id_list = []
remark_damping_bug_greater_than_one_day = ""
for bug in damping_bug_greater_than_one_day_list:
    damping_bug_greater_than_one_day_id_list.append(bug["bug_id"])
if damping_bug_greater_than_one_day_id_list:
    remark_damping_bug_greater_than_one_day = "bugID:" + str(damping_bug_greater_than_one_day_id_list)
# 阻塞性bug超过半天小于一天
damping_bug_greater_than_half_day_and_less_than_one_day_num = \
    len(damping_bug_greater_than_half_day_and_less_than_one_day_list)
damping_bug_greater_than_half_day_and_less_than_one_day_id_list = []
remark_damping_bug_greater_than_half_day_and_less_than_one_day = ""
for bug in damping_bug_greater_than_half_day_and_less_than_one_day_list:
    damping_bug_greater_than_half_day_and_less_than_one_day_id_list.append(bug["bug_id"])
if damping_bug_greater_than_half_day_and_less_than_one_day_id_list:
    remark_damping_bug_greater_than_half_day_and_less_than_one_day = \
        "bugID:" + str(damping_bug_greater_than_half_day_and_less_than_one_day_id_list)
# 阻塞性bug小于半天
damping_bug_less_than_half_day_num = len(damping_bug_less_than_half_day_list)
damping_bug_less_than_half_day_id_list = []
remark_damping_bug_less_than_half_day = ""
for bug in damping_bug_less_than_half_day_list:
    damping_bug_less_than_half_day_id_list.append(bug["bug_id"])
if damping_bug_less_than_half_day_id_list:
    remark_damping_bug_less_than_half_day = \
        "bugID:" + str(damping_bug_less_than_half_day_id_list)
# 二次缺陷bug
secondary_defect_num = len(secondary_defect_bug_list)
damping_secondary_defect_bug_id_list = []
remark_secondary_defect_bug = ""
for bug in secondary_defect_bug_list:
    damping_secondary_defect_bug_id_list.append(bug["bug_id"])
if damping_secondary_defect_bug_id_list:
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
remark_not_solved_bug = ""
for bug in not_solved_bug_list:
    not_solved_bug_id_list.append(bug["bug_id"])
if not_solved_bug_id_list:
    remark_not_solved_bug = "bugID:" + str(not_solved_bug_id_list)
bug_index = ('阻塞性bug', '阻塞性bug修复时长超过1天的数量',
             '阻塞性bug修复时长超过半天小于1天的数量', '阻塞性bug修复时长小于半天的数量', '二次缺陷数量',
             '总bug数量', '禅道遗留未解决bug','需求变更次数', '接口变更次数')

bug_data = [
    (damping_bug_num, remark_damping_bug),
    (damping_bug_greater_than_one_day_num, remark_damping_bug_greater_than_one_day),
    (damping_bug_greater_than_half_day_and_less_than_one_day_num,
     remark_damping_bug_greater_than_half_day_and_less_than_one_day),
    (damping_bug_less_than_half_day_num, remark_damping_bug_less_than_half_day),
    (secondary_defect_num, remark_secondary_defect_bug),
    (total_bug_num, remark_total_bug_num),
    (not_solved_bug_num, remark_not_solved_bug),
    (requirements_change_times, remark_requirements_change),
    (interface_change_times, remark_interface_change),
]
df = pd.DataFrame(data=bug_data, index=bug_index, columns=['数据', '备注'])
st.table(df)
data = bug_data
column_labels = ['数据', '备注']

# fig, ax = plt.subplots()
#
# ax.axis('off')
# table = ax.table(cellText=data, rowLabels=bug_index, colLabels=column_labels, loc="center")
# table.auto_set_font_size(False)
# table.set_fontsize(20)
# table.scale(1, 1)
# ax.title.set_text("表格标题")
# st.pyplot(fig)

# index = pd.MultiIndex.from_tuples(bug_index, names=['first', 'second'])
index, bug_num_list = get_chart_index_and_data(bug_data_list, 'bug_created_date')
for i, value in enumerate(index):
    index[i] = str(index[i])

st.subheader('Bug生成和解决时间分布图')
# index = pd.to_datetime(index, dayfirst=True, format='%Y-%m-%d %H:%M:%S')
fig, ax = plt.subplots(figsize=(10, 6))
fig.autofmt_xdate()
ax.set_yticks(bug_num_list)
ax.set_title("BUG生成分布图")
ax.set_xlabel('日期')
ax.set_ylabel('BUG生成数量')
for i, v in enumerate(bug_num_list):
    ax.text(index[i], bug_num_list[i], bug_num_list[i], color='r', fontsize=15)

ax.plot(index, bug_num_list, 's-', color='r', label='BUG数量')
ax.legend(loc='best')
st.pyplot(fig)

# 生成表格


# annotations_df = pd.DataFrame(
#     bug_num_list,
#     index=index,
#     columns=["每小时生成bug数量"]
# )
# st.line_chart(annotations_df)


bug_data_list.sort(key=lambda x: x["bug_solved_date"])
for bug in bug_data_list:
    if bug["bug_solved_date"] == "0000-00-00 00:00:00":
        bug_data_list.remove(bug)
index = get_chart_index_and_data(bug_data_list, 'bug_solved_date')[0]
for i, value in enumerate(index):
    index[i] = str(index[i])
bug_num_list = get_chart_index_and_data(bug_data_list, 'bug_solved_date')[1]

fig, ax = plt.subplots(figsize=(10, 6))
fig.autofmt_xdate()
ax.set_yticks(bug_num_list)
ax.set_title("Bug解决分布图")
ax.set_xlabel('日期')
ax.set_ylabel('BUG解决数量')
for i, v in enumerate(bug_num_list):
    ax.text(index[i], bug_num_list[i], bug_num_list[i], color='g', fontsize=15)

ax.plot(index, bug_num_list, 'o-', color='g', label='BUG数量')
ax.legend(loc='best')
st.pyplot(fig)

# annotations_df = pd.DataFrame(
#     bug_num_list,
#     index=index,
#     columns=["每小时解决bug数量"]
# )
# annotations_df.index = pd.to_datetime(annotations_df.index)
# st.write(annotations_df)
# st.line_chart(annotations_df)
st.subheader('风险')

if not risks:
    st.markdown("暂无")
else:
    for i, r in enumerate(risks):
        st.markdown(f"**{i+1}**. {r}")

st.subheader('问题和建议')
if not questions:
    st.markdown("暂无")
else:
    for (i, question), advice in zip(enumerate(questions), advices):
        st.write(f"**问题** **{i+1}**:  {question}")
        st.write(f"**建议** **{i+1}**:  {advice}")


st.subheader('测试覆盖的接口')

# 读取xlsx文件
api_sheet_columns = ['接口名', '接口URL']
result = get_interface_data(project_name)

df = pd.DataFrame(data=result, columns=api_sheet_columns)
st.table(df)
