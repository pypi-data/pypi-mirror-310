# -*- coding: utf-8 -*-
# @Time : 2024/11/19 10:00
# @Author : Zhang Shaodong
# @Email : zsd0830@163.com
# @File : universal_parameter.py
# @Info : 该脚本中包含通用的变量设置

# 如果数据库改了，就要修改这里
ip_database = {"localhost": "wom_db_local", "BA_USING": "BA_USING", "BI_READ": "bi"}  # 需修改本地数据库名
dic_connet = {"localhost": {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': 'zwp650811', 'database': 'wom_db_local'},
              "BA_USING": {'host': '10.26.241.164', 'port': 3306, 'user': 'BA_USING', 'password': 'BA_USING@2022', 'database': ip_database["BA_USING"]},
              "BI_READ": {'host': '10.26.241.164', 'port': 3306, 'user': 'BI_READ', 'password': 'Bireader@1027', 'database': ip_database["BI_READ"]}}
proxy_dict = {"host": "tunnel2.qg.net", "port": "17104", "key": "66D2C356", "passwd": "8A0FDC1CC0D9"}

province_ls = ["北京", "天津", "上海", "重庆", "河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西",
               "山东", "河南", "湖北", "湖南", "广东", "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "台湾", "内蒙古",
               "广西", "西藏", "宁夏", "新疆", "香港", "澳门"]
zhixia_list = ["北京", "天津", "上海", "重庆"]
month_dic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
             "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}