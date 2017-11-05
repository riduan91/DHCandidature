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
import argparse
import makeZip

API_KEY = '521350-1405134815-au8cmd567qxfnrb49'
FORM_ID = {
    "fr": "1006311",
    "sg": "2266863",
    "tw": "2272966"
}

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
ZIP_SOURCE_FOLDER = "../Docs/"
ZIP_DESTINATION_FOLDER = "../Docsreduce/ZIPPER/"
REDUCED_TARGET = '../Docsreduce/'

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

def simply_prepare(path):
        if (not(os.path.exists(path))):
            print 'Đang tạo thư mục %s' % path
            os.mkdir(path)

        if (not(os.path.exists(path + 'ZIPPER'))):
            print 'Đang tạo thư mục ZIPPER'
            os.mkdir(path + 'ZIPPER/')

def log_error(error_message):
    f = open("error_log.txt","w")
    f.write(error_message)
    f.close()

def run(candidates):
    print 'Tạo pdf tương ứng với từng bạn sinh viên và phân loại theo tên trường...'

    # create thread POOL w.r.t the number of available cpus
    pool = multiprocessing.Pool(POOL_SIZE)
    print 'Máy tính của bạn có %s cpu, Chương trình sẽ tạo %s threads' % (NB_CPUS, POOL_SIZE)

    # keep track of start time
    start_time = time.time()

    # assign pdf build tasks to pool
    heading_csv = makePdf.FIELD_NAMES
    task_args = [(TARGET, index, candidates[index], heading_csv) for index in range(len(candidates))]
    apply_objects = [pool.apply_async(makePdf.buildPdf, args) for args in task_args]

    # wait for execution end
    for r in apply_objects:
        try:
            pdfname = r.get()
            print 'File %s đã được tạo' % pdfname
        except Exception as e:
            print r
            print e
            #log_error(str(r))
            #log_error(str(e))

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

def zip():
	# keep track of start time
    start_time = time.time()

    for school_code in SCHOOL_CODE:
        makeZip.zip(ZIP_SOURCE_FOLDER + school_code, ZIP_DESTINATION_FOLDER + school_code)
        makeZip.zip(ZIP_SOURCE_FOLDER + "INTERVIEW/" + school_code, ZIP_DESTINATION_FOLDER + "_INTERVIEW_" + school_code )
    print 'Việc nén file được tiến hành trong %0.2f giây' % (time.time()-start_time)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    simply_prepare(REDUCED_TARGET)
    prepare(TARGET)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-f', '--form', dest='form', type=str, help='Choose form to get submissions. Available choice: fr, sg, tw. To get all submissions: -f all')

    args = parser.parse_args()
    if args.form == "all":
        for form in FORM_ID:
            print("Generate pdf for {}".format(form))
            candidates = getSubmissionsFromAPI(FORM_ID[form])
            run(candidates)
            print("Finished pdf generator for {}".format(form))
    if args.form in FORM_ID:
        form_id = FORM_ID[args.form]
        candidates = getSubmissionsFromAPI(form_id)
        run(candidates)
    else:
        print("Please choose a form to get submission. Available choice: fr, sg, tw")
        sys.exit(1)

    zip()

    print("done")
