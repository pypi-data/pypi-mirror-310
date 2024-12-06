import json
import subprocess
from functools import partial  # 锁定参数

# 防止乱码
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs


# 读取javascript 代码，执行js代码并返回 结果
def js_read(file_or_code: str = None, code: str = None, encoding="utf-8"):
    """
    读取并编译 JavaScript 代码。

    :param file_or_code: str, JavaScript 文件路径或代码内容。
                         - 如果是路径，则读取该文件的内容。
                         - 如果是代码内容，则直接使用。
    :param code: str, 可选参数。需要添加在文件开头的 JavaScript 代码。
                 示例: code = "var a = 10;"
    :param encoding: str, 文件编码格式，默认为 "utf-8"。
    :return: execjs 编译后的 JavaScript 对象。
    """
    # 判断参数是否为空
    if not file_or_code and not code:
        raise ValueError("参数 `file_or_code` 和 `code` 至少需要提供一个。")
    # 判断是否需要为 code 添加分号和换行符
    if code and not code.endswith(';'):
        code += ';'  # 如果没有分号，则添加
    try:
        # 判断第一个参数是文件路径还是代码内容
        if file_or_code and file_or_code.endswith('.js'):
            # 如果是路径，读取文件内容
            with open(file_or_code, mode="r", encoding=encoding) as f:
                file_content = f.read()
            js_code = (code + '\n' + file_content) if code else file_content
        else:
            # 如果第一个参数是代码内容，直接使用
            js_code = (code + '\n' + file_or_code) if code else file_or_code

    except Exception as e:
        raise RuntimeError(f"无法读取文件或处理 JavaScript 代码: {e}") from e

    # 编译 JavaScript 代码
    return execjs.compile(js_code)


# 在控制台执行 js 代码 拿到控制台打印js结果 返回列表
def js_run(file: str, *args, split=None, encoding="utf-8"):
    """
    使用 Python 调用 Node.js 执行 JavaScript 文件，并返回控制台输出的结果。
    :Python 调用 js_run(js文件绝对路径,1,"1",[1,"2"],{k:1})
                js_run(js文件绝对路径,[1,"1",[1,"2"],{k:1}])
        也可以传入单个参数 数字 字符串 列表 字典 在Node.js 里直接收到的都是 JSON 字符串
    :Node.js 接收参数 var arr = process.argv.slice(2); arr 是 JSON 字符串
        把字符串 转为 JSON 格式 然后在 Node.js 里使用
        arr = JSON.parse(arr[0]); 转为 Node.js JSON 数组
    :param file: str
        需要执行的 Node.js 文件的绝对路径。
    :param args: tuple
        传递给 Node.js 文件的参数，支持字符串、数字、字典、列表等。
    :param split: str, optional
        用于分割输出的分隔符，默认为换行符 `'\n'`。
    :param encoding: str, optional
        Node.js 输出的编码格式，默认为 "utf-8"。
    :return: str 或 list
        返回分割后的段落列表。
    """
    # 验证 file 是否为 .js 文件
    if not file.endswith('.js'):
        raise ValueError("参数 `file` 必须是 JavaScript 文件路径。")

    # 构造 Node.js 命令
    cmd = ['node', file]
    if args:
        cmd.append(json.dumps(args, separators=(",", ":")))

    # 执行命令并捕获输出
    result = subprocess.run(cmd, capture_output=True, text=True, encoding=encoding)
    stdout = result.stdout.strip().splitlines()

    # 如果没有提供分隔符，返回按行分割的列表
    # 如果提供了分隔符，先将所有行合并为一个字符串，再按照分隔符拆分
    return stdout if split is None else "".join(stdout).split(split)
