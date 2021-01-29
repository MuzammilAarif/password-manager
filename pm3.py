
from flask import *
import sqlite3


def get_table(username):
    rank = username[-3:]
    if rank == 'adm':
        table = "admin_cred"
    elif rank == 'sad':
        table = "s_admin_cred"
    elif rank == 'int':
        table = "intern_cred"
    else:
        table = "Invalid username!"
    return table


app = Flask(__name__)

app.secret_key = "password"

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    msg = "error"
    if request.method == "POST":
        try:
            global username
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            msg = "Account creation successful!"

            with sqlite3.connect("pass_manager.db") as con:
                cur = con.cursor()
                exe = "INSERT into login_cred (username, email, password) values (?,?,?)"
                cur.execute(exe, (username, email, password))
                con.commit()
                if(username[-3:]!="sad"):
                    cur = con.cursor()
                    exe1 = "INSERT into login_cred_adm (username, email, password) values (?,?,?)"
                    cur.execute(exe1, (username, email, password))
                    con.commit()

        except(e):
            print(e)
            msg = "Failed to create new account"
        finally:
            return render_template("success.html", msg=msg)


@app.route("/login", methods=["POST", "GET"])
def login():
    msg = "error"
    if request.method == "POST":
        try:
            global username
            username = request.form["username"]
            password = request.form["password"]
            session['logged_in'] = True

            with sqlite3.connect("pass_manager.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                exe = "select * from login_cred"
                cur.execute(exe)
                rows = cur.fetchall()
                users = [row["username"] for row in rows]
                passwords = [row["password"] for row in rows]
                if username in users:
                    ind = users.index(username)
                    if password == passwords[int(ind)]:
                        text = "Login successful!"
                        print(text)
                        return render_template("dash.html", text=text)
                    else:
                        msg = "Incorrect password"
                        return render_template("disp_msg.html", msg=msg)
                else:
                    msg = "Username not found! Kindly create an account to continue.."
                    return render_template("disp_msg.html", msg=msg)
        except:
            msg = "Error logging in"
            return render_template("disp_msg.html", msg=msg)


@app.route("/dashboard")
def dashboard():
    return render_template("dash.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "error"
    if request.method == "POST":
        try:
            new_username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            table = get_table(new_username)

            # if (new_username.find(".")):
            #     pass

            # else:
            #     raise TypeError("User not defined")

            with sqlite3.connect("pass_manager.db") as con:
                cur = con.cursor()
                exe = "INSERT into {} (username, email, password) values (?,?,?)".format(
                    table)
                cur.execute(exe, (new_username, email, password))
                con.commit()
                msg = "The credentials added successfully"
        except:
            con.rollback()
            msg = "Ooops! Something went wrong!"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route("/view")
def view():
    con = sqlite3.connect("pass_manager.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rank = username[-3:]
    tables = ['intern_cred', 'admin_cred',
              's_admin_cred', 'login_cred', 'login_cred_adm']
    if rank == 'sad':
        rows = []
        for t in tables[:3]:
            exe = "select * from {}".format(t)
            cur.execute(exe)
            r = cur.fetchall()
            rows = rows+r
    elif rank == 'adm':
        rows = []
        for t in tables[:2]:
            exe = "select * from {}".format(t)
            cur.execute(exe)
            r = cur.fetchall()
            rows = rows+r
    elif rank == 'int':
        rows = []
        exe = "select * from {}".format(tables[0])
        cur.execute(exe)
        rows = cur.fetchall()

    if rank == 'sad':
        cur.execute("select * from login_cred")
        l_rows = cur.fetchall()
        print(l_rows)
        return render_template("list.html", rows=rows, l_rows=l_rows)
    if rank == 'adm':
        cur.execute("select * from login_cred_adm")
        l_rows = cur.fetchall()
        print(l_rows)
        return render_template("list.html", rows=rows, l_rows=l_rows)
    return render_template("list.html", rows=rows)


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    uname = request.form["username"]
    if username[-3:] == 'int':
        msg = "Only admins and super-admins are authorized to delete credentials!"
        return render_template("disp_msg.html", msg=msg)

    table = get_table(uname)
    with sqlite3.connect("pass_manager.db") as con:
        try:
            cur = con.cursor()
            exe = "delete from {} where username = ?".format(table)
            cur.execute(exe, (uname,))
            msg = "Deleted successfully!"
        except:
            msg = "Unable to delete"
        finally:
            return render_template("delete_record.html", msg=msg)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)
