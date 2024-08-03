from flask import Flask, render_template, redirect, url_for, request, Response

from modules.database import DB
from modules.storage import Storage
from modules.webhook import Webhook
from modules.webconfig import WebConfig
from modules.auth import Auth
from modules.logger import Logger

from modules.safe_md import filter, text2md

app = Flask(__name__)

@app.route('/')
def root():
    client_ip = request.remote_addr
    Logger.debug(f"{client_ip}: connected to the server")

    return redirect(url_for("index"))

@app.route("/index")
def index():
    names = DB.get_names()
    titles = [name[0] for name in names]

    return render_template("index.html", titles=titles)

@app.route("/download", methods=["POST"])
def download():
    client_ip = request.remote_addr
    password = request.form["password"]
    title = request.form["file_name"]

    if (not Auth.is_valid(password)):
        return redirect(url_for("index"))

    response = Response(Storage.get(title),
                    mimetype="application/octet-stream",
                    headers={"Content-Disposition": f"attachment; filename={title}"}
                    )
    
    Logger.info(f"{client_ip}: File {title} downloaded")
    
    return response

@app.route("/add_page")
def add_page():
    return render_template("add.html")

@app.route("/add", methods=["POST"])
def add():
    client_ip = request.remote_addr
    title = request.form["title"]
    password = request.form["password"]
    content = request.form["content"]
    is_md = request.form.get("is_md")
    content_type = "markdown" if is_md else "text"

    if (Auth.is_valid(password)):
        if (content_type == "markdown" and not filter(content)):
            return redirect(url_for("add_page"))
        
        DB.upload(title, password, content, content_type)

        Webhook.send(f"{title}\n{content}")
        Logger.info(f"{client_ip}: {content_type} {title} added")

        return redirect(url_for("index"))
    
    return redirect(url_for("add_page"))

@app.route("/file_add_page")
def file_add_page():
    return render_template("file_add.html")

@app.route("/file_add", methods=["POST"])
def file_add():
    client_ip = request.remote_addr
    title = request.form["title"]
    password = request.form["password"]
    file = request.files["file"]

    if (Auth.is_valid(password)):
        if (not DB.exists(title) and not Storage.exists(title)):
            DB.upload(title, password, file.filename, "file")
            Storage.upload(file)

            Webhook.send(f"{title}\n{file.filename}")
            Logger.info(f"{client_ip}: file {title} added")

            return redirect(url_for("index"))
        
    return redirect(url_for("file_add_page"))

@app.route("/content/<title>", methods=["POST", "GET"])
def content(title):
    if request.method == "GET":
        return render_template("auth.html", title=title, query="content")
    password = request.form["password"]

    if (Auth.is_valid(password)):
        content = DB.get(title, password)
        content_type = DB.get_content_type(title, password)
        md_content = ""
        file_size = "0"

        if (content_type == "markdown"):
            md_content = text2md(content)
        
        elif (content_type == "file"):
            file_size = f"{Storage.get_file_size(content):.2f}"

        return render_template("content.html", title=title, content=content, content_type=content_type, password=password, md_content=md_content, file_size=file_size)
    
    return render_template("auth.html", title=title, query="content")

@app.route("/edit_page", methods=["POST"])
def edit_page():
    title = request.form["title"]
    password = request.form["password"]
    content = request.form["content"]
    content_type = request.form["content_type"]

    return render_template("edit.html", title=title, password=password, content=content, content_type=content_type)

@app.route("/edit", methods=["POST"])
def edit():
    content_type = request.form["content_type"]
    original_title = request.form["original_title"]
    original_password = request.form["original_password"]

    title = request.form["title"]
    password = request.form["password"]
    content = request.form["content"]

    if (Auth.is_valid(password)):
        DB.delete(original_title, original_password)
        DB.upload(title, password, content, content_type)

        Webhook.send(f"{title}\n{content}")

        return redirect(url_for("index"))
    
    return redirect(url_for("edit_page", title=title, password=password, content=content))

@app.route("/auth", methods=["POST"])
def auth():
    title = request.form["title"]
    query = request.form["query"]

    return render_template("auth.html", title=title, query=query)

@app.route("/delete", methods=["POST"])
def delete():
    client_ip = request.remote_addr
    title = request.form["title"]
    password = request.form["password"]

    if (Auth.is_valid(password)):
        content_type = DB.get_content_type(title, password)
        file_name = DB.get(title, password)
        DB.delete(title, password)

        Logger.info(f"{client_ip}: {content_type} {title} deleted")

        if content_type == "file":
            Storage.delete(file_name)

            Logger.info(f"{client_ip}: file {title} deleted")

        return redirect(url_for("index"))

    return render_template("auth.html", title=title, query="delete")

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=WebConfig.get_port(),
            debug=WebConfig.get_debug())
