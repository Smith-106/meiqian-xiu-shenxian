# -*- coding: utf-8 -*-
r"""把流水线脚本里的 Windows 绝对路径改成本克隆的实际路径。

这些脚本是当时一次性写就的，路径全写死成 C:\Users\niko\storymoss_case\full_rewrite。
克隆到别的机器后跑一次本脚本即可：

    python patch_paths.py            # 先看会改什么（不落盘）
    python patch_paths.py --apply    # 真正改写，并做语法检查

只替换根路径前缀；指向数据库的两行会单独提示，需要手工确认。
"""
import sys
import io
import os
import re
import glob

HERE = os.path.dirname(os.path.abspath(__file__))          # writing/pipeline
ROOT = os.path.dirname(os.path.dirname(HERE))               # 仓库根
WRITING = os.path.join(ROOT, "writing")

OLD_ROOT = r"C:\Users\niko\storymoss_case"
OLD_PL = r"C:\Users\niko\storymoss_case\full_rewrite"
OLD_TMP = r"C:\Users\niko\AppData\Local\Temp"

# 转义形式（脚本里 u"C:\\Users\\..." 那种写法）也要覆盖
PAIRS = [
    (OLD_PL.replace("\\", "\\\\"), HERE.replace("\\", "\\\\")),
    (OLD_PL, HERE),
    (OLD_ROOT.replace("\\", "\\\\"), ROOT.replace("\\", "\\\\")),
    (OLD_ROOT, ROOT),
    (OLD_TMP.replace("\\", "\\\\"), WRITING.replace("\\", "\\\\")),
    (OLD_TMP, WRITING),
]

DB_MARKERS = ("AppData\\Roaming\\com.storymoss.app", "AppData\\\\Roaming\\\\com.storymoss.app")


_MAP = dict(PAIRS)
# 单次扫描：避免 A→B 之后 B 又被后续规则命中
_PAT = re.compile("|".join(re.escape(k) for k in sorted(_MAP, key=len, reverse=True)))


def patch_text(t):
    n = [0]

    def sub(m):
        n[0] += 1
        return _MAP[m.group(0)]

    return _PAT.sub(sub, t), n[0]


def main(argv):
    apply = "--apply" in argv
    files = sorted(glob.glob(os.path.join(HERE, "*.py")))
    files = [f for f in files if os.path.basename(f) != "patch_paths.py"]
    total = 0
    changed = []
    for f in files:
        t = io.open(f, encoding="utf-8").read()
        nt, n = patch_text(t)
        if n:
            changed.append((os.path.basename(f), n))
            total += n
            if apply:
                io.open(f, "w", encoding="utf-8", newline="\n").write(nt)

    print(u"目标根目录：%s" % ROOT)
    print(u"流水线目录：%s" % HERE)
    print()
    for name, n in changed:
        print(u"  %-22s 替换 %d 处" % (name, n))
    print(u"\n共 %d 个文件，%d 处替换%s" % (
        len(changed), total, u"（已写入）" if apply else u"（预演，加 --apply 才落盘）"))

    # 仍存在的绝对路径提示
    left = []
    for f in files:
        for i, line in enumerate(io.open(f, encoding="utf-8").read().split("\n"), 1):
            if any(m in line for m in DB_MARKERS):
                left.append((os.path.basename(f), i, line.strip()))
    if left:
        print(u"\n需要手工确认的数据库路径：")
        for name, i, line in left:
            print(u"  %s:%d  %s" % (name, i, line))

    if apply:
        bad = []
        for f in files:
            try:
                compile(io.open(f, encoding="utf-8").read(), f, "exec")
            except SyntaxError as e:
                bad.append((os.path.basename(f), "%s (line %s)" % (e.msg, e.lineno)))
        print(u"\n语法检查：%s" % (u"全部通过" if not bad else u"%d 个失败" % len(bad)))
        for name, msg in bad:
            print(u"  %s  %s" % (name, msg))
        return 0 if not bad else 1
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main(sys.argv))
