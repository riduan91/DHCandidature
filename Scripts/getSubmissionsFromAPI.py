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
import logging
from fixtures import *

logger = logging.getLogger(__name__)

API_KEY = '521350-1405134815-au8cmd567qxfnrb49'
FORM_ID = {
	"fr": "1006311",
	"sg": "2266863",
	"tw": "2272966"
}

URL_SUBMISSION_FORMAT = "https://123contactform.com/api/forms/{}/submissions.json"
URL_SUBMISSION_COUNT_FORMAT = "https://www.123contactform.com/api/forms/{}/submissions/count.json?apiKey={}"

PAGE_SIZE = 50

# Specifies the .csv name and where to store pdfs
TARGET = '../Docs_{}/'.format(CURRENT_SEMESTER)

# Determine pool size
NB_CPUS = multiprocessing.cpu_count()
logger.info("nb_cpus", NB_CPUS)
POOL_SIZE = (NB_CPUS-1)*2
if (POOL_SIZE==0):
		POOL_SIZE = 2

# Check if target folders exist and create them if necessary
# Arguments(1):
#   - path: the path of target
def prepare(path):
	if (not(os.path.exists(path))):
		logger.info('Đang tạo thư mục %s' % path)
		os.mkdir(path)

	os.chdir(path)
	if not(os.path.exists('tmp')):
		logger.info('Đang tạo thư mục tmp')
		os.mkdir('tmp')

	for code in SCHOOL_CODE.values():
		if (not(os.path.exists(code))):
			logger.info('Đang tạo thư mục %s' % code)
			os.mkdir(code)
			if (not(os.path.exists(code + '/DISQUALIFIED'))):
				os.mkdir(code + '/DISQUALIFIED')

		if (not(os.path.exists('INTERVIEW'))):
			logger.info('Đang tạo thư mục INTERVIEW')
			os.mkdir('INTERVIEW')

		for code in SCHOOL_CODE.values():
			if (not(os.path.exists('INTERVIEW/' + code))):
				logger.info('Đang tạo thư mục INTERVIEW/%s' % code)
				os.mkdir('INTERVIEW/' + code)


def run(candidates):
	logger.info('Tạo pdf tương ứng với từng bạn sinh viên và phân loại theo tên trường...')

	# create thread POOL w.r.t the number of available cpus
	pool = multiprocessing.Pool(POOL_SIZE)
	logger.info('Máy tính của bạn có %s cpu, Chương trình sẽ tạo %s threads' % (NB_CPUS, POOL_SIZE))

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
			logger.info('File %s đã được tạo' % pdfname)
		except Exception as e:
			logger.error(e)

	pool.close()
	pool.join()

	try:
		os.rmdir(TARGET+'tmp')
	except OSError as e:
		logger.error(e)

	logger.info('Việc tạo pdf được tiến hành trong %0.2f giây' % (time.time()-start_time))


def getSubmissionCount(form_id):
	url = URL_SUBMISSION_COUNT_FORMAT.format(form_id, API_KEY)
	data = {
		'apiKey': API_KEY
	}
	response = requests.get(url)
	res_obj = json.loads(response.content)
	logger.info(res_obj)
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
	return candidates

if __name__ == '__main__':
	logger.setLevel(logging.DEBUG)
	FORMAT = '[%(asctime)-15s] %(levelname)-6s %(message)s'
	DATE_FORMAT = '%d/%b/%Y %H:%M:%S'
	formatter = logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)
	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	handler.setLevel(logging.DEBUG)
	logger.addHandler(handler)

	file_handler = logging.FileHandler("error.log")
	file_handler.setFormatter(formatter)
	file_handler.setLevel(logging.ERROR)
	logger.addHandler(file_handler)


	multiprocessing.freeze_support()
	prepare(TARGET)

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-f', '--form', dest='form', type=str, help='Choose form to get submissions. Available choice: fr, sg, tw. To get all submissions: -f all')

	args = parser.parse_args()
	if args.form == "all":
		for form in FORM_ID:
			logger.info("Generate pdf for {}".format(form))
			candidates = getSubmissionsFromAPI(FORM_ID[form])
			run(candidates)
			logger.info("Finished pdf generator for {}".format(form))
	elif args.form in FORM_ID:
		form_id = FORM_ID[args.form]
		candidates = getSubmissionsFromAPI(form_id)
		run(candidates)
	else:
		logger.info("Please choose a form to get submission. Available choice: fr, sg, tw")
		sys.exit(1)

	logger.info("done")
