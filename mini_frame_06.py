def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])


    file_name = env["PATH_INFO"]
    print(file_name)
    if file_name == "index.py":
        return index()

    if file_name == "login.py":

        return login()
    else:
        return 'Hello World! 我爱你中国....'

def index():
    return "刚开始咯"

def login():
    return "快上啊。。。"


