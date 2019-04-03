import os


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587

    #config variables 
# C:\\workspace\\python_book\\pmr\\GENERATED\\SPELL\
	UPLOAD_FOLDER = "C:/workspace/python_book/pmr/UPLOAD_FOLDER"

	UPLOAD_FOLDER_ISI = "C:/workspace/python_book/pmr/UPLOAD_FOLDER_ISI"

	UPLOAD_SIZE = 100 * 1024 * 1024

	STATIC_FOLDER_NAME="GENERATED"

	ALLOWED_EXTENSIONS = set(["pdf"])

	#local
	# MONGO_URI="mongodb://localhost:27017/serverlog"

	#production 
	MONGO_URI="mongodb://yalairfan:yalairfan@ds219100.mlab.com:19100/playvideo"

	CWD=os.getcwd()

	FIlE_SYSTEM=CWD+os.sep+"GENERATED"

	