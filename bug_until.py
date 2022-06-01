import datetime
import time


def str_to_datetime(date_str: str):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(date_str, "%Y-%m-%d %H:%M:%S"))


def init_bug_data(bug_tuple: list) -> list:
    bug_list_dict = []
    for bug in bug_tuple:
        if bug[-1] is None:
            bug_list_dict.append({
                "product": bug[0],
                "project": bug[1],
                "bug_id": bug[2],
                "env": bug[3],
                "test_times": bug[4],
                "platform": bug[5],
                "bug_title": bug[6],
                "bug_level": bug[7],
                "bug_created_dept": bug[8],
                "bug_creator": bug[9],
                "bug_created_date": str_to_datetime(str(bug[10])),
                "bug_version": bug[11],
                "bug_dept": bug[12],
                "bug_assigned_dept": bug[13],
                "bug_assigned_date": str_to_datetime(str(bug[14])),
                "bug_solved_dept": bug[15],
                "bug_solved_people": bug[16],
                "bug_solved_date": bug[17],
                "bug_solved_version": bug[18],
                "bug_solved_reason": bug[19],
                "bug_status": bug[20],
                "bug_activated_times": bug[21],
                "serious": bug[22],
                "solved_time": bug[23],
            })
        else:
            bug_list_dict.append({
                "product": bug[0],
                "project": bug[1],
                "bug_id": bug[2],
                "env": bug[3],
                "test_times": bug[4],
                "platform": bug[5],
                "bug_title": bug[6],
                "bug_level": bug[7],
                "bug_created_dept": bug[8],
                "bug_creator": bug[9],
                "bug_created_date": str_to_datetime(str(bug[10])),
                "bug_version": bug[11],
                "bug_dept": bug[12],
                "bug_assigned_dept": bug[13],
                "bug_assigned_date": str_to_datetime(str(bug[14])),
                "bug_solved_dept": bug[15],
                "bug_solved_people": bug[16],
                "bug_solved_date": str_to_datetime(str(bug[17])),
                "bug_solved_version": bug[18],
                "bug_solved_reason": bug[19],
                "bug_status": bug[20],
                "bug_activated_times": bug[21],
                "serious": bug[22],
                "solved_time": float(bug[23]),
            })
    return bug_list_dict


def get_ci_time(bug_tuple):
    min_bug_created_date = bug_tuple[0]["bug_created_date"]
    max_bug_solved_date = bug_tuple[0]["bug_solved_date"]
    for bug in bug_tuple:
        if bug["bug_created_date"] != "0000-00-00 00:00:00" and bug["bug_solved_date"] != "0000-00-00 00:00:00":
            if bug["bug_created_date"] <= min_bug_created_date:
                min_bug_created_date = bug["bug_created_date"]
            if bug["bug_solved_date"] >= max_bug_solved_date:
                max_bug_solved_date = bug["bug_solved_date"]
    min_bug_created_date = datetime.datetime.strptime(min_bug_created_date, "%Y-%m-%d %H:%M:%S")
    max_bug_solved_date = datetime.datetime.strptime(max_bug_solved_date, "%Y-%m-%d %H:%M:%S")
    return (max_bug_solved_date - min_bug_created_date).days


def get_bug_min_and_max_time(bug_tuple, bug_data_type):
    min_bug_date = "9999-99-99 00:00:00"
    max_bug_date = "0000-00-00 00:00:00"
    for bug in bug_tuple:
        if bug["bug_solved_date"] != "0000-00-00 00:00:00":
            if bug[bug_data_type] < min_bug_date:
                min_bug_date = bug[bug_data_type]
            if bug[bug_data_type] > max_bug_date:
                max_bug_date = bug[bug_data_type]
    min_bug_date = datetime.datetime.strptime(min_bug_date, "%Y-%m-%d %H:%M:%S")
    max_bug_date = datetime.datetime.strptime(max_bug_date, "%Y-%m-%d %H:%M:%S")
    return min_bug_date, max_bug_date


def get_created_bug_min_and_max_time(bug_tuple):
    min_bug_created_date = "9999-99-99 00:00:00"
    max_bug_created_date = "0000-00-00 00:00:00"
    for bug in bug_tuple:
        if bug["bug_created_date"] != "0000-00-00 00:00:00" and bug["bug_created_date"] != "0000-00-00 00:00:00":
            if bug["bug_created_date"] < min_bug_created_date:
                min_bug_created_date = bug["bug_created_date"]
            if bug["bug_created_date"] > max_bug_created_date:
                max_bug_created_date = bug["bug_created_date"]
    min_bug_created_date = datetime.datetime.strptime(min_bug_created_date, "%Y-%m-%d %H:%M:%S")
    max_bug_created_date = datetime.datetime.strptime(max_bug_created_date, "%Y-%m-%d %H:%M:%S")
    return min_bug_created_date, max_bug_created_date
