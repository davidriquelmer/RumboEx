db_username = 'root'
db_password = ''
db_name = 'rumboex'
db_hostname = 'localhost'

DEBUG = True
SECRET_KEY = "s0me random RumboEx string"
SQLALCHEMY_DATABASE_URI = "mysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=db_username,
                                                                                   DB_PASS=db_password,
                                                                                   DB_ADDR=db_hostname,
                                                                                   DB_NAME=db_name)

