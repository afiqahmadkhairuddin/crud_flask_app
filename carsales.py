from flask import Flask, render_template, request, redirect
import pymysql

carsales = Flask(__name__)


def connection():
    s = 'localhost'  # Your server(host) name
    d = 'carsales'
    u = 'root'  # Your login user
    p = ''  # Your login password
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn


# ini main route untuk page. fetchall untuk fetch semua data dari cursor.
@carsales.route("/")
def main():
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TblCars")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1],
                    "year": row[2], "price": row[3]})
    conn.close()
    return render_template("carslist.html", cars=cars)

# ini adalah route add car menggunakan template yang sama seperti edit (route dibawah) menggunakan method get post
@carsales.route("/addcar2", methods=['GET', 'POST'])
def addcar2():
    if request.method == 'GET':
        return render_template("addcar2.html")
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        year = int(request.form["year"])
        price = float(request.form["price"])
        #perhatikan data yang difetch adalah oleh price digunakan logik seperti di price2
        price2 = price/2
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO TblCars (id, name, year, price) VALUES (%s, %s, %s, %s)", (id, name, year, price2))
        conn.commit()
        conn.close()
        return redirect('/')

#



#edit cars
@carsales.route('/updatecar/<int:id>', methods=['GET', 'POST'])
def updatecar(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM TblCars WHERE id = %s", (id))
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1],
                      "year": row[2], "price": row[3]})
        conn.close()
        return render_template("addcar.html", car=cr[0])
    if request.method == 'POST':
        name = str(request.form["name"])
        year = int(request.form["year"])
        price = float(request.form["price"])
        cursor.execute(
            "UPDATE TblCars SET name = %s, year = %s, price = %s WHERE id = %s", (name, year, price, id))
        conn.commit()
        conn.close()
        return redirect('/')

# untuk delete entries
@carsales.route('/deletecar/<int:id>')
def deletecar(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TblCars WHERE id = %s", (id))
    conn.commit()
    conn.close()
    return redirect('/')


if(__name__ == "__main__"):
    carsales.run()
