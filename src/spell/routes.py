from flask import abort, url_for, flash, redirect, request, Blueprint,abort,make_response,jsonify
from src import mongo
import datetime,tempfile
from src.config import Config
import os
from werkzeug.utils import secure_filename


spell = Blueprint('spell', __name__)


@spell.route("/spellcheck", methods=['GET', 'POST'])
def spellcheck():
    total_result=[]
    imageList=[]
    temp_dir=""
    error_obj={}
    try:
        print("Inside spell check... " ,request.args.get("language"),Config)
        # serverLog({"inou"})
        filename=""
        midname=datetime.datetime.now()
        if (request.method == "POST"):
            if ("file" not in request.files):
                error_obj['message']='Invalid file.'
                return jsonify(error_obj),500
            file = request.files["file"]
            if(file.filename[-4:].lower()!='.pdf'):
                error_obj['message']='Please select valid file type.'
                return jsonify(error_obj),500
            temp_dir = tempfile.mkdtemp(("-"+str(midname).replace(":", "-")),"PMR_",Config.CWD+os.sep+"GENERATED"+os.sep+"SPELL")
            # temp_dir = tempfile.mkdtemp(("-"+str(datetime.datetime.now()).replace(":", "-")),"PMR_",Config.CWD+os.sep+"spellFolder")
            print("Creating temp folder ..",temp_dir)
            if file and allowed_file(file.filename):
                renamefile=file.filename.split('.pdf')[0]+"_"+str(midname)+".pdf"
                filename = secure_filename(renamefile) 
                # print(filename)
                file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            spellcheck= SpellCheckCntroller()
            total_result = spellcheck.convert_pdf_images(UPLOAD_FOLDER+os.sep+filename,temp_dir,request.args.get("language"))
            newpdf = ("PMR_output_"+str(random.randint(0,100000000))+".pdf")
            total_result["pdf_url"]= "http://emrintegration.indegene.com:4200/GENERATED/"+newpdf

            for p in total_result["pth"]:
                imageList.append(p.split(Config.CWD)[1])
            total_result["imageUrls"] = imageList

            total_result["_name"]=newpdf
            spellcheck.pdfConverter(total_result["pth"], os.path.join(os.path.join(Config.CWD,"GENERATED"), newpdf))
            del total_result["pth"]

    # except KeyError as keyerr:
    #     print(keyerr)
    #     error_obj["_error"]="Error key error"
    #     total_result.append(error_obj)  
    except Exception as err:
        print(111)
        print(type(err).__name__, err)
        print("end")
        error_obj["_error"]=str(err)
        total_result.append(error_obj)
        return abort(500,err)
    # finally: 
    #     try:
    #         print("Deleting the temperary file..!")
    #         if(os.path.isdir(temp_dir)):
    #             shutil.rmtree(temp_dir)
    #     except OSError as os_err:
    #         print(222)
    #         print(type(os_err).__name__, os_err)
    #         # return str(os_err) 
  
    print("returning response...")

    # serverLog({'event':"Spell check Success","function":"Spell Check","Description":newpdf,"createdBy":"USER"})
    return jsonify(data=total_result)



def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS