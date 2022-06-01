import datetime

import pymysql
import yaml

from bug_until import init_bug_data, get_ci_time, get_bug_min_and_max_time


def init_zentao_mysql(config):
    db_tmp = pymysql.connect(host=config['zentao']['host'],
                             port=config['zentao']['port'],
                             user=config['zentao']['user'],
                             password=config['zentao']['password'],
                             db=config['zentao']['dbname'])
    db_tmp.autocommit(True)
    return db_tmp


def get_bug_list(name: str, zentao_cursor):
    sql_select = "(select" \
                 "`zt_product`.`name` AS `product`," \
                 "`zt_project`.`name` AS `project`," \
                 "`zt_bug`.`id` AS `bug_id`," \
                 "substring_index( substring_index( `zt_bug`.`title`, '】', 1 ), '【',- ( 1 ) ) AS `env`," \
                 "substring_index( substring_index( `zt_bug`.`title`, '】', 2 ), '【',- ( 1 ) ) AS `times`," \
                 "substring_index( substring_index( `zt_bug`.`title`, '】', 3 ), '【',- ( 1 ) ) AS `platform`," \
                 "`zt_bug`.`title` AS `bug_title`," \
                 "`zt_bug`.`severity` AS `bug_level`," \
                 "`zt_dept1`.`name` AS `bug_created_dept`," \
                 "`zt_bug`.`openedBy` AS `bug_creator`," \
                 "`zt_bug`.`openedDate` AS `bug_created_date`," \
                 "`zt_build1`.`name` AS `bug_version`," \
                 "`zt_dept2`.`name` AS `bug_dept`," \
                 "`zt_bug`.`assignedTo` AS `bug_assigned_dept`," \
                 "`zt_bug`.`assignedDate` AS `bug_assigned_date`," \
                 "`zt_dept3`.`name` AS `bug_solved_dept`," \
                 "`zt_bug`.`resolvedBy` AS `bug_solved_people`," \
                 "`zt_bug`.`resolvedDate` AS `bug_solved_date`," \
                 "`zt_build2`.`name` AS `bug_solved_version`," \
                 "`zt_bug`.`resolution` AS `bug_solved_reason`," \
                 "`zt_bug`.`status` AS `bug_status`," \
                 "`zt_bug`.`activatedCount` AS `bug_activated_times`," \
                 "`zt_bug`.`severity` AS `bug_severity`," \
                 "IF" \
                 "  (" \
                 "  ( `zt_bug`.`resolvedDate` <> '' )," \
                 "  ( timestampdiff( SECOND, `zt_bug`.`openedDate`, `zt_bug`.`resolvedDate` ) / 3600 )," \
                 "NULL" \
                 "  ) AS `bug_solved_time`" \
                 "FROM" \
                 "  (" \
                 "  (" \
                 "  (" \
                 "  (" \
                 "  (" \
                 "  (" \
                 "  (" \
                 "  (" \
                 "  (" \
                 "  ( `zt_bug` LEFT JOIN `zt_user` `zt_user1` ON ( ( `zt_bug`.`openedBy` = `zt_user1`.`account` ) ) )" \
                 "  LEFT JOIN `zt_dept` `zt_dept1` ON ( ( `zt_user1`.`dept` = `zt_dept1`.`id` ) )" \
                 "  )" \
                 "  LEFT JOIN `zt_user` `zt_user2` ON ( ( `zt_bug`.`assignedTo` = `zt_user2`.`account` ) )" \
                 "  )" \
                 "  LEFT JOIN `zt_dept` `zt_dept2` ON ( ( `zt_user2`.`dept` = `zt_dept2`.`id` ) )" \
                 "  )" \
                 "  LEFT JOIN `zt_user` `zt_user3` ON ( ( `zt_bug`.`resolvedBy` = `zt_user3`.`account` ) )" \
                 "  )" \
                 "  LEFT JOIN `zt_dept` `zt_dept3` ON ( ( `zt_user3`.`dept` = `zt_dept3`.`id` ) )" \
                 "  )" \
                 "  LEFT JOIN `zt_product` ON ( ( `zt_bug`.`product` = `zt_product`.`id` ) )" \
                 "  )" \
                 "  LEFT JOIN `zt_project` ON ( ( `zt_bug`.`project` = `zt_project`.`id` ) )" \
                 "  )" \
                 "  LEFT JOIN `zt_build` `zt_build1` ON ( ( `zt_bug`.`openedBuild` = `zt_build1`.`id` ) )" \
                 "  )" \
                 "  LEFT JOIN `zt_build` `zt_build2` ON ( ( `zt_bug`.`resolvedBuild` = `zt_build2`.`id` ) )" \
                 "  )" \
                 "WHERE" \
                 "  (zt_product.name = '{name}'" \
                 "  )" \
                 "  AND ( `zt_bug`.`deleted` = '0' )" \
                 "  )".format(name=name)
    zentao_cursor.execute(sql_select)
    bug_list = zentao_cursor.fetchall()
    return bug_list


