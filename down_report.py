# -*- coding:UTF-8 -*-
import os
import sys
from flask import Flask, send_from_directory, render_template, request, jsonify
from report_doc.report_core import get_report_core
from report_doc.report_core_test import get_children
from jy_word.File import File
from config import base_dir, patient_info
reload(sys)
sys.setdefaultencoding('utf-8')
out_file = 'TCRseq_results.xlsx'
dir_name = base_dir
result_dir = os.path.join(dir_name, 'results')
template_folder = os.path.join(dir_name, 'templates')
print base_dir

app = Flask(__name__, template_folder=template_folder)
my_file = File(base_dir)


@app.route('/upload/', methods=['POST'])
def upload():
    print request.data
    print request.json
    return jsonify({'upload': 'dsfg'})


@app.route('/upload_file/')
def render_html():
    return render_template('upload_file.html')


@app.route('/')
def download_docx():
    user_name = patient_info['name']
    file_name = u'results/%s检测报告.doc' % user_name
    print u'%s begin.' % file_name
    data = {'patient_info': patient_info}
    pkg = get_report_core(report_title_cn, report_title_en, data)
    my_file.download(pkg, file_name)
    dict_url = os.path.join(dir_name, file_name.split('/')[0])
    print u'%s over.' % file_name
    return send_from_directory(dict_url, file_name.split('/')[1], as_attachment=True)


@app.route('/children/')
def download_children():
    report_title = '晶苗儿童基因检测'
    file_name = u'%s.doc' % report_title
    print u'%s begin.' % file_name
    data = my_file.read('children/children.json')
    # print data.keys()
    pkg = get_children(report_title, data)
    my_file.download(pkg, os.path.join('results', file_name))
    dict_url = os.path.join(dir_name, 'results')
    print u'%s over.' % file_name
    return send_from_directory(dict_url, file_name, as_attachment=True)


if __name__ == '__main__':
    report_title_cn = u'多组学临床检测报告'
    report_title_en = 'AIomics1'
    port = 1234
    # print 'http://127.0.0.1:%d/upload_file/' % port
    print 'http://127.0.0.1:%d/children/' % port
    app.run(port=port, debug=False)
