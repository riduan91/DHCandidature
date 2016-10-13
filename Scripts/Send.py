# !/user/local/bin/python2.7
# -*- coding: utf-8 -*-
# Main App


import sys                  # for getting command line arguments
import multiprocessing      # for parallel tasks
import time                 # for time measurement
#import make_pdf             # for building pdf
import os                   # for os commands
import urllib2              # for dealing with url, proxy
#import upload_google_drive  # for uploading to google drive
import mailSender           # for mail sending
import csv                  # for csv form

# Abbreviations for universities' names
SCHOOL_CODE = [
    'BKHN', 'TNHN', 'XD', 'GTVT1', 'CNHN',
    'VINH', 'BKDN', 'KTDN','SPDN', 
    'NNDN', 'BKHCM', 'TNHCM', 'KTLHCM',
    'GTVT2', 'DALAT', 'CTHO', 'KHAC'
]

SCHOOL_DICTIONARY = {
    'Trường Đại học Bách khoa Hà Nội' : 'BKHN',
    'Trường Đại học Khoa học tự nhiên, ĐHQG Hà Nội' : 'TNHN',
    'Trường Đại học Xây dựng' : 'XD',
    'Trường Đại học Giao thông vận tải cơ sở I (tại Hà Nội)' : 'GTVT1',
    'Trường Đại học Công nghệ, ĐHQG Hà Nội' : 'CNHN',
    'Trường Đại học Vinh' : 'VINH',
    'Trường Đại học Bách khoa, ĐH Đà Nẵng' : 'BKDN',
    'Trường Đại học Kinh tế, ĐH Đà Nẵng' : 'KTDN',
    'Trường Đại học Sư phạm, ĐH Đà Nẵng' : 'SPDN',
    'Trường Đại học Ngoại ngữ, ĐH Đà Nẵng' : 'NNDN',
    'Trường Đại học Bách khoa, ĐHQG TP Hồ Chí Minh' : 'BKHCM',
    'Trường Đại học Khoa học tự nhiên, ĐHQG TP Hồ Chí Minh' : 'TNHCM',
    'Trường Đại học Kinh tế Luật, ĐHQG TP Hồ Chí Minh' : 'KTLHCM',
    'Trường Đại học Giao thông vận tải cơ sở II (tại TP Hồ Chí Minh)' : 'GTVT2',
    'Trường Đại học Đà Lạt' : 'DALAT',
    'Trường Đại học Cần Thơ' : 'CTHO',
    'Trường khác (ghi rõ trong thư xin học bổng)' : 'KHAC',
}

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

    # back to the path's folder
	os.chdir('..')


# Prepare tasks for building and classifying pdfs
# Arguments(0):

# Prepare tasks for sending pdfs to candidates and upload them to Google Drive
# Arguments(0)
def send():
    print 'Gửi pdf đến các bạn sinh viên...'
 
    os.chdir(TARGET)

    # create thread POOL w.r.t the number of available cpus
    pool = multiprocessing.Pool(POOL_SIZE)
    print 'Máy tính của bạn có %s cpu, Chương trình sẽ tạo %s threads' % (NB_CPUS, POOL_SIZE)
    
    # keep track of start time
    start_time = time.time()
    
    # First, we send back pdfs to candidates
    # open a smtp server to send gmail
    mail_server = mailsender.openMailServer()

    # assign sending task to pool
    index_range = range(START_INDEX, END_INDEX)
    task_args = [((SCHOOL_DICTIONARY[CANDIDATE_LIST[index][8]], make_pdf.buildPdfName(CANDIDATE_LIST[index], index), CANDIDATE_LIST[index][16])) for index in index_range]
    print task_args
    apply_objects = [pool.apply_async(mailsender.do, args) for args in task_args]

    for r in apply_objects:
        r.wait()
	
    pool.close()
    pool.join()
	
    print 'Bước 2 tiến hành trong %0.2f giây' % (time.time()-start_time)

# Read and convert content in csv format into python list
# Arguments(1):
#   - filename: the file to read
def transformCSVToList(filename):
    with open(os.path.abspath(filename), 'rU') as f:
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter = ','))
        f.close()
    return data

# Specifies the .csv name and where to store pdfs
TARGET = '../Docs/'
UPLOAD_FOLDER = 'DH 2014'

# Constants
START_INDEX = 1
END_INDEX = 91
CANDIDATE_LIST = []

# Specifies proxies that this app may bypass
PROXIES = {'http':'pcyvipncp2n.edf.fr:3128'}
HAS_PROXY = False

# Determine pool size
NB_CPUS = multiprocessing.cpu_count()
print "nb_cpus", NB_CPUS
POOL_SIZE = (NB_CPUS-1)*2
if (POOL_SIZE==0):
	POOL_SIZE = 2

# entry point (main function)
# the next two lines are needed for Windows compatibility when cloning a process
# freeze_support() must be right after if __name__...
if __name__ == '__main__':
    multiprocessing.freeze_support()

    # init
    prepare(TARGET)

    # Transform our csv table into a list of lists of strings. Each list of strings is called a "candidate".
    CANDIDATE_LIST = transformCSVToList(sys.argv[1])
    nb_candidates = len(CANDIDATE_LIST)
    print 'Có %s sinh viên trong danh sách' % nb_candidates

    # check for start and end index arguments
    if len(sys.argv) == 4:
        START_INDEX = int(sys.argv[2])
        END_INDEX = int(sys.argv[3])

        if (END_INDEX - START_INDEX <= 0 or int(START_INDEX) == 0):
            print 'Vui lòng nhập lại chỉ số bắt đầu và kết thúc!!!!'
            sys.exit(0)

    # Chỉ thực hiện stepTwo() một lần duy nhất sau khi nhận được tất cả hồ sơ
    send()