def get_bug_data(product_name):
    with open('setting.yaml', 'rb') as f:
        config = yaml.safe_load(f)
    db_zentao = init_zentao_mysql(config)
    zentao_cursor = db_zentao.cursor()
    bug_tuple = get_bug_list(product_name, zentao_cursor)
    bug_data_list = init_bug_data(bug_tuple)
    # 阻塞bug
    damping_bug_list = []
    # 阻塞bug解决时间大于1天
    damping_bug_greater_than_one_day_list = []
    # 阻塞bug解决时间大于半天小于1天
    damping_bug_greater_than_half_day_and_less_than_one_day_list = []
    # 阻塞bug解决时间小于半天
    damping_bug_less_than_half_day = []
    # 二次缺陷bug
    secondary_defect_bug = []
    # 未解决bug
    not_solved_bug = []
    for bug in bug_data_list:
        # 判断阻塞性bug
        if bug["bug_title"].find("堵塞") != -1 or bug["bug_title"].find("阻塞") != -1:
            damping_bug_list.append(bug)
            if bug["solved_time"] is not None:
                if bug["solved_time"] > 24:
                    damping_bug_greater_than_one_day_list.append(bug)
                if 12 < bug["solved_time"] < 24:
                    damping_bug_greater_than_half_day_and_less_than_one_day_list.append(bug)
                if bug["solved_time"] < 12:
                    damping_bug_less_than_half_day.append(bug)
        # 二次缺陷bug
        if bug["bug_activated_times"] >= 1:
            secondary_defect_bug.append(bug)
        # 禅道遗留未解决bug
        if bug["solved_time"] is None:
            not_solved_bug.append(bug)
    return bug_data_list, damping_bug_list, damping_bug_greater_than_one_day_list, \
           damping_bug_greater_than_half_day_and_less_than_one_day_list, damping_bug_less_than_half_day, \
           secondary_defect_bug, not_solved_bug


def get_chart_index_and_data(bug_data_list: list, bug_date_type):
    min_time = get_bug_min_and_max_time(bug_data_list, bug_date_type)[0]
    max_time = get_bug_min_and_max_time(bug_data_list, bug_date_type)[1]
    chart_index = [min_time]
    i = min_time
    while True:
        i += datetime.timedelta(hours=1)
        chart_index.append(i)
        if i > max_time:
            break
    bug_num_list = [0 for i in range(len(chart_index))]
    bug_data_list_new = []
    for bug in bug_data_list:
        if bug[bug_date_type] != "0000-00-00 00:00:00":
            bug_data_list_new.append(bug)
    for time, (i, bug_num) in zip(chart_index, enumerate(bug_num_list)):
        for bug in bug_data_list_new:
            if datetime.datetime.strptime(bug[bug_date_type], "%Y-%m-%d %H:%M:%S") - time > datetime.timedelta(hours=1):
                break
            if datetime.datetime.strptime(bug[bug_date_type], "%Y-%m-%d %H:%M:%S") >= time:
                bug_num_list[i] += 1
    time_list = []
    for time, bug_created_num in zip(chart_index, bug_num_list):
        if bug_created_num != 0:
            time_list.append(time)
    while True:
        flag = 0
        for time, bug_num in zip(chart_index, bug_num_list):
            if bug_num == 0:
                bug_num_list.remove(bug_num)
        for index, num in enumerate(bug_num_list):
            if index == len(bug_num_list) - 1 and num != 0:
                flag = 1
        if flag == 1:
            break
    return time_list, bug_num_list


if __name__ == '__main__':
    product_name = "【220426】美区商城-积分兑换 "
    bug_data = get_bug_data(product_name)
    bug_data_list = bug_data[0]
    # for bug_time in bug_data_list:
    #     print(bug_time['bug_solved_date'])
    # print(len(bug_data_list))
    bug_data_list.sort(key=lambda x: x["bug_solved_date"])
    for bug in bug_data_list:
        if bug["bug_solved_date"] == "0000-00-00 00:00:00":
            bug_data_list.remove(bug)

    index = get_chart_index_and_data(bug_data_list, 'bug_solved_date')[0]
    bug_num_list = get_chart_index_and_data(bug_data_list, 'bug_solved_date')[1]
    print(index, bug_num_list,sum(bug_num_list))
    print(bug_data_list,len(bug_data_list))





