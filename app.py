from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL
import math
import csv
import pandas as pd
import numpy as np
from info_gain import info_gain
from scipy.stats import entropy

app = Flask(__name__) #harus sama dengan @
app.config["SECRET_KEY"] = "FAUZAN"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mahasiswa_tif'
# app.config['MYSQL_DB'] = 'nilai_mhs_tif'
# app.config['MYSQL_DB'] = 'mhs_ta'

mysql = MySQL(app)


@app.route("/")
def index():
        return render_template("index.html")

# @app.route("/dataset", defaults={'page':1})
# @app.route("/dataset/page/<int:page>")
@app.route("/dataset")
def dataset():
        # limit = 50
        # offset = page*limit - limit

        # my_cursor = mysql.connection.cursor()
        # my_cursor.execute("SELECT * FROM nilai_test")
        # total_row = my_cursor.rowcount
        # total_page = math.ceil(total_row / limit )

        # next = page+1
        # prev = page-1


        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM nilai_test")
        fetchdata = cur.fetchall()
        cur.close()
        return render_template("dataset.html", tables = fetchdata)


@app.route("/dataset_csv")
def dataset_csv():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM nilai_test")
        fetchdata = cur.fetchall()
        cur.close()

        with open("file/dataset_sistem.csv", "w", newline='', encoding='utf-8') as file:
                a = csv.DictWriter(file, fieldnames=['nilai_ptik','nilai_sd','nilai_dp','nilai_ap','nilai_ecs','nilai_md','nilai_ak','nilai_bd','nilai_mn','nilai_tbo','nilai_std','nilai_sbd','nilai_so','nilai_jk','nilai_ki','nilai_rpl','nilai_si','nilai_kb','nilai_mpti','nilai_pb','nilai_kp','nilai_ta','status_kelulusan'])
                # a = csv.DictWriter(file, fieldnames=['nilai_sd','nilai_dp','nilai_ap','nilai_md','nilai_bd','nilai_mn','nilai_std','nilai_sbd','nilai_kp','nilai_ta','ipk','status_kelulusan'])
                a.writeheader()
                for row in fetchdata:
                        csv.writer(file, delimiter =',', quoting=csv.QUOTE_NONNUMERIC).writerow(row)

        flash("Berhasil Membuat CSV", "success")
        return redirect("/dataset")

@app.route("/transformasi_csv")
def transformasi_csv():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM nilai_transformasi")
        fetchdata = cur.fetchall()
        cur.close()

        with open("file/data_transformasi.csv", "w", newline='', encoding='utf-8') as file:
                a = csv.DictWriter(file, fieldnames=['nilai_ptik','nilai_sd','nilai_dp','nilai_ap','nilai_ecs','nilai_md','nilai_ak','nilai_bd','nilai_mn','nilai_tbo','nilai_std','nilai_sbd','nilai_so','nilai_jk','nilai_ki','nilai_rpl','nilai_si','nilai_kb','nilai_mpti','nilai_pb','nilai_kp','nilai_ta','status_kelulusan'])
                # a = csv.DictWriter(file, fieldnames=['nilai_sd','nilai_dp','nilai_ap','nilai_md','nilai_bd','nilai_mn','nilai_std','nilai_sbd','nilai_kp','nilai_ta','ipk','status_kelulusan'])
                a.writeheader()
                for row in fetchdata:
                        csv.writer(file, delimiter =',', quoting=csv.QUOTE_NONNUMERIC).writerow(row)

        flash("Berhasil Membuat CSV", "success")
        return redirect("/transformasi")

