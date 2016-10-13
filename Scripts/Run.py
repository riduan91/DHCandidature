# !/user/local/bin/python2.7
# -*- coding: utf-8 -*-
# Main App


import sys                  # for getting command line arguments
import multiprocessing      # for parallel tasks
import time                 # for time measurement
import makePdf              # for building pdf
import os                   # for os commands
import urllib2              # for dealing with url, proxy
import makeZip              # for file compression
#import upload_google_drive  # for uploading to google drive
import csv                  # for csv form

# Abbreviations for universities' names
SCHOOL_CODE = [
    'BKHN', 'TNHN', 'XD', 'GTVT1', 'CNHN',
    'VINH', 'BKDN', 'KTDN','SPDN', 
    'NNDN', 'BKHCM', 'TNHCM', 'KTLHCM',
    'GTVT2', 'DALAT', 'CTHO', 'KHAC'
]

ZIP_SOURCE_FOLDER = "../Docs/"
ZIP_DESTINATION_FOLDER = "../Docsreduce/ZIPPER/"


# Specifies the .csv name and where to store pdfs
TARGET = '../Docs/'
UPLOAD_FOLDER = 'DH 2014'
REDUCED_TARGET = '../Docsreduce/'

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

    # back to the path's folder

# Prepare tasks for building and classifying pdfs
# Arguments(0):
def run():
    print 'Tạo pdf tương ứng với từng bạn sinh viên và phân loại theo tên trường...'

    # create thread POOL w.r.t the number of available cpus
    pool = multiprocessing.Pool(POOL_SIZE)
    print 'Máy tính của bạn có %s cpu, Chương trình sẽ tạo %s threads' % (NB_CPUS, POOL_SIZE)
    
    # keep track of start time
    start_time = time.time()
    
    # assign pdf build tasks to pool
    heading_csv = CANDIDATE_LIST[0]
    index_range = range(START_INDEX, END_INDEX)
    task_args = [(TARGET, index, CANDIDATE_LIST[index], heading_csv) for index in index_range]
    apply_objects = [pool.apply_async(makePdf.buildPdf, args) for args in task_args]

    # wait for execution end
    for r in apply_objects:
        pdfname = r.get()
        print 'File %s đã được tạo' % pdfname

    pool.close()
    pool.join()
    
    try:
        os.rmdir(TARGET+'tmp')
    except OSError:
        pass
		
    print 'Việc tạo pdf được tiến hành trong %0.2f giây' % (time.time()-start_time)
		
def zip():
	# keep track of start time
    start_time = time.time()
	
    for school_code in SCHOOL_CODE:
        makeZip.zip(ZIP_SOURCE_FOLDER + school_code, ZIP_DESTINATION_FOLDER + school_code)
        makeZip.zip(ZIP_SOURCE_FOLDER + "INTERVIEW/" + school_code, ZIP_DESTINATION_FOLDER + "_INTERVIEW_" + school_code )    
    print 'Việc nén file được tiến hành trong %0.2f giây' % (time.time()-start_time)
    

# Prepare tasks for sending pdfs to candidates and upload them to Google Drive
# Arguments(0)

# Read and convert content in csv format into python list
# Arguments(1):
#   - filename: the file to read
def transformCSVToList(filename):
    with open(os.path.abspath(filename), 'rU') as f:
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter = ','))
        f.close()
    return data

# entry point (main function)
# the next two lines are needed for Windows compatibility when cloning a process
# freeze_support() must be right after if __name__...
if __name__ == '__main__':
    multiprocessing.freeze_support()

    # init
    prepare(TARGET)
    simply_prepare(REDUCED_TARGET)

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

    # Make docs
    run()
    zip()
    # Chỉ thực hiện stepTwo() một lần duy nhất sau khi nhận được tất cả hồ sơ
    # stepTwo()

