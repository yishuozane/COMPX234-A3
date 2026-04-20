import socket
import sys


def main():
    # 检查命令行参数是不是4个 (例如: python client.py localhost 51234 client_1.txt)
    if len(sys.argv) != 4:
        print("Usage: python client.py <hostname> <port> <filename>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    # 创建一个 TCP Socket (买个手机)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 拨号连接服务器
        client_socket.connect((hostname, port))
        print(f"Successfully connected to {hostname} on port {port}")
        print(f"Ready to process file: {filename}")

        # 测试完毕，挂断电话
        client_socket.close()
    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")


if __name__ == "__main__":
    main()