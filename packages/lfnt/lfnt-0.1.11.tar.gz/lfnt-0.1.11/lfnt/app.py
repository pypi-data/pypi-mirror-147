from flask import Flask, render_template
from .digestion import DigestiveSystem

app = Flask(__name__, static_url_path="", static_folder="static")
de = DigestiveSystem()


def get_data():
    return de.dump()


@app.route("/")
def index():
    return render_template("home.html", data=get_data())


@app.route("/profile")
def profile():
    return render_template("profile.html", data=get_data())


@app.route("/environment")
def environment():
    return render_template("environment.html", data=get_data())


@app.route("/package/<pkgmgr>/<pkg>")
def package_info(pkgmgr, pkg):
    pkginfo = de.get_package(pkgmgr, pkg)
    return render_template(
        "package.html", pkgmgr=pkgmgr, pkg=pkg, data=get_data(), pkginfo=pkginfo
    )


@app.route("/package/<pkgmgr>/<pkg>/uninstall")
def package_uninstall(pkgmgr, pkg):
    pkginfo = de.poop_package(pkgmgr, pkg)
    return render_template(
        "package.html", pkgmgr=pkgmgr, pkg=pkg, data=get_data(), pkginfo=pkginfo
    )


if __name__ == "__main__":
    app.run()
