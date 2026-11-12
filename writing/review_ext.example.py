# -*- coding: utf-8 -*-
u"""外部评审接口配置模板。

review_sample.py / judge.py 通过 `import review_ext as R` 读取 R.URL 与 R.KEY。
真实文件含 API 密钥，不入库。使用时复制本文件为 review_ext.py 并填入自己的值：

    copy review_ext.example.py review_ext.py

URL 需为 OpenAI 兼容的 chat/completions 端点。
"""

KEY = "sk-REPLACE-WITH-YOUR-KEY"
URL = "https://your-gateway.example.com/v1/chat/completions"

# review_sample.py 会在 user 消息开头强制直答，避免模型输出思考过程
FORCE = u"不要思考，直接输出最终答案JSON："
