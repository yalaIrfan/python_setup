from flask import render_template, url_for, flash, redirect, request, Blueprint


isi = Blueprint('isi', __name__)


@isi.route("/isicheck", methods=['GET','POST'])
def isicheck():
    print("isicheck check")

    return "isicheck success"


@isi.route("/isicheckcrop", methods=['GET','POST'])
def isicheckcrop():
    print("isicheckcrop check")


    return "isicheckcrop success"


@isi.route("/compareisi", methods=['GET','POST'])
def compareisi():
    print("compareisi check")

    return "compareisi success"


@isi.route("/resetisi", methods=['GET','POST'])
def resetisi():
    print("resetisi check")

    return "resetisi success"