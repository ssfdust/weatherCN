from pathlib import Path

def cache_path(filename):
    """cache目录"""
    dirpath = Path.home().joinpath(".cache", "weatherCN")
    if not dirpath.exists():
        dirpath.mkdir(parents=True)

    return dirpath.joinpath(filename)


def txtlen(txt):
    """返回字符串长度"""
    _len = 0
    for ch in txt:
        if ord(ch) > 0x3000:
            _len += 2
        else:
            _len += 1
    return _len


def centertxt(txt, length=12):
    """居中字符串"""
    tlen = txtlen(txt)
    rlen = (length - tlen) // 2
    llen = length - rlen - tlen
    return " " * llen + txt + " " * rlen



