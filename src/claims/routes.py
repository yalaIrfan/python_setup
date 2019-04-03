from flask import render_template, url_for, flash, redirect, request, Blueprint


claims = Blueprint('claims', __name__)


@claims.route("/claims", methods=['GET', 'POST'])
def claimscheck():
    print("claims check")


    return "claims checkk success"
