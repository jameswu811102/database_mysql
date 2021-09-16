import pymysql
import prettytable
import os

# 先決條件：先連接資料庫
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

        # (1) 顯示會員列表
        if command == "1":
            cur.execute("SELECT `id`, `name`, `birthday`, `address` FROM `member`")
            p = prettytable.PrettyTable(["編號", "姓名", "生日", "地址"], encoding="utf8")

            for d in cur.fetchall():
                p.add_row(d)
            print(p)
            print("")


        # (2) 新增會員資料
        elif command == "2":
            params = [
                    input("請輸入會員姓名: "),
                    input("請輸入會員生日: "),
                    input("請輸入會員地址: ")
                ]

            # 防止新增資料留白
            if len(params[0]) == 0 or len(params[1]) == 0 or len(params[2]) == 0:
                os.system("cls")
                print("新增資料過程中有資料未輸入，請重新操作並輸入，謝謝！\n")

            else:
                cur.execute("INSERT INTO `member` (`name`, `birthday`, `address`) VALUES (%s, %s, %s)", params)
                link.commit()
                os.system("cls")


        # (3) 更新會員資料
        elif command == "3":
            # 呈現表格
            cur.execute("SELECT `id`, `name`, `birthday`, `address` FROM `member`")
            p = prettytable.PrettyTable(["編號", "姓名", "生日", "地址"], encoding="utf8")

            for d in cur.fetchall():
                p.add_row(d)
            print(p)
            print("")

            # 欲更新資料的索引及修改內容 (考量未輸入及資料編號異常超出範圍或不存在)
            id_number = input("請輸入欲更新資料的編號: ")
            print("")

            if len(id_number) == 0:
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
                    if len(params[0]) == 0 or len(params[1]) == 0 or len(params[2]) == 0:
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
            cur.execute("SELECT `id`, `name`, `birthday`, `address` FROM `member`")
            p = prettytable.PrettyTable(["編號", "姓名", "生日", "地址"], encoding="utf8")

            for d in cur.fetchall():
                p.add_row(d)
            print(p)
            print("")

            # 欲刪除資料的索引 (考量未輸入及資料編號異常超出範圍或不存在)
            id_number = input("請輸入欲刪除資料的編號: ")

            if len(id_number) == 0:
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


        # 操作介面
        print(" (0) 離開程式\n", "(1) 顯示會員列表\n", "(2) 新增會員資料\n", "(3) 更新會員資料\n", "(4) 刪除會員資料\n")
        command = input("操作：")
        if len(command) == 0:
            os.system("cls")
            print("請參照上述指示輸入操作指令\n")
        else:
            os.system("cls")


    # 最後關閉資料庫
    link.close()