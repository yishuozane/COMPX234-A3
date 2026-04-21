import socket
import sys
import threading


# --- 新增：专门接待单个客户端的“接线员”函数 ---
def handle_client(client_socket, addr):
    print(f"Accepted connection from {addr}")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break  # 客户端断开或发完了

            request_msg = data.decode('utf-8')

            # 为了防止一会儿多个客户端同时连进来屏幕太乱，我们暂时不把收到的具体内容打印出来了
            # 假装处理了一下，随便回一句符合协议格式的话
            dummy_response = "019 OK (dummy) read"
            client_socket.sendall(dummy_response.encode('utf-8'))

        except ConnectionResetError:
            break  # 客户端非正常强退时保护服务器不崩溃

    print(f"Connection closed by {addr}")
    client_socket.close()


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

    # --- 修改：主线程的死循环，专门接客并分配线程 ---
    while True:
        try:
            client_socket, addr = server_socket.accept()
            # 关键一步：创建一个新线程，目标是 handle_client 函数，并把客户端信息传给它
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()  # 启动线程！
        except KeyboardInterrupt:
            # 允许我们在终端按 Ctrl+C 优雅地关闭服务器
            print("\nServer shutting down...")
            break

    server_socket.close()


if __name__ == "__main__":
    main()