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

                    # 先打印出来看看我们解析得对不对
                    print(f"Parsed -> Command: {command}, Key: {key}, Value: {value}")

                    # (下一阶段骤我们将在这里把指令打包成 NNN 格式发给服务器)

        except FileNotFoundError:
            print(f"Error: File {filename} not found.")

        # 测试完毕，挂断电话
        client_socket.close()
    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")


if __name__ == "__main__":
    main()