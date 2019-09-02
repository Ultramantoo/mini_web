import socket
import re
import multiprocessing
import time
import mini_frame_05


class WGSIServer(object):
    def __init__(self):
        """用来完成整体的控制"""
        # 1. 创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定7788端口
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. 绑定
        self.tcp_server_socket.bind(("", 7890))

        # 3. 变为监听套接字
        self.tcp_server_socket.listen(128)

    # @staticmethod
    def service_client(self, new_socket):
        """为这个客户端返回数据"""
        # 1.接收浏览器发送过来请求，即Http请求
        request = new_socket.recv(1024).decode()
        # print(request)
        request_lines = request.splitlines()
        print(request_lines[0])

        file_name = re.findall(" (.+) HTTP/1.1", request_lines[0])[0]
        # print(request_page)
        if file_name == "/":
            file_name = "/index.html"
        file_name = file_name[1:]
        print(file_name)

        # 2.返回ht格式的数据，给浏览器
        if not file_name.endswith(".py"):
            # py 结尾为动态
            # noinspection PyBroadException
            try:
                with open(r".\html\\" + file_name, "rb") as f:
                    html_content = f.read()
            except Exception:
                # 无法访问的页面时
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "------file not found------"
                html_content = response.encode("utf-8")
            else:
                # 2.1准备发送给浏览器的数据--header
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                # 2.2 准备发送给浏览器的数据---boy
                new_socket.send(response.encode("utf-8"))
            new_socket.send(html_content)

        else:
            # 2.2 如果。py
            # body = "hello world {}".format(time.ctime())
            # print(file_name)
            # if file_name == "login.py":
            #     body = mini_frame.login()
            # elif file_name == "register.py":
            #     body = mini_frame.register()
            env = dict()
            body = mini_frame_05.application(env, self.set_response_header)

            response = "HTTP/1.1 {}\r\n".format(self.status)
            for temp in self.headers:
                response += "{}:{}\r\n".format(temp[0],temp[1])
            response += "\r\n"
            # 准备发送给浏览器的数据---boy
            response += body
            new_socket.send(response.encode("utf-8"))

        # 3.关闭套接字
        new_socket.close()

    def set_response_header(self, status, headers):
        self.status = status
        self.headers = [('server', 'mimi_frame v8.8')] +headers

    def run_forever(self):

        while True:
            # 4. 等待新客户端链接
            new_socket, client_addr = self.tcp_server_socket.accept()

            # 5. 为这个客户端服务
            # service_client(new_socket)
            p = multiprocessing.Process(target=self.service_client, args=(new_socket,))
            p.start()

            new_socket.close()

        # break
        # 关闭监听套接字
        # self.tcp_server_socket.close()


def main():
    wsgi_server = WGSIServer()
    wsgi_server.run_forever()


# 类 只在局部起作用的可以不加 self

if __name__ == "__main__":
    main()
