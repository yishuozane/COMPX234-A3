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

        # --- 新增：读取并解析任务清单 ---
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()  # 去掉每行前后的换行符和空格
                    if not line:
                        continue  # 跳过空行

                    # 把一行指令拆开。因为 PUT 命令的 value 里可能包含空格，所以我们最多只拆分2次
                    # 例如: "PUT my-key this is a long value" -> ["PUT", "my-key", "this is a long value"]
                    parts = line.split(' ', 2)
                    command = parts[0]
                    key = parts[1] if len(parts) > 1 else ""
                    value = parts[2] if len(parts) > 2 else ""

                    # 检查作业要求的长度限制：k 和 v 的组合长度不能超过 970
                    kv_string = f"{key} {value}".strip()
                    if len(kv_string) > 970:
                        print(f"Error: Key and value too long, ignoring: {line}")
                        continue

                    # 1. 把命令缩写成一个字母 (P, R, 或 G)
                    cmd_char = command[0]

                    # 2. 拼装后面的内容
                    if cmd_char == 'P':
                        payload = f"{cmd_char} {key} {value}"
                    else:
                        payload = f"{cmd_char} {key}"

                    # 3. 计算总长度。"NNN " 占 4 个字符，所以总长度是 payload 长度 + 4
                    total_length = len(payload) + 4

                    # 4. 组装最终暗号，03d 表示用0填补到3位数
                    message = f"{total_length:03d} {payload}"

                    # 5. 发送给服务器 (需要转换成 bytes)
                    client_socket.sendall(message.encode('utf-8'))
                    print(f"Client Sent: {message}")

                    # 6. 必须等待服务器的回复才能继续下一条！(同步行为)
                    response = client_socket.recv(1024).decode('utf-8')
                    if not response:
                        break  # 服务器断开了
                    print(f"Client Received: {response}")

        except FileNotFoundError:
            print(f"Error: File {filename} not found.")

        # 测试完毕，挂断电话
        client_socket.close()
    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")


if __name__ == "__main__":
    main()