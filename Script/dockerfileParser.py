import re


def get_base_image_from_dockerfile(file_path):
    """
    从Dockerfile文件中获取base image，并返回其名称。

    Args:
        file_path (str): Dockerfile文件的本地路径。

    Returns:
        str: base image的名称，如果未找到则返回空字符串。
    """
    # 从本地文件读取Dockerfile内容
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()

    # 解析Dockerfile文件并获取base image
    match = re.search(r'^FROM\s+(.*)\s*', data, flags=re.MULTILINE)
    if match:
        base_image = match.group(1)
    else:
        base_image = ''

    return base_image


if __name__ == '__main__':
    print(get_base_image_from_dockerfile("./Dockerfile"))