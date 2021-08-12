from flask import Flask,render_template,redirect,url_for,request,session,flash
from  flask_bcrypt import check_password_hash,generate_password_hash
from Databases import Users,Products

app = Flask(__name__)
app.secret_key = "gnsdghasfgdgynashahydfahsydajajdga"


@app.route('/',methods=['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form["x"]
        email = request.form["y"]
        password = request.form["z"]
        password = generate_password_hash(password)
        try:
            Users.create(name=name,email=email,password=password)
            flash("Account created successfully")
        except Exception:
            flash("That email is already used")
    return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["x"]
        password = request.form["y"]
        try:
            user = Users.get(Users.email == email)
            hashed_password = user.password
            if check_password_hash(hashed_password,password):
                flash("Login successful")
                session["name"] = user.name
                session["email"] = user.email
                session["id"] = user.id
                session["logged_in"] = True
                return  redirect(url_for("home_page"))
        except Users.DoesNotExist:
            flash("Wrong username or password")
    return render_template("login.html")


@app.route('/home')
def home_page():
    if not  session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route('/logout')
def logout():
    if not  session.get("logged_in"):
        return redirect(url_for("login"))
    session.pop("logged_in",None)
    return redirect(url_for("login"))

@app.route('/view_users')
def view_users():
    users = Users.select()
    return  render_template("users.html",users = users)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    if not session.get("logged_in"):
        return  redirect(url_for("login"))
    Users.delete().where(Users.id == id).execute()
    flash("User deleted successfully")
    return redirect(url_for("view_users"))


@app.route('/update_user/<int:id>',methods=['GET','POST'])
def update_user(id):
    user = Users.get(Users.id == id)
    if request.method == "POST":
        updated_name = request.form["x"]
        updated_email = request.form["y"]
        updated_password = request.form["z"]
        hashed_password = generate_password_hash(updated_password)
        user.name = updated_name
        user.email = updated_email
        user.password = hashed_password
        user.save()
        flash("User updated successfully")
        return redirect(url_for("view_users"))
    return render_template("update_user.html",user = user)


@app.route('/add_products',methods=['GET','POST'])
def add_products():
    if request.method == "POST":
        product_name = request.form["jina"]
        product_price = request.form["bei"]
        product_quantity = request.form["wingi"]
        try:
            Products.create(name=product_name,quantity=product_quantity,price=product_price)
            flash("Product added successfully")
        except Exception:
            flash("Adding product failed")
    return render_template("add_products.html")


if __name__ == '__main__':
    app.run()
