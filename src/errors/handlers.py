from flask import Blueprint, render_template,abort,make_response,jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    # return abort(make_response(jsonify(error="Page not found."), 404))
    return jsonify(error="Page not found."),404


@errors.app_errorhandler(403)
def error_403(error):
    # return abort(make_response(jsonify(error="Authontication require."), 403))

    return jsonify(error="Authontication require."),403


# @errors.app_errorhandler(500)
# def error_500(error):
#     # return abort(make_response(jsonify(error="Service unavailable. Please try after sometime!"), 500))
#     return jsonify(error="Service unavailable. Please try after sometime!"),500

@errors.app_errorhandler(501)
def error_500(error):
    # return abort(make_response(jsonify(error="Service unavailable. Please try after sometime!"), 501))
    return jsonify(error="Oops something went wrong. Please try after sometime!"),501



# To through instant errors use this from the method
# return abort(make_response(jsonify(error="Invalid file type."), 400))
