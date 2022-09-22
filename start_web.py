#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from flask import Flask

app = Flask(__name__)

import time
import logging

from flask import Flask, request, render_template
from flask_cors import CORS

from src.tools import Trie, clean_space
from config.config import semantic_search_url

logger = logging
app = Flask(__name__,template_folder='templates',static_folder='static')
CORS(app, supports_credentials=True)
app.secret_key = '1234567'

trie = Trie()

@app.route('/search', methods=['GET','POST'])
def search():
    """
    前端调用接口
        路径：/ai
        请求方式：GET、POST
        请求参数：question
    :return: response rasa响应数据
    """

    if request.method == 'POST':
        b0 = time.time()
        question = request.args["key"]
        if not question.strip():
            return render_template("index.html")
        answer = requests.post(semantic_search_url, data=json.dumps({'msg':question}))
        ret = {'response': []}
        # answer替换response中的内容
        for item in answer.json()['answer']:
            ret['response'].append({"name":item['title'], "abstract": item['para']})
        logger.info('total costs {:.2f}s'.format(time.time() - b0))
        # answer = str({"response":answer,"intent":{"name":intent_name, "confidence":intent_confidence}, "entities":entities, "faq_match":faq_dict})
        return ret

    return render_template("index.html")

@app.route('/suggest', methods=['POST'])
def suggest():
    key = request.args['key']
    if key == '':
        return {'suggestions': []}

    terms = []
    res = trie.get_start(clean_space(key))
    for i in res:
        terms.append({"term": i})
    return {'suggestions': terms}

if __name__ == '__main__':
    # 启动服务，开启多线程模式
    app.run(
        host='0.0.0.0',
        port=8082,
        threaded=True,
        debug=False
    )
