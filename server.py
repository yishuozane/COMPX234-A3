import socket
import sys
import threading

# --- 新增：核心数据结构 (Tuple Space) 和 互斥锁 ---
tuple_space = {}  # 我们的共享大字典
space_lock = threading.Lock()  # 保护字典的锁，防止并发冲突


# --- 新增：专门接待单个客户端的“接线员”函数 ---
def handle_client(client_socket, addr):
    print(f"Accepted connection from {addr}")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break  # 客户端断开或发完了

            request_msg = data.decode('utf-8')

            # --- 新增：解析暗号并执行真实的 PUT/READ/GET 操作 ---
            # 客户端发来的格式例如: "023 P apple is a red fruit"
            # 我们最多把它切成4份: ["023", "P", "apple", "is a red fruit"]
            parts = request_msg.split(' ', 3)
            if len(parts) < 3:
                continue  # 格式不对就忽略

            cmd = parts[1]
            key = parts[2]
            val = parts[3] if len(parts) > 3 else ""

            response_str = ""

            # 【重点来了】：进入金库前先上锁！
            with space_lock:
                if cmd == 'P':  # PUT 操作
                    if key in tuple_space:
                        response_str = f"ERR {key} already exists"
                    else:
                        tuple_space[key] = val
                        response_str = f"OK ({key}, {val}) added"

                elif cmd == 'R':  # READ 操作
                    if key in tuple_space:
                        response_str = f"OK ({key}, {tuple_space[key]}) read"
                    else:
                        response_str = f"ERR {key} does not exist"

                elif cmd == 'G':  # GET 操作 (读完还要删掉)
                    if key in tuple_space:
                        fetched_val = tuple_space.pop(key)  # pop能同时完成“拿出”和“删除”
                        response_str = f"OK ({key}, {fetched_val}) removed"
                    else:
                        response_str = f"ERR {key} does not exist"
            # (代码运行到这里退出了 with 缩进，锁会自动解开)

            # 把服务器的回复按照 "NNN 回复内容" 的格式打包发回去
            total_length = len(response_str) + 4
            final_msg = f"{total_length:03d} {response_str}"
            client_socket.sendall(final_msg.encode('utf-8'))
            # ------------------------------------------------

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