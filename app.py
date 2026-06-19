from flask import Flask, render_template, request
import sqlite3
from markupsafe import escape

app = Flask(__name__)
@app.after_request
def adicionar_csp(response):
    
    response.headers["Content-Security-Police"] = ("default-src 'self'; " "script-src 'self'; ")

    response.headers["Cache-Control"] = "no-store"

    response.headers["X-Frame-Options"] = "DENY"

    return response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        nome = escape(request.form["nome"])
        telefone = escape(request.form["telefone"])
        email = escape(request.form["email"])
        site = escape(request.form["site"])
        if site and not site.startswith(("http://", "https://")):
            site = "Site não permitido"
        experiencia = escape(request.form["experiencia"])

        conexao = sqlite3.connect("curriculos.db")
        cursor = conexao.cursor()

        cursor.execute("""
        INSERT INTO curriculos
        (nome, telefone, email, site, experiencia)
        VALUES (?, ?, ?, ?, ?)
        """, (nome, telefone, email, site, experiencia))

        conexao.commit()
        conexao.close()

    return render_template("cadastro.html")

@app.route("/curriculos")
def curriculos():

    conexao = sqlite3.connect("curriculos.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, email FROM curriculos")

    curriculos = cursor.fetchall()

    conexao.close()
    return render_template("lista.html", curriculos=curriculos)

@app.route("/consulta/<int:id>")
def consulta(id):
    conexao = sqlite3.connect("curriculos.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM curriculos WHERE id=?",
        (id,)
    )

    curriculo = cursor.fetchone()
    conexao.close()

    return render_template("consulta.html", curriculo=curriculo)


app.run(host="0.0.0.0", port=5000, debug=True)