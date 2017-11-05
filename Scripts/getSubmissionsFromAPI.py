# !/user/local/bin/python2.7
# -*- coding: utf-8 -*-

import requests
import simplejson as json
import sys                  # for getting command line arguments
import multiprocessing      # for parallel tasks
import time                 # for time measurement
import makePdf              # for building pdf
import os                   # for os commands
import urllib2              # for dealing with url, proxy

API_KEY = '521350-1405134815-au8cmd567qxfnrb49'
FORM_DH_FRANCE_ID = "1006311"

URL_SUBMISSION_FORMAT = "https://123contactform.com/api/forms/{}/submissions.json"
URL_SUBMISSION_COUNT_FORMAT = "https://www.123contactform.com/api/forms/{}/submissions/count.json"

PAGE_SIZE = 50

SCHOOL_CODE = [
    'BKHN', 'TNHN', 'XD', 'GTVT1', 'CNHN',
    'VINH', 'BKDN', 'KTDN','SPDN',
    'NNDN', 'BKHCM', 'TNHCM', 'KTLHCM',
    'GTVT2', 'DALAT', 'CTHO', 'SPKTHCM', 'KHAC'
]

# Specifies the .csv name and where to store pdfs
TARGET = '../Docs/'
UPLOAD_FOLDER = 'DH 2014'
REDUCED_TARGET = '../Docsreduce/'

CANDIDATE_LIST = []

# Determine pool size
NB_CPUS = multiprocessing.cpu_count()
print "nb_cpus", NB_CPUS
POOL_SIZE = (NB_CPUS-1)*2
if (POOL_SIZE==0):
        POOL_SIZE = 2

# Check if target folders exist and create them if necessary
# Arguments(1):
#   - path: the path of target
def prepare(path):
	if (not(os.path.exists(path))):
	    print 'Đang tạo thư mục %s' % path
	    os.mkdir(path)

	os.chdir(path)
	if (not(os.path.exists('tmp'))):
	    print 'Đang tạo thư mục tmp'
	    os.mkdir('tmp')

	for code in SCHOOL_CODE:
	    if (not(os.path.exists(code))):
		print 'Đang tạo thư mục %s' % code
		os.mkdir(code)

        if (not(os.path.exists('INTERVIEW'))):
            print 'Đang tạo thư mục INTERVIEW'
            os.mkdir('INTERVIEW')

        for code in SCHOOL_CODE:
            if (not(os.path.exists('INTERVIEW/' + code))):
                print 'Đang tạo thư mục INTERVIEW/%s' % code
                os.mkdir('INTERVIEW/' + code)
def run():
    print 'Tạo pdf tương ứng với từng bạn sinh viên và phân loại theo tên trường...'

    # create thread POOL w.r.t the number of available cpus
    pool = multiprocessing.Pool(POOL_SIZE)
    print 'Máy tính của bạn có %s cpu, Chương trình sẽ tạo %s threads' % (NB_CPUS, POOL_SIZE)

    # keep track of start time
    start_time = time.time()

    # assign pdf build tasks to pool
    heading_csv = makePdf.FIELD_NAMES
    task_args = [(TARGET, index, CANDIDATE_LIST[index], heading_csv) for index in range(len(CANDIDATE_LIST))]
    apply_objects = [pool.apply_async(makePdf.buildPdf, args) for args in task_args]

    # wait for execution end
    for r in apply_objects:
        try:
            pdfname = r.get()
            print 'File %s đã được tạo' % pdfname
        except Exception as e:
            print e

    pool.close()
    pool.join()

    try:
        os.rmdir(TARGET+'tmp')
    except OSError:
        pass

    print 'Việc tạo pdf được tiến hành trong %0.2f giây' % (time.time()-start_time)


def getSubmissionCount(form_id):
    url = URL_SUBMISSION_COUNT_FORMAT.format(form_id)
    data = {
        'apiKey' : API_KEY
    }
    response = requests.post(url, data=data)
    res_obj = json.loads(response.content)
    print res_obj['submissionsCount']
    return int(res_obj['submissionsCount'])

def getSubmissionsFromAPI(form_id):
    candidates = []
    url = URL_SUBMISSION_FORMAT.format(form_id)
    count = getSubmissionCount(form_id)
    data = {
        'apiKey' : API_KEY,
        'pageSize': PAGE_SIZE,
        'sort': "ASC" #sort oldest to newest
    }
    num_page = count/PAGE_SIZE + 1
    for i in range(num_page):
        data['pageNr'] = i
        response = requests.post(url, data=data)
        res_dict = json.loads(response.content.encode('utf-8'))
        for candidate in res_dict['submissions']:
            candidate_string_list = []
            for field in candidate['fields']:
                candidate_string_list += [field['fieldvalue'].encode('utf-8')]
            candidates += [candidate_string_list]
    # print(candidates[0])
    return candidates



if __name__ == '__main__':
    CANDIDATE_LIST = getSubmissionsFromAPI(FORM_DH_FRANCE_ID)
    multiprocessing.freeze_support()

    # init
    prepare(TARGET)
    run()
    print("done")
