import pymysql
import prettytable
import os

# 資料庫表格要設定關聯

# 先連接資料庫
password = input("請輸入資料庫root密碼： ")
Port = input("請輸入資料庫Port： ")
try:
    link = pymysql.connect(
                            host="localhost",
                            user="root",
                            passwd=password,
                            db="python_ai",
                            charset="utf8",
                            port=int(Port))
    cur = link.cursor()
except (pymysql.err.OperationalError, ValueError):
    print("無法連接至資料庫，請重新確認資料庫的root密碼及Port")

else:
    # 操作介面執行
    command = ""
    os.system("cls")

    while command != "0":

        # (1) 顯示會員資料列表
        if command == "1":
            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            TABLE = prettytable.PrettyTable(["編號", "姓名", "生日", "地址"], align="l", encoding="utf8")

            # 先處理其他會員資料
            temp_ls = []
            for temp in cur.fetchall():
                temp_ls.append(temp[0:-1])
            # step1: 相同資料只留一筆，其餘空行
            status_ls = []
            for status in temp_ls:
                if status in status_ls:
                    status_ls.append(["", "", "", ""])
                else:
                    status_ls.append(status)
            # step2: 製作出資料不重複的表格
            for s in status_ls:
                TABLE.add_row(s)

            # 再處理會員電話欄位
            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            tel_ls = []
            for tel in cur.fetchall():
                tel_ls.append(tel[-1])
            TABLE.add_column("電話", tel_ls)
            print(TABLE)
            print("")


        # (2) 新增會員資料
        elif command == "2":
            params = [
                    input("請輸入會員姓名: "),
                    input("請輸入會員生日: "),
                    input("請輸入會員地址: ")
                ]

            # 防止新增資料留白
            if params[0] == "" or params[1] == "" or params[2] == "":
                os.system("cls")
                print("新增資料過程中有資料未輸入，請重新操作並輸入，謝謝！\n")

            else:
                cur.execute("INSERT INTO `member` (`name`, `birthday`, `address`) VALUES (%s, %s, %s)", params)
                link.commit()
                os.system("cls")

        # (3) 更新會員資料
        elif command == "3":
            # 呈現表格
            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            TABLE = prettytable.PrettyTable(["編號", "姓名", "生日", "地址"], align="l", encoding="utf8")

            temp_ls = []
            for temp in cur.fetchall():
                temp_ls.append(temp[0:-1])
            status_ls = []

            for status in temp_ls:
                if status in status_ls:
                    status_ls.append(["", "", "", ""])
                else:
                    status_ls.append(status)

            for s in status_ls:
                TABLE.add_row(s)

            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            tel_ls = []
            for tel in cur.fetchall():
                tel_ls.append(tel[-1])
            TABLE.add_column("電話", tel_ls)
            print(TABLE)
            print("")

            # 欲更新資料的索引及修改內容 (考量未輸入及資料編號異常超出範圍或不存在)
            id_number = input("請輸入欲更新資料的編號: ")
            print("")

            if id_number == "":
                os.system("cls")
                print("未輸入欲更新資料的編號，請重新再試，謝謝！\n")

            else:
                print("若資料沒有要做更新，請輸入原資料，謝謝!")
                if cur.execute("SELECT `id` FROM `member` WHERE `id` = '{}'".format(id_number)):
                    params = [
                            input("請輸入修改後會員姓名: "),
                            input("請輸入修改後會員生日: "),
                            input("請輸入修改後會員地址: ")
                        ]
                    # 防止更新資料留白
                    if params[0] == "" or params[1] == "" or params[2] == "":
                        os.system("cls")
                        print("有資料未輸入，請重新操作，謝謝！\n")
                    else:
                        cur.execute("UPDATE `member`SET `name`= %s, `birthday`= %s, `address`= %s WHERE `id`= '{}'".format(id_number), params)
                        link.commit()
                        os.system("cls")
                else:
                    os.system("cls")
                    print("欲更新資料的編號不存在，請重新再試，謝謝！\n")


        # (4) 刪除會員資料
        elif command == "4":
            # 呈現表格
            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            TABLE = prettytable.PrettyTable(["編號", "姓名", "生日", "地址"], align="l", encoding="utf8")

            temp_ls = []
            for temp in cur.fetchall():
                temp_ls.append(temp[0:-1])
            status_ls = []

            for status in temp_ls:
                if status in status_ls:
                    status_ls.append(["", "", "", ""])
                else:
                    status_ls.append(status)

            for s in status_ls:
                TABLE.add_row(s)

            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            tel_ls = []
            for tel in cur.fetchall():
                tel_ls.append(tel[-1])
            TABLE.add_column("電話", tel_ls)
            print(TABLE)
            print("")

            # 欲刪除資料的索引 (考量未輸入及資料編號異常超出範圍或不存在)
            id_number = input("請輸入欲刪除資料的編號: ")

            if id_number == "":
                os.system("cls")
                print("未輸入欲刪除資料的編號，請重新再試，謝謝！\n")

            else:
                if cur.execute("SELECT `id` FROM `member` WHERE `id` = '{}'".format(id_number)):
                    cur.execute("DELETE FROM `member` WHERE `id` = '{}'".format(id_number))
                    link.commit()
                    os.system("cls")
                else:
                    os.system("cls")
                    print("欲刪除資料的編號不存在，請重新再試，謝謝！\n")


        # (5) 新增會員電話資料
        elif command == "5":
            # 呈現表格
            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            TABLE = prettytable.PrettyTable(["編號", "姓名", "生日", "地址"], align="l", encoding="utf8")

            temp_ls = []
            for temp in cur.fetchall():
                temp_ls.append(temp[0:-1])
            status_ls = []

            for status in temp_ls:
                if status in status_ls:
                    status_ls.append(["", "", "", ""])
                else:
                    status_ls.append(status)

            for s in status_ls:
                TABLE.add_row(s)

            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            tel_ls = []
            for tel in cur.fetchall():
                tel_ls.append(tel[-1])
            TABLE.add_column("電話", tel_ls)
            print(TABLE)
            print("")

            # 新增電話
            id_number = input("請選擇要添加電話的會員編號: ")
            print("")

            if id_number == "":
                os.system("cls")
                print("未輸入欲新增電話的會員編號，請重新再試，謝謝！\n")

            else:
                if cur.execute("SELECT `id` FROM `member` WHERE `id` = '{}'".format(id_number)):
                    tel_number = input("請輸入新增電話: ")
                    cur.execute("INSERT INTO `tel` (`member_id`, `tel`) VALUES (%s, %s)", [id_number, tel_number])
                    link.commit()
                    os.system("cls")

                else:
                    os.system("cls")
                    print("欲新增電話的會員編號不存在，請重新再試，謝謝！\n")

        # (6) 刪除會員電話資料
        elif command == "6":
            # 呈現表格
            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            TABLE = prettytable.PrettyTable(["編號", "姓名", "生日", "地址"], align="l", encoding="utf8")

            temp_ls = []
            for temp in cur.fetchall():
                temp_ls.append(temp[0:-1])
            status_ls = []

            for status in temp_ls:
                if status in status_ls:
                    status_ls.append(["", "", "", ""])
                else:
                    status_ls.append(status)

            for s in status_ls:
                TABLE.add_row(s)

            cur.execute("SELECT `M`.*, `T`.tel FROM `member` AS `M` LEFT JOIN `tel` AS `T` ON `M`.`id` = `T`.`member_id` ORDER BY `id` ASC")
            tel_ls = []
            for tel in cur.fetchall():
                tel_ls.append(tel[-1])
            TABLE.add_column("電話", tel_ls)
            print(TABLE)
            print("")

            # 刪除電話
            id_number = input("請選擇要刪除電話的會員編號: ")
            print("")

            if id_number == "":
                os.system("cls")
                print("未輸入欲刪除電話的會員編號，請重新再試，謝謝！\n")

            else:
                if cur.execute("SELECT `id` FROM `member` WHERE `id` = '{}'".format(id_number)):
                    # 列出選中會員的電話表格
                    cur.execute("SELECT `id`, `tel` FROM `tel` WHERE `member_id` = '{}'".format(id_number))
                    TEL = prettytable.PrettyTable(["編號", "電話"], align="l", encoding="utf8")
                    for t in cur.fetchall():
                        TEL.add_row(t)
                    print(TEL)
                    print("")

                    tel_number = input("請輸入欲刪除的電話編號: ")
                    if tel_number == "":
                        os.system("cls")
                        print("未輸入欲刪除的電話編號，請重新再試，謝謝！\n")

                    else:
                        if cur.execute("SELECT * FROM `tel` WHERE `id` = '{}'".format(tel_number)):
                            cur.execute("DELETE FROM `tel` WHERE `id` = '{}'".format(tel_number))
                            link.commit()
                            os.system("cls")

                        else:
                            os.system("cls")
                            print("欲刪除的電話編號不存在，請重新再試，謝謝！\n")

                else:
                    os.system("cls")
                    print("欲刪除電話的會員編號不存在，請重新再試，謝謝！\n")


        # 操作介面
        print(" (0) 離開程式\n", "(1) 顯示會員列表\n", "(2) 新增會員資料\n", "(3) 更新會員資料\n", "(4) 刪除會員資料\n", "(5) 新增會員的電話\n", "(6) 刪除會員的電話\n")
        command = input("操作：")
        if command == "":
            os.system("cls")
            print("請參照指示輸入操作指令\n")
        else:
            os.system("cls")

    # 最後關閉資料庫
    link.close()