@app.route("/action_upload", defaults={'page':1}, methods=['GET', 'POST'])
@app.route("/action_upload/page/<int:page>")
def form_action_upload(page):
    
    if request.method == 'POST':

        data_csv = pd.read_csv("file/"+request.form['upload_cleaning'])
        # replace missing value
        data_csv.fillna( method ='ffill', inplace = True)
        df_missing = pd.DataFrame(data_csv)
        data_list_missing = df_missing.values.tolist()
        cur_missing = mysql.connection.cursor()
        for row in data_list_missing:
            cur_missing.execute("INSERT INTO nilai_cleaning (nilai_ptik,nilai_sd,nilai_dp,nilai_ap,nilai_ecs,nilai_md,nilai_ak,nilai_bd,nilai_mn,nilai_tbo,nilai_std,nilai_sbd,nilai_so,nilai_jk,nilai_ki,nilai_rpl,nilai_si,nilai_kb,nilai_mpti,nilai_pb,nilai_kp,nilai_ta,status_kelulusan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],row[10], row[11], row[12], row[13], row[14], row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22]))
            mysql.connection.commit()
       

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('A'))] = '4.00'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('A'))] = '4.00'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('A-'))] = '3.70'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('A-'))] = '3.70'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('B+'))] = '3.30'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('B+'))] = '3.30'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('B'))] = '3.00'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('B'))] = '3.00'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('B-'))] = '2.70'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('B-'))] = '2.70'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('C+'))] = '2.30'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('C+'))] = '2.30'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('C'))] = '2.00'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('C'))] = '2.00'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('C-'))] = '1.70'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('C-'))] = '1.70'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('D+'))] = '1.30'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('D+'))] = '1.30'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('D'))] = '1.00'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('D'))] = '1.00'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('D-'))] = '0.50'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('D-'))] = '0.50'

        data_csv['nilai_ptik'].loc[(data_csv['nilai_ptik'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_sd'].loc[(data_csv['nilai_sd'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_dp'].loc[(data_csv['nilai_dp'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_ap'].loc[(data_csv['nilai_ap'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_ecs'].loc[(data_csv['nilai_ecs'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_md'].loc[(data_csv['nilai_md'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_ak'].loc[(data_csv['nilai_ak'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_bd'].loc[(data_csv['nilai_bd'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_mn'].loc[(data_csv['nilai_mn'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_tbo'].loc[(data_csv['nilai_tbo'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_std'].loc[(data_csv['nilai_std'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_sbd'].loc[(data_csv['nilai_sbd'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_so'].loc[(data_csv['nilai_so'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_jk'].loc[(data_csv['nilai_jk'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_ki'].loc[(data_csv['nilai_ki'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_rpl'].loc[(data_csv['nilai_rpl'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_si'].loc[(data_csv['nilai_si'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_kb'].loc[(data_csv['nilai_kb'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_mpti'].loc[(data_csv['nilai_mpti'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_pb'].loc[(data_csv['nilai_pb'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_kp'].loc[(data_csv['nilai_kp'].astype(str) == str('E'))] = '0.00'
        data_csv['nilai_ta'].loc[(data_csv['nilai_ta'].astype(str) == str('E'))] = '0.00'

        df_inisialisasi = pd.DataFrame(data_csv)
        data_list_inisialisasi = df_inisialisasi.values.tolist()
        cur_missing = mysql.connection.cursor()
        for row in data_list_inisialisasi:
            cur_missing.execute("INSERT INTO nilai_transformasi (nilai_ptik,nilai_sd,nilai_dp,nilai_ap,nilai_ecs,nilai_md,nilai_ak,nilai_bd,nilai_mn,nilai_tbo,nilai_std,nilai_sbd,nilai_so,nilai_jk,nilai_ki,nilai_rpl,nilai_si,nilai_kb,nilai_mpti,nilai_pb,nilai_kp,nilai_ta,status_kelulusan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],row[10], row[11], row[12], row[13], row[14], row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22]))
            mysql.connection.commit()
        
        cur_missing.close()

        # return render_template("upload.html", tables = data_list_missing, page=total_page, next=next, prev=prev)
        flash("Berhasil Menghapus Data", "success")

        return render_template("upload.html", tables = data_list_missing)

#         # inisiasi atribut
#         data_csv['ipk'].loc[(data_csv['ipk'].astype(str) >= str(1.00)) & (data_csv['ipk'].astype(str) <= str(2.49))] = 'rendah'
#         data_csv['ipk'].loc[(data_csv['ipk'].astype(str) >= str(2.50)) & (data_csv['ipk'].astype(str) <= str(3.25))] = 'sedang'
#         data_csv['ipk'].loc[(data_csv['ipk'].astype(str) >= str(3.26)) & (data_csv['ipk'].astype(str) <= str(4.00))] = 'tinggi'

#         data_csv['nilai_sd'] = 'sistem digital = ' + data_csv['nilai_sd']
#         data_csv['nilai_dp'] = 'dasar pemrograman = ' + data_csv['nilai_dp']
#         data_csv['nilai_ap'] = 'algoritma dan pemrograman = ' + data_csv['nilai_ap']
#         data_csv['nilai_md'] = 'matematika diskrit = ' + data_csv['nilai_md']
#         data_csv['nilai_bd'] = 'basis data = ' + data_csv['nilai_bd']
#         data_csv['nilai_mn'] = 'metode numerik = ' + data_csv['nilai_mn']
#         data_csv['nilai_std'] = 'struktur data = ' + data_csv['nilai_std']
#         data_csv['nilai_sbd'] = 'sistem basis data = ' + data_csv['nilai_sbd']
#         data_csv['nilai_jk'] = 'jaringan komputer = ' + data_csv['nilai_jk']
#         data_csv['nilai_ki'] = 'kemanan informasi = ' + data_csv['nilai_ki']
#         data_csv['nilai_rpl'] = 'rekayasa perangkat lunak = ' + data_csv['nilai_rpl']
#         data_csv['nilai_si'] = 'sistem informasi = ' + data_csv['nilai_si']
#         data_csv['nilai_kb'] = 'kecerdasan buatan = ' + data_csv['nilai_kb']
#         data_csv['nilai_pb'] = 'pemrograman bergerak = ' + data_csv['nilai_pb']
#         data_csv['nilai_kp'] = 'nilai kp = ' + data_csv['nilai_kp']
#         data_csv['ipk'] = 'nilai ipk = ' + data_csv['ipk']
#         # data_csv['nilai_kp'] = 'kerja praktek = ' + data_csv['nilai_kp']
#         # data_csv['nilai_ta'] = 'tugas akhir = ' + data_csv['nilai_ta']

#         # data_csv['wis_smt'].loc[(data_csv['wis_smt'].astype(str) == str(8)) ] = '8 semester'
#         # data_csv['wis_smt'].loc[(data_csv['wis_smt'].astype(str) == str(9)) ] = '9-10 semester'
#         # data_csv['wis_smt'].loc[(data_csv['wis_smt'].astype(str) == str(10)) ] = '9-10 semester'
#         # data_csv['wis_smt'].loc[(data_csv['wis_smt'].astype(str) >= str(11)) & (data_csv['wis_smt'].astype(str) <= str(14))] = 'diatas 10 semester'
#         # data_csv['wis_smt'].loc[(data_csv['wis_smt'].astype(str) <= str(8))] = 'cepat lulus'
#         # data_csv['wis_smt'].loc[(data_csv['wis_smt'].astype(str) >= str(9))] = 'lambat lulus'
        
#         df_inisialisasi = pd.DataFrame(data_csv)
#         data_list_inisialisasi = df_inisialisasi.values.tolist()
#         cur_inisialisasi = mysql.connection.cursor()
#         for row in data_list_inisialisasi:
#             cur_inisialisasi.execute("INSERT INTO nilai_inisialisasi_atribut (nilai_sd,nilai_dp,nilai_ap,nilai_md,nilai_bd,nilai_mn,nilai_std,nilai_sbd,nilai_jk,nilai_ki,nilai_rpl,nilai_si,nilai_kb,nilai_pb,nilai_kp,ipk,status_kelulusan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],row[10], row[11], row[12], row[13], row[14], row[15],row[16],))
#             # cur_inisialisasi.execute("INSERT INTO nilai_inisialisasi_atribut (nilai_sd,nilai_dp,nilai_ap,nilai_md,nilai_bd,nilai_mn,nilai_std,nilai_sbd,nilai_kp,nilai_ta,ipk,status_kelulusan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],))
#             mysql.connection.commit()
#         cur_inisialisasi.close()

#         # inconsistent_data
#         atributs = data_csv.columns
#         for atribut in atributs:
#             data_csv[atribut] = data_csv[atribut].astype(str).str.upper()    
#         df_inconsistent = pd.DataFrame(data_csv)
#         data_list_inconsistent = df_inconsistent.values.tolist()
#         cur_inconsistent = mysql.connection.cursor()
#         for row in data_list_inconsistent:
#             cur_inconsistent.execute("INSERT INTO nilai_inconsistent_data (nilai_sd,nilai_dp,nilai_ap,nilai_md,nilai_bd,nilai_mn,nilai_std,nilai_sbd,nilai_jk,nilai_ki,nilai_rpl,nilai_si,nilai_kb,nilai_pb,nilai_kp,ipk,status_kelulusan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],row[10], row[11], row[12], row[13], row[14], row[15],row[16],))
#             # cur_inconsistent.execute("INSERT INTO nilai_inconsistent_data (nilai_sd,nilai_dp,nilai_ap,nilai_md,nilai_bd,nilai_mn,nilai_std,nilai_sbd,nilai_kp,nilai_ta,ipk,status_kelulusan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],))
#             mysql.connection.commit()
#         cur_inconsistent.close()

#         flash("Berhasil Upload CSV", "info")
#         return render_template("missing_value/form_upload_missing_value.html", datas = data_list_missing, page=total_page, next=next, prev=prev)
        
    else:

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM nilai_cleaning ")
        fetchdata = cur.fetchall()
        cur.close()
        return render_template("upload.html", tables = fetchdata)

@app.route("/infogain", methods=['GET', 'POST'])
def infogain():
        if request.method == 'POST':

                session['gain_ratio'] = request.form['upload_gainratio']
                ranking = request.form['upload_rangking']
                session['ranking_gain_ratio'] = ranking

                list_a = []#list untuk atribut
                db = []#list untuk db
                dataset = []#list untuk db

                file = "file/"+request.form['upload_gainratio']
                data = pd.read_csv(file, quotechar = '"', encoding="ISO-8859-1")#input dataset

                columns = len(data.columns)-1#pilih atribut biasa
                atribut = data.iloc[:,0:columns]

                label = data.iloc[:,-1]#pilih class

                for row in atribut:#hitung information gain
                        igr = info_gain.info_gain_ratio(label, atribut[row]), row
                        list_a.append(igr)#masukkan ke list

                list_a.sort(reverse=True)#urutkan list

                for rank in list_a:#baca list
                        db.append(rank)#masukkan ke list

                select = db[0:int(ranking)]#select 5 atribut teratas

                flash("Berhasil Upload CSV", "info")
                return render_template("infogain.html", datas = list_a, selects = select)
        
        else:
                if 'gain_ratio' in session:
                        list_a = []#list untuk atribut
                        db = []#list untuk db
                        dataset = []#list untuk db

                        file = "file/"+session['gain_ratio']
                        data = pd.read_csv(file, quotechar = '"', encoding="ISO-8859-1")#input dataset

                        columns = len(data.columns)-1#pilih atribut biasa
                        atribut = data.iloc[:,0:columns]

                        label = data.iloc[:,-1]#pilih class

                        for row in atribut:#hitung information gain
                                igr = info_gain.info_gain_ratio(label, atribut[row]), row
                                list_a.append(igr)#masukkan ke list

                        list_a.sort(reverse=True)#urutkan list

                        for rank in list_a:#baca list
                                db.append(rank)#masukkan ke list

                        select = db[0:int(session['ranking_gain_ratio'])]#select 5 atribut teratas
                        
                        return render_template("infogain.html", datas = list_a, selects = select)

                else:
                        return render_template("infogain.html")


@app.route("/transformasi")
def transformasiku():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM nilai_transformasi ")
        fetchdata = cur.fetchall()
        cur.close()
        return render_template("transformasi.html", tables = fetchdata)

@app.route("/hapus_cleaning")
def hapus_cleaning():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM nilai_cleaning")
    cur.execute("DELETE FROM nilai_transformasi")
    mysql.connection.commit()
    cur.close()

    flash("Berhasil Menghapus Data", "success")
    return redirect("/action_upload")

@app.route("/hapus_session_gain_ratio", methods=['GET', 'POST'])
def hapus_session_gain_ratio():
    
    session.pop('gain_ratio', None)
    session.pop('ranking_gain_ratio', None)
    flash("Berhasil Menghapus Data CSV", "danger")
    return render_template("infogain.html")

@app.route("/gain_ratio_csv", methods=['GET', 'POST'])
def gain_ratio_csv():
    if 'gain_ratio' in session:

        list_a = []#list untuk atribut
        db = []#list untuk db
        dataset = []#list untuk db

        file = "file/"+session['gain_ratio']
        data = pd.read_csv(file, quotechar = '"', encoding="ISO-8859-1")#input dataset

        columns = len(data.columns)-1#pilih atribut biasa
        atribut = data.iloc[:,0:columns]

        label = data.iloc[:,-1]#pilih class

        for row in atribut:#hitung information gain
                igr = info_gain.info_gain_ratio(label, atribut[row]), row
                list_a.append(igr)#masukkan ke list

        list_a.sort(reverse=True)#urutkan list

        for rank in list_a:#baca list
            db.append(rank[1])#masukkan ke list

        select = db[0:int(session['ranking_gain_ratio'])]#select 5 atribut teratas
        output = ','.join(map(str, select))

        cur = mysql.connection.cursor()
        cur.execute("SELECT "+output+",status_kelulusan FROM nilai_transformasi")
        fetchdata = cur.fetchall()
        cur.close()

        select.append('status_kelulusan')

        with open("file/gain_ratio_sistem.csv", "w", newline='') as file:
            a = csv.DictWriter(file, fieldnames=select)
            a.writeheader()
            for row in fetchdata:
                csv.writer(file, delimiter =',', quoting=csv.QUOTE_NONNUMERIC).writerow(row)

        flash("Berhasil Membuat CSV", "success")
        return redirect ("/infogain")

    else:
        return "tidak ada session"

if __name__ == "__main__":
        app.run(debug=True, port=5001)