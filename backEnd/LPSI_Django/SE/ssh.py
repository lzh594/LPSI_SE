import ast

import paramiko
import base64


def set_SSH():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.192.98.141', port=22, username='skd', password='lzh142857')
    return ssh


def command_SSH(command):
    myssh = set_SSH()
    # 输入命令
    cmd = "source /etc/profile; cd /home/skd/Desktop/SE/cmake-build-debug; "
    cmd += command
    # 获取输出
    stdin, stdout, stderr = myssh.exec_command(cmd)
    # 格式处理
    out = stdout.read().replace(b' ', b'')[:-4]
    print("out:", out)
    # 查询操作
    result = b''  # 查询结果
    enc = {}  # 加密的结果（搜索的关键词及对应的标识）
    index = len(out) - 1

    # 解析结果
    while out[index:index + 1] != b'}':
        result = out[index:index + 1] + result
        index -= 1

    # 解析加密的结果
    enc_data = out.replace(result, b'').strip(b'{').strip(b'}').strip(b'\n').split(b'\n')
    print("enc_data", enc_data)
    for kw in enc_data:
        li = kw.split(b'":["')
        keyword = li[0].strip(b'\"')  # 提取出关键词
        inv = li[1].strip(b',],').split(b'\",\"')  # 提取出关键词对应的标识符列表
        inv_base = []

        # 进行base64编码
        keyword = base64.b64encode(keyword).decode('utf-8')
        for iv in inv:
            iv = base64.b64encode(iv).decode('utf-8')
            inv_base.append(iv)

        # 存入字典
        enc[keyword] = inv_base

    result = result.decode()
    result = ast.literal_eval(result)

    myssh.close()

    return enc, result


if __name__ == "__main__":
    command_SSH("")
