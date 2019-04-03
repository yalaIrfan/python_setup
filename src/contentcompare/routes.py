from flask import render_template, url_for, flash, redirect, request, Blueprint


contentcompare = Blueprint('contentcompare', __name__)


@contentcompare.route("/contentcompare", methods=['GET', 'POST'])
def contentcomparecheck():
    print("contentcompare check")

    return "contentcompare checkk success"
