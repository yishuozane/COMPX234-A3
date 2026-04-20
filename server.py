import socket
import sys


def main():
    # 检查命令行参数是不是2个 (例如: python server.py 51234)
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])

    # 创建一个 TCP Socket (买个手机)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定端口 (插上电话卡)
    server_socket.bind(('', port))
    # 开始监听 (开机等电话)
    server_socket.listen(5)
    print(f"Server is listening on port {port}...")

    # 目前先只接听一个电话用来测试
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")

    # 测试完毕，挂断电话
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()