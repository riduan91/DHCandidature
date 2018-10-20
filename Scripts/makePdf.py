# !/user/local/bin/python2.7
# -*- coding: utf-8 -*-

############### ----------IMPORT---------- ###############

# Import some important files from reportlab
import reportlab.rl_config
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import Image as Flowable_Image
import logging
import traceback
from PyPDF2.utils import PdfReadError
from PIL import Image
from fixtures import *

logger = logging.getLogger(__name__)
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

reportlab.rl_config.warnOnMissingFontGlyphs = 0

logodir = '../Resources/Images/'
# Determine where to find fonts w.r.t OS
UVN_SRC = '../Resources/Fonts/cambria.ttc'
UVNB_SRC = '../Resources/Fonts/cambriab.ttf'
UVNI_SRC = '../Resources/Fonts/cambriai.ttf'
UVNZ_SRC = '../Resources/Fonts/cambriaz.ttf'

# Import the font 'CAMBRIA' to display Vietnamese
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('UVN', UVN_SRC))
pdfmetrics.registerFont(TTFont('UVNB', UVNB_SRC))
pdfmetrics.registerFont(TTFont('UVNI', UVNI_SRC))
pdfmetrics.registerFont(TTFont('UVNZ', UVNZ_SRC))
pdfmetrics.registerFontFamily('Cambria', normal='UVN', bold='UVNB', italic='UVNI', boldItalic='UVNZ')

import urllib  # Import urllib to download files
import requests  # Another lib to download files
from PIL import Image as PIL_Image  # Import PIL to read image files
from PyPDF2 import PdfFileMerger, PdfFileReader  # Import pypdf2 to merge pdf file
import os  # for deleting temps
from PyPDF2 import PdfFileWriter

############### ----------END OF IMPORT---------- ###############


############### ----------PARAMETERS---------- ###############

# Page layout
LEFT_MARGIN = 50
RIGHT_MARGIN = 50
TOP_MARGIN = 50
BOTTOM_MARGIN = 50

CURRENT_SEMESTER = 34

# Line spacing
LINE_SPACING = 6

# A python dictionary to transform Vietnamese letters and accents into ASCII-letters.
REMOVE_ACCENT = {
    'a': 'a', 'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
    'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
    'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
    'e': 'e', 'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
    'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
    'i': 'i', 'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
    'o': 'o', 'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
    'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
    'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
    'u': 'u', 'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
    'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
    'y': 'y', 'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    'đ': 'd',
    'A': 'A', 'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
    'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
    'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
    'E': 'E', 'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
    'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
    'I': 'I', 'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
    'O': 'O', 'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
    'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
    'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
    'U': 'U', 'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
    'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
    'Y': 'Y', 'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
    'Đ': 'D',
    '\xcc\x80': '', '\xcc\x81': '', '\xcc\x89': '', '\xcc\x83': '', '\xbb\xa4': '',
    ' ': ' ',
}

# Icon for Yes/No questions: cross for "Yes", blank for "No"
# YES_NO_ICON = {'yes': "[ X ]", 'Yes': u"[ X ]", 'No': "[    ]", 'no': "[    ]", u'Có': "[ X ]", u'Không': "[    ]", u'có': "[ X ]", u'không': "[    ]", 'Không': "[    ]", 'Có': "[ X ]", 'Chưa từng': "[    ]", u'Chưa từng': "[     ]", '': "[     ]"}

YES_NO_ICON = {'yes': u"\u2327", 'Yes': u"\u2327", 'No': u"\u29e0", 'no': u"\u29e0", u'Có': u"\u2327",
               u'Không': u"\u29e0", u'có': u"\u2327", u'không': u"\u29e0", 'Không': u"\u29e0", 'Có': u"\u2327",
               'Chưa từng': u"\u29e0", u'Chưa từng': u"\u29e0", '': u"\u29e0"}

# Keys for all fields of the input csv
# The order of these fields must match exactly those in the input csb
# NB: For any insertion/deletion/change of positions of columns, please update this param
FIELD_NAMES = ['HoVaTen', 'GioiTinh', 'NgaySinh', 'MaSoSV', 'NamThu', 'KhoaNganh',
               'Lop', 'Truong', 'SoNhaDuongSinh', 'QuanHuyenSinh', 'TinhThanhSinh', 'SoNhaDuongTru',
               'QuanHuyenTru', 'TinhThanhTru', 'DienThoai', 'Email', 'HoTenCha', 'TuoiCha',
               'NgheNghiepCha', 'HoTenMe', 'TuoiMe', 'NgheNghiepMe', 'NguoiThan1', 'NguoiThan2',
               'NguoiThan3', 'NguoiThan4', 'NguoiThan5', 'NguoiThan6', 'NguoiThan7', 'NguoiThan8',
               'NguoiThan9', 'DiemDaiHoc', 'DiemKi1', 'DiemKi2', 'DiemKi3', 'DiemTotNghiep',
               'ThanhTichKhac1', 'ThanhTichKhac2', 'ThanhTichKhac3', 'ThanhTichKhac4', 'ThanhTichKhac5', 'THPT',
               'NhanHBDHChua', 'KiN-5', 'KiN-4', 'KiN-3', 'KiN-2', 'KiN-1',
               'CoHoTroKhac', 'HoTro1', 'HoTro2', 'HoTro3', 'HoTro4', 'HoTro5',
               'LamThem', 'HoatDongKhac', 'NhaO', 'DiLai', 'TienAn', 'TienHoc',
               'TienHocThem', 'VuiChoi', 'CacKhoanKhac', 'ThuNhapBinhQuan', 'ThuNhapGiaDinh', 'ThuNhapHocBong',
               'ThuNhapTienVay', 'ThuNhapLamThem', 'ThuNhapKhac', 'KhoKhanCuocSong', 'DongTienHocKhong',
               'DongTienHocBaoNhieu',
               'DongTienNhaKhong', 'DongTienNhaBaoNhieu', 'HocThemKhong', 'HocThemBaoNhieu', 'DongTienKhac',
               'MongMuonNhanGiTuDH',
               'KhoKhanLamHoSo', 'LienLacCachNao1', 'LienLacCachNao2', 'LienLacCachNao3', 'LienLacCachNao4',
               'DeDatNhanNhu',
               'HinhThucThu', 'KhungVietThu', 'KhungScanThu', 'BangDiemScan', 'ChungNhanKhoKhanScan', 'GiayToKhacScan',
               'GiayToKhacList', 'AnhCaNhan']

FIELD_NAMES_FULL = {'HoVaTen': 'Họ và tên', 'GioiTinh': 'Giới tính', 'NgaySinh': 'Ngày sinh',
                    'MaSoSV': 'Mã số sinh viên', 'NamThu': 'Sinh viên năm thứ', 'KhoaNganh': 'Khoa/Ngành',
                    'Lop': 'Lớp', 'Truong': 'Trường', 'DiaChiSinh': 'Địa chỉ hiện tại',
                    'DiaChiTru': 'Địa chỉ thường trú', 'DienThoai': 'Điện thoại', 'Email': 'Email',
                    'NhaO': 'Nhà ở', 'DiLai': 'Đi lại', 'TienAn': 'Tiền ăn', 'TienHoc': 'Tiền học chính khoá',
                    'TienHocThem': 'Tiền học thêm', 'VuiChoi': 'Vui chơi, giải trí', 'CacKhoanKhac': 'Các khoản khác',
                    'ThuNhapGiaDinh': 'Thu nhập gia đình', 'ThuNhapHocBong': 'Học bổng',
                    'ThuNhapTienVay': 'Tiền vay ngân hàng', 'ThuNhapLamThem': 'Thu nhập làm thêm',
                    'ThuNhapKhac': 'Thu nhập khác',
                    'DeDatNhanNhu': 'Bạn có đề đạt, nhắn gửi gì tới quỹ học bổng Đồng Hành ?',
                    'MongMuonNhanGiTuDH': 'Bạn mong muốn nhận được gì từ Đồng Hành ngoài việc giúp đỡ tài chính?',
                    'KhoKhanLamHoSo': 'Bạn gặp khó khăn gì trong quá trình làm hồ sơ xin học bổng Đồng Hành?'
                    }

# Get the index (position of column) of each fields
INDEX_OF_KEY = {}
for index in range(0, len(FIELD_NAMES)):
    INDEX_OF_KEY[FIELD_NAMES[index]] = index

# Some table styles
TRANSPARENT_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONT', (0, 0), (-1, -1), 'UVN'),
    ('FONT', (1, 0), (1, -1), 'UVNI'),
    ('FONT', (-1, 0), (-1, -1), 'UVNI'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
])
TRANSPARENT_TABLE_WITH_MERGE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONT', (0, 0), (-1, -1), 'UVN'),
    ('FONT', (1, 0), (1, -1), 'UVNI'),
    ('FONT', (-1, 0), (-1, -1), 'UVNI'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('SPAN', (-1, 0), (-1, -1)),
])
TRANSPARENT_REGULAR_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONT', (0, 0), (-1, -1), 'UVN'),
    ('FONT', (1, 0), (1, -1), 'UVN'),
    ('FONT', (-1, 0), (-1, -1), 'UVN'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
])
STANDARD_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ('FONT', (0, 0), (-1, 0), 'UVNB'),
    ('FONT', (0, 1), (0, -1), 'UVN'),
    ('FONT', (1, 1), (-1, -1), 'UVNI'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
])
HORIZONTAL_NUMERIC_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('ALIGN', (0, 1), (-1, -1), 'RIGHT'),
    ('FONT', (0, 0), (-1, 0), 'UVNB'),
    ('FONT', (0, 1), (-1, -1), 'UVN'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
])
VERTICAL_TRANSPARENT_NUMERIC_TABLE = TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
    ('FONT', (0, 0), (-1, -1), 'UVN'),
    ('FONT', (-1, 0), (-1, -1), 'UVNI'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
])


############### ----------END OF PARAMETERS---------- ###############

############### ----------LOCAL FUNCTIONS---------- ###############

def get(candidate, key, is_heading=False):
    """
        Usage: get(candidate, key, is_heading=False)
        This function returns the column "key" of the candidate "candidate"
        Params(3):
            candidate:      The csv row w.r.t a candidate
            key:            The field to get
            is_heading:     True if this is the heading row of the csv
    """

    if key == 'NgaySinh' and is_heading:
        return "Ngày sinh"

    # 'DiaChiSinh' and 'DiaChiTru' are combinations of 'SoNhaDuong', 'QuanHuyen' and 'TinhThanh'
    if key == 'DiaChiSinh':
        if not is_heading:
            return candidate[INDEX_OF_KEY['SoNhaDuongSinh']] + ", " + candidate[INDEX_OF_KEY['QuanHuyenSinh']] + ", " + \
                   candidate[INDEX_OF_KEY['TinhThanhSinh']]
        else:
            return "Địa chỉ hiện tại"
    if key == 'DiaChiTru':
        if not is_heading:
            return candidate[INDEX_OF_KEY['SoNhaDuongTru']] + ", " + candidate[INDEX_OF_KEY['QuanHuyenTru']] + ", " + \
                   candidate[INDEX_OF_KEY['TinhThanhTru']]
        else:
            return "Địa chỉ gia đình"
    return candidate[INDEX_OF_KEY[key]]


def moneyProcessing(candidate, key):
    """
        Usage: moneyProcessing(candidate, key)
        This function transform an integer like 100000 into a "money" form like "100.000 đồng"
        Params(2):
            candidate:      The csv row w.r.t a candidate
            key:            The field to get
    """

    transformed_value = get(candidate, key)
    if len(transformed_value) >= 7:
        l = len(transformed_value)
        transformed_value = transformed_value[0:-6] + '.' + transformed_value[l - 6:l]
    if len(transformed_value) >= 5:
        l = len(transformed_value)
        transformed_value = transformed_value[0:-3] + '.' + transformed_value[l - 3:l]
    if transformed_value != '' and transformed_value != '0':
        transformed_value += u' đồng'
    return transformed_value


def createStyles():
    """
        Usage: createStyles()
        This function initializes all necessary document styles for the final output pdf
        Params(0): No param
    """

    Styles = getSampleStyleSheet()

    # logo text + signature
    Styles.add(ParagraphStyle(name='Signature Style',
                              fontName='UVNB', fontSize=10, alignment=TA_RIGHT, rightIndent=10))

    # Document title
    Styles.add(ParagraphStyle(name='Title Style',
                              fontName='UVNB', fontSize=16, alignment=TA_CENTER, spaceAfter=3 * LINE_SPACING,
                              spaceBefore=3 * LINE_SPACING))

    # Document body text
    Styles.add(ParagraphStyle(name='Body Style',
                              fontName='UVNI', fontSize=12, leading=16, alignment=TA_JUSTIFY, spaceAfter=LINE_SPACING))

    # Document body text
    Styles.add(ParagraphStyle(name='Body Right Style',
                              fontName='UVNI', fontSize=12, leading=16, alignment=TA_RIGHT, spaceAfter=LINE_SPACING))

    # Document body text
    Styles.add(ParagraphStyle(name='Body Center Style',
                              fontName='UVNI', fontSize=12, leading=16, alignment=TA_CENTER, spaceAfter=LINE_SPACING))

    # Document body text with italic
    Styles.add(ParagraphStyle(name='Italic Body Style',
                              fontName='UVNI', fontSize=12, alignment=TA_JUSTIFY, spaceAfter=LINE_SPACING))

    # Heading I
    Styles.add(ParagraphStyle(name='Heading I Style',
                              fontName='UVNB', fontSize=12, alignment=TA_JUSTIFY, spaceBefore=2 * LINE_SPACING,
                              spaceAfter=2 * LINE_SPACING))

    # Table Heading
    Styles.add(ParagraphStyle(name='Table Heading Style',
                              fontName='UVNB', fontSize=12, leading=16, alignment=TA_CENTER))

    # Table Cell
    Styles.add(ParagraphStyle(name='Table Cell Style',
                              fontName='UVNI', fontSize=12, leading=16))

    # LoM Body
    Styles.add(ParagraphStyle(name='LoM Body Style',
                              fontName='UVN', fontSize=12, alignment=TA_JUSTIFY, spaceAfter=LINE_SPACING,
                              firstLineIndent=28, leading=20))

    return Styles


# Some document styles
DOC_STYLES = createStyles()


def newLine(Story, nbLines):
    """
        Usage: newLine(Story, nbLines)
        This function makes several empty lines in the current story of the output pdf
        Params(2):
            Story: The current reportlab story
            nbLines: The number of empty lines to make

    """
    for index in xrange(nbLines):
        Story.append(Paragraph('', DOC_STYLES['Body Style']))


def rename(my_string):
    '''
        Usage: rename(my_string)
        This function transforms a Vietnamese string into standard ASCII-string, eg. "Đường" into "Duong"
        Params(1):
            my_string: The string to be transformed.
    '''
    my_new_string = ''
    current = ''
    for index in xrange(len(my_string)):
        # Only transform letters in the REMOVE_ACCENT dictionary
        if current in REMOVE_ACCENT:
            my_new_string += REMOVE_ACCENT[current]
            current = ''

        # All ASCII letters should be conserved
        if ord(my_string[index]) <= 123 and ord(my_string[index]) >= 65:
            my_new_string += my_string[index]
            current = ''

        else:
            current += my_string[index]

    if current in REMOVE_ACCENT:
        my_new_string += REMOVE_ACCENT[current]
    return my_new_string.title().replace(' ', '_')


def buildPdfName(candidate, index):
    '''
        Usage: buildPdfName(candidate, index)
        This function builds the name for the output pdf, which is Schoolname + _ + Candidate's fullname + _ + index
        Params(2):
            candidate:      The csv row w.r.t a candidate
            index:          The order of this candidate's row in the csv file
    '''
    filename = SCHOOL_CODE[get(candidate, 'Truong')] + '_' + rename(get(candidate, 'HoVaTen')) + '_' + str(index)
    return filename


def transform_to_list(filename):
    '''
        Usage: transform_to_list(filename)
        This function transforms the csv file 'filename' into a list of lists of strings. Each list of strings represents a candidate. Each column represents a field.
        Arguments expected (1): The name of the csv file.
    '''
    with open(filename, 'rU') as f:
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter=','))
        f.close()
    return data


def createLogo(candidate):
    '''
        This function creates logo and logo text for some pdf pages.
    '''

    # For DH Singapore
    if SCHOOL_CODE[get(candidate, 'Truong')] in ['CNHN', 'KTLHCM']:
        # read image and put to flowable object
        logo_img = PIL_Image.open(logodir + 'logo_dong_hanh_sing.png')
        imsize = logo_img.size
        imw = float(imsize[0]) * .09
        imh = float(imsize[1]) * .09
        logo_img = Flowable_Image(logodir + 'logo_dong_hanh_sing.png', imw, imh)
        logo_img.hAlign = 'LEFT'

        # create DH info
        logo_text = []
        logo_text.append(Paragraph('Quỹ học bổng Đồng Hành Singapore', DOC_STYLES['Signature Style']))
        logo_text.append(Paragraph('Website: www.donghanh.net', DOC_STYLES['Signature Style']))
        logo_text.append(Paragraph('Email: contact@donghanh.net', DOC_STYLES['Signature Style']))

        return logo_img, logo_text

    elif SCHOOL_CODE[get(candidate, 'Truong')] in ['CTHO']:
        # read image and put to flowable object
        logo_img = PIL_Image.open(logodir + 'logo_dong_hanh.png')
        imsize = logo_img.size
        imw = float(imsize[0]) * .15
        imh = float(imsize[1]) * .15
        logo_img = Flowable_Image(logodir + 'logo_dong_hanh.png', imw, imh)
        logo_img.hAlign = 'LEFT'

        # create DH info
        logo_text = []
        logo_text.append(Paragraph('Quỹ học bổng Đồng Hành Đài Loan', DOC_STYLES['Signature Style']))
        logo_text.append(Paragraph('Website: www.donghanh.net', DOC_STYLES['Signature Style']))
        logo_text.append(Paragraph('Email: contact@donghanh.net', DOC_STYLES['Signature Style']))

        return logo_img, logo_text

    # Now for DH France
    # read image and put to flowable object
    logo_img = PIL_Image.open(logodir + 'logo_dong_hanh.png')
    imsize = logo_img.size
    imw = float(imsize[0]) * .15
    imh = float(imsize[1]) * .15
    logo_img = Flowable_Image(logodir + 'logo_dong_hanh.png', imw, imh)
    logo_img.hAlign = 'LEFT'

    # create DH info
    logo_text = []
    logo_text.append(Paragraph('Quỹ học bổng Đồng Hành', DOC_STYLES['Signature Style']))
    logo_text.append(Paragraph('16 rue Petit-Musc', DOC_STYLES['Signature Style']))
    logo_text.append(Paragraph('75004, Paris, Pháp', DOC_STYLES['Signature Style']))
    logo_text.append(Paragraph('Email: contact@donghanh.net', DOC_STYLES['Signature Style']))

    return logo_img, logo_text


def make_tabs(N): return '&nbsp;' * N


def download(urllink, filename):
    '''
        Usage: download(urllink, filename)
        This function downloads content from urllink and save it under 'filename'
        Params(2):
            urllink:        the URL link
            filename:       The filename to be saved.
    '''
    r = requests.get(urllink)
    with open(filename, "wb") as code:
        code.write(r.content)
    return filename


############### ----------END OF LOCAL FUNCTIONS---------- ###############

############### ----------CORE FUNCTION---------- ###############

def buildPdf(target, index, candidate, heading_csv):
    '''
        Usage: buildPdf(target, index, candidate, heading_csv)
        This function builds the output pdf.
        Params(4):
            target          The directory for output files
            index:          Index of the candidate's row in the csv
            candidate:      The csv row w.r.t a candidate
            heading_csv:    The heading row of the csv file
    '''
    # set path for temporary files
    TMP_PATH = target + 'tmp/'
    INTERVIEW_PATH = target + 'INTERVIEW/'
    if get(candidate, 'Truong') == '-':
        candidate[INDEX_OF_KEY['Truong']] = "Unknown"
    filename = buildPdfName(candidate, index)
    filename2 = buildPdfName(candidate, 0)
    # initialise document
    Doc = SimpleDocTemplate(TMP_PATH + filename + '_1.pdf', papersize=A4,
                            rightMargin=RIGHT_MARGIN, leftMargin=LEFT_MARGIN,
                            topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
                            title=filename, author='DH\'s pdf generator v1.0', )

    Story = []

    # Sơ yếu lí lịch
    Story = step1(Story, candidate, heading_csv, TMP_PATH)

    # Phiếu điều tra
    Story = step2(Story, candidate, heading_csv)

    # Thư xin học bổng
    Story = step3(Story, candidate)

    # create temporary file
    Doc.build(Story)

    # Download attachments
    has_file = step4(candidate, TMP_PATH + filename)

    # Ý kiến đánh giá
    Doc = SimpleDocTemplate(TMP_PATH + filename + '_6.pdf', papersize=A4,
                            rightMargin=RIGHT_MARGIN, leftMargin=LEFT_MARGIN,
                            topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
                            title=filename, author='DH\'s pdf generator v1.0', )
    DocForInterview = SimpleDocTemplate(
        INTERVIEW_PATH + SCHOOL_CODE[get(candidate, 'Truong')] + '/' + filename + '_6.pdf', papersize=A4,
        rightMargin=RIGHT_MARGIN, leftMargin=LEFT_MARGIN,
        topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
        title=filename, author='DH\'s pdf generator v1.0', )
    Story = []
    Story = step5(Story, candidate, heading_csv)
    Doc.build(Story)
    Story = step5(Story, candidate, heading_csv)
    DocForInterview.build(Story)

    success = 1

    # Create a merger (an object to merge documents) then join created documents into the merger.
    merger = PdfFileMerger(strict=False)
    input = PdfFileReader(file(TMP_PATH + filename + '_1.pdf', 'rb'))
    merger.append(input)

    # Check if need to merge pdf with attachments
    # Some pdf may be encrypted, in this case automatic merge cannot be performed.
    # Thư xin học bổng (scan)
    if has_file['ThuXinHocBongScan'] == 1:
        try:
            input = PdfFileReader(file(TMP_PATH + filename + '_2.pdf', 'rb'))
            if not input.isEncrypted:
                merger.append(input)
            else:
                logger.info(
                    "Không thể nối thư xin học bổng ở hồ sơ thứ " + str(index) + ". Yêu cầu thực hiện thủ công.")
                success = 0
        except PdfReadError as e:
            success = 0
            formatted_lines = traceback.format_exc().splitlines()
            trace_back = "\n".join(formatted_lines)
            logger.info(trace_back)
            logger.error("Failed file: {}".format(TMP_PATH + filename + '_2.pdf'))
            logger.info("Không thể nối thư xin học bổng ở hồ sơ thứ " + str(index) + ". Yêu cầu thực hiện thủ công.")

    # Bảng điểm
    if has_file['BangDiemScan'] == 1:
        try:
            input = PdfFileReader(file(TMP_PATH + filename + '_3.pdf', 'rb'))
            if not input.isEncrypted:
                merger.append(input)
            else:
                logger.error("Không thể nối bảng điểm ở hồ sơ thứ " + str(index) + ". Yêu cầu thực hiện thủ công.")
                success = 0
        except PdfReadError as e:
            success = 0
            formatted_lines = traceback.format_exc().splitlines()
            trace_back = "\n".join(formatted_lines)
            logger.info(trace_back)
            logger.error("Failed file: {}".format(TMP_PATH + filename + '_3.pdf'))
            logger.error("Không thể nối bảng điểm ở hồ sơ thứ " + str(index) + ". Yêu cầu thực hiện thủ công.")

    # Chứng nhận hoàn cảnh khó khăn/Sổ hộ nghèo
    if has_file['ChungNhanKhoKhanScan'] == 1:
        try:
            input = PdfFileReader(file(TMP_PATH + filename + '_4.pdf', 'rb'))
            if not input.isEncrypted:
                merger.append(input)
            else:
                logger.error(
                    "Không thể nối chứng nhận khó khăn ở hồ sơ thứ " + str(index) + ". Yêu cầu thực hiện thủ công.")
                success = 0
        except PdfReadError as e:
            success = 0
            formatted_lines = traceback.format_exc().splitlines()
            trace_back = "\n".join(formatted_lines)
            logger.info(trace_back)
            logger.error("Failed file: {}".format(TMP_PATH + filename + '_4.pdf'))
            logger.error(
                "Không thể nối chứng nhận khó khăn ở hồ sơ thứ " + str(index) + ". Yêu cầu thực hiện thủ công.")

    # Giấy tờ khác
    if has_file['GiayToKhacScan'] == 1:
        try:
            input = PdfFileReader(file(TMP_PATH + filename + '_5.pdf', 'rb'))
            if not input.isEncrypted:
                merger.append(input)
            else:
                logger.error("Không thể các giấy tờ khác ở hồ sơ thứ " + str(index) + ". Yêu cầu thực hiện thủ công.")
                success = 0
        except PdfReadError as e:
            success = 0
            formatted_lines = traceback.format_exc().splitlines()
            trace_back = "\n".join(formatted_lines)
            logger.info(trace_back)
            logger.error("Failed file: {}".format(TMP_PATH + filename + '_5.pdf'))
            logger.error("Không thể các giấy tờ khác ở hồ sơ thứ " + str(index) + ". Yêu cầu thực hiện thủ công.")

    input = PdfFileReader(file(TMP_PATH + filename + '_6.pdf', 'rb'))
    merger.append(input)

    # final pdf path
    try:
        # pdf_path = '%s%s/%s.pdf' % (target, SCHOOL_CODE[get(candidate, 'Truong')], filename)
        if get(candidate, 'KhungVietThu') == "" and has_file['ThuXinHocBongScan'] == 0:
            merger.write(target + SCHOOL_CODE[get(candidate, 'Truong')] + '/DISQUALIFIED/' + filename + '.pdf')
        else:
            merger.write(target + SCHOOL_CODE[get(candidate, 'Truong')] + '/' + filename + '.pdf')
    except Exception as e:
        success = 0
        formatted_lines = traceback.format_exc().splitlines()
        trace_back = "\n".join(formatted_lines)
        logger.error(trace_back)

    # Delete tmp files if suceess
    if success:
        for index in xrange(1, 7):
            try:
                os.remove(TMP_PATH + filename + '_' + str(index) + '.pdf')
            except OSError:
                pass

    try:
        os.remove(TMP_PATH + filename2 + '_photo')
    except OSError as e:
        pass
    return filename

############### ----------END OF CORE FUNCTION---------- ###############

############### ----------PARTIAL FUNCTIONS---------- ###############

def step1(Story, candidate, heading_csv, TMP_PATH):
    '''
        This function creates "Sơ yếu lí lịch"
    '''
    filename = buildPdfName(candidate, 0)

    # add logo
    logo_img, logo_text = createLogo(candidate)
    Story.append(Table([[logo_img, logo_text]]))

    # add AnhCaNhan
    candidate_photo = ""
    if get(candidate, 'AnhCaNhan') != "yes" and get(candidate, 'AnhCaNhan') != "no" and get(candidate, 'AnhCaNhan') != "":
        try:
            # print(get(candidate, 'AnhCaNhan'))
            download(get(candidate, 'AnhCaNhan'), TMP_PATH + filename + '_photo')
            im = Image.open(TMP_PATH + filename + '_photo')
            imw = 75
            imh = 100
            candidate_photo = Flowable_Image(TMP_PATH + filename + '_photo', imw, imh)
            candidate_photo.hAlign = 'CENTER'
        except IOError as e:
            logger.error(e)
            logger.error("Invalid image. Discard candidate photo {}".format(filename))

        # c.drawImage(filename, inch, height - 2 * inch)

    # Title
    Story.append(Paragraph(u'SƠ YẾU LÍ LỊCH', DOC_STYLES['Title Style']))

    # Personal Infos
    Story.append(Paragraph(u'I. Thông tin cá nhân', DOC_STYLES['Heading I Style']))

    local_needed_fields = ['HoVaTen', 'GioiTinh', 'NgaySinh', 'MaSoSV', 'NamThu', 'KhoaNganh']
    table_data = [[(FIELD_NAMES_FULL[key] + ':').decode('utf-8'),
                   Paragraph(get(candidate, key).decode('utf-8'), DOC_STYLES['Italic Body Style']), candidate_photo] for
                  key in local_needed_fields]
    table_style = TRANSPARENT_TABLE_WITH_MERGE
    table = Table(table_data, colWidths=[136, 240, 120])
    table.setStyle(table_style)
    Story.append(table)

    local_needed_fields = ['Lop', 'Truong', 'DiaChiSinh', 'DiaChiTru', 'DienThoai', 'Email']
    table_data = [[(FIELD_NAMES_FULL[key] + ':').decode('utf-8'),
                   Paragraph(get(candidate, key).decode('utf-8'), DOC_STYLES['Italic Body Style'])] for key in
                  local_needed_fields]
    table_style = TRANSPARENT_TABLE
    table = Table(table_data, colWidths=[136, 360])
    table.setStyle(table_style)
    Story.append(table)

    # Infos on family
    Story.append(Paragraph(u'II. Thông tin về các thành viên trong gia đình', DOC_STYLES['Heading I Style']))
    table_data = [[u'Họ và tên cha:', get(candidate, 'HoTenCha')],
                  [u'Tuổi:', get(candidate, 'TuoiCha'), u'Nghề nghiệp:', get(candidate, 'NgheNghiepCha')],
                  [u'Họ và tên mẹ:', get(candidate, 'HoTenMe')],
                  [u'Tuổi:', get(candidate, 'TuoiMe'), u'Nghề nghiệp:', get(candidate, 'NgheNghiepMe')]]
    table_style = TRANSPARENT_TABLE
    table = Table(table_data, colWidths=[100, 100, 100, 200])
    table.setStyle(table_style)
    Story.append(table)

    Story.append(Spacer(width=0, height=2 * LINE_SPACING))
    Story.append(Paragraph(u'Các thành viên khác trong gia đình:', DOC_STYLES['Body Style']))
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))

    # Family member table
    table_data = [[u'Họ và tên', u'Quan hệ', u'Tuổi', u'Nghề nghiệp']]
    for index in range(1, 10):
        row = get(candidate, 'NguoiThan' + str(index)).split(';')
        table_data += [[Paragraph(element, DOC_STYLES['Body Center Style']) for element in row]]
    table_style = STANDARD_TABLE
    table = Table(table_data, colWidths=[150, 120, 60, 170])
    table.setStyle(table_style)
    Story.append(table)

    # Story.append(PageBreak()) # new page

    # Study results
    Story.append(Paragraph(u'III. Kết quả học tập', DOC_STYLES['Heading I Style']))
    Story.append(Paragraph(u'Điểm trung bình các học kì đại học:', DOC_STYLES['Body Style']))
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))
    table_data = [[u'Học kì I năm I', u'Học kì II năm I', u'Học kì I năm II'], \
                  [get(candidate, key) for key in ['DiemKi1', 'DiemKi2', 'DiemKi3']]]
    table = Table(table_data, colWidths=[160, 160, 160])
    table_style = HORIZONTAL_NUMERIC_TABLE
    table.setStyle(table_style)
    Story.append(table)
    table_data = [[u'Điểm thi tốt nghiệp:', [Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                                             get(candidate, 'DiemTotNghiep').split("\n")]],
                  [u'Điểm thi đại học:', [Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                                          get(candidate, 'DiemDaiHoc').split("\n")]]]
    table = Table(table_data, colWidths=[150, 330])
    table_style = TRANSPARENT_TABLE
    table.setStyle(table_style)
    Story.append(table)

    Story.append(Spacer(width=0, height=2 * LINE_SPACING))

    # Other achievements
    Story.append(Paragraph(u'Các thành tích khác:', DOC_STYLES['Body Style']))
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))
    table_data = [[u'STT', u'Thành tích']] + \
                 [[str(index), Paragraph(get(candidate, 'ThanhTichKhac' + str(index)), DOC_STYLES['Table Cell Style'])]
                  for index in range(1, 6)]
    table = Table(table_data, colWidths=[30, 450])
    table_style = STANDARD_TABLE
    table.setStyle(table_style)
    Story.append(table)
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))

    # Other infos
    Story.append(Paragraph(u'IV. Các thông tin khác', DOC_STYLES['Heading I Style']))
    Story.append(Paragraph(('Nơi học THPT: <i>%s%s</i>' % (make_tabs(16), get(candidate, 'THPT'))).decode('utf-8'),
                           DOC_STYLES['Body Style']))

    Story.append(Paragraph(u'Bạn từng nhận được học bổng Đồng Hành bao giờ chưa? Nếu có, ở các kì nào?',
                           DOC_STYLES['Heading I Style']))
    LOCAL_TABLE_HEAD = {'NhanHBDHChua': u'Chưa từng có', 'KiN-5': u'Trước kì ' + str(CURRENT_SEMESTER - 4),
                        'KiN-4': u'Kì ' + str(CURRENT_SEMESTER - 4),
                        'KiN-3': u'Kì ' + str(CURRENT_SEMESTER - 3), 'KiN-2': u'Kì ' + str(CURRENT_SEMESTER - 2),
                        'KiN-1': u'Kì ' + str(CURRENT_SEMESTER - 1)}

    table_data = [
        [YES_NO_ICON[get(candidate, key)] + " " + LOCAL_TABLE_HEAD[key] for key in ['NhanHBDHChua', 'KiN-5', 'KiN-4']],
        [YES_NO_ICON[get(candidate, key)] + " " + LOCAL_TABLE_HEAD[key] for key in ['KiN-3', 'KiN-2', 'KiN-1']]]
    table_style = TRANSPARENT_REGULAR_TABLE
    table = Table(table_data, colWidths=[160, 160, 160])
    table.setStyle(table_style)
    Story.append(table)
    Story.append(Paragraph(u'Bạn từng được nhận hỗ trợ tài chính khác trong thời gian học đại học chưa?',
                           DOC_STYLES['Heading I Style']))
    Story.append(Paragraph(u'Nếu có, hãy ghi lại những hỗ trợ đó trong bảng dưới đây', DOC_STYLES['Body Style']))

    # Tạo bảng các thành tích khác
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))
    table_data = [[u'Tên học bổng/hỗ trợ', u'Thời gian nhận', u'Giá trị', u'Lí do được nhận']] + \
                 [[Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                   get(candidate, 'HoTro' + str(index)).split(';')] for index in range(1, 6)]
    table = Table(table_data, colWidths=[140, 100, 100, 140])
    table_style = STANDARD_TABLE
    table.setStyle(table_style)
    Story.append(table)
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))

    Story.append(Spacer(width=0, height=2 * LINE_SPACING))
    table_data = [[u'Các việc làm thêm', [Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                                          get(candidate, 'LamThem').split("\n")]],
                  [u'Những hoạt động khác', [Paragraph(element, DOC_STYLES['Table Cell Style']) for element in
                                             get(candidate, 'HoatDongKhac').split("\n")]]]
    table = Table(table_data, colWidths=[150, 330])
    table_style = TRANSPARENT_TABLE
    table.setStyle(table_style)
    Story.append(table)
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))

    Story.append(PageBreak())
    return Story


def step2(Story, candidate, heading_csv):
    '''
            This function creates "Phiếu điều tra"
    '''
    # add logo
    logo_img, logo_text = createLogo(candidate)
    Story.append(Table([[logo_img, logo_text]]))

    # Title
    Story.append(Paragraph(u'PHIẾU ĐIỀU TRA', DOC_STYLES['Title Style']))

    # Monthly costs
    Story.append(Paragraph(u'1. Chi phí hằng tháng:', DOC_STYLES['Heading I Style']))
    local_needed_fields = ['NhaO', 'DiLai', 'TienAn', 'TienHoc', 'TienHocThem', 'VuiChoi', 'CacKhoanKhac']
    table_data = [[(FIELD_NAMES_FULL[key] + ': ').decode('utf-8'), moneyProcessing(candidate, key)] for key in
                  local_needed_fields]
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[150, 250])
    table.setStyle(table_style)
    Story.append(table)
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))

    # Revenu
    Story.append(Paragraph(u'2. Thu nhập bình quân của gia đình:', DOC_STYLES['Heading I Style']))
    table_data = [['', moneyProcessing(candidate, 'ThuNhapBinhQuan')]]
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[150, 250])
    table.setStyle(table_style)
    Story.append(table)
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))

    # Resource contribution
    Story.append(Paragraph(u'3. Kinh phí để trang trải cho cuộc sống và học tập của bạn hiện nay là từ:',
                           DOC_STYLES['Heading I Style']))
    local_needed_fields = ['ThuNhapGiaDinh', 'ThuNhapHocBong', 'ThuNhapTienVay', 'ThuNhapLamThem']
    table_data = [[(FIELD_NAMES_FULL[key] + ': ').decode('utf-8'), moneyProcessing(candidate, key)] for key in
                  local_needed_fields]
    table_data.append([(FIELD_NAMES_FULL['ThuNhapKhac'] + ': ').decode('utf-8'),
                       Paragraph(get(candidate, 'ThuNhapKhac').decode('utf-8'), DOC_STYLES['Body Right Style'])])
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[150, 250])
    table.setStyle(table_style)
    Story.append(table)
    Story.append(Spacer(width=0, height=2 * LINE_SPACING))

    # Personal Difficulties
    Story.append(Paragraph(u'4. Khó khăn lớn nhất của bạn khi vào đại học:', DOC_STYLES['Heading I Style']))
    Story += [Paragraph(('%s%s' % (make_tabs(14), element)).decode('utf-8'), DOC_STYLES['Body Style']) for element in
              get(candidate, 'KhoKhanCuocSong').split('\n')]

    # Objectives
    Story.append(Paragraph(u'5. Nếu được nhận học bổng Đồng Hành trong học kì này, bạn sẽ sử dụng vào mục đích gì?',
                           DOC_STYLES['Heading I Style']))
    table_data = [[u'Đóng tiền học: ', YES_NO_ICON[get(candidate, 'DongTienHocKhong')], u'Thời gian: ',
                   Paragraph(get(candidate, 'DongTienHocBaoNhieu'), DOC_STYLES['Body Right Style'])],
                  [u'Đóng tiền nhà: ', YES_NO_ICON[get(candidate, 'DongTienNhaKhong')], u'Thời gian: ',
                   Paragraph(get(candidate, 'DongTienNhaBaoNhieu'), DOC_STYLES['Body Right Style'])],
                  [u'Học thêm ngoại ngữ, tin học: ', YES_NO_ICON[get(candidate, 'HocThemKhong')], u'Thời gian: ',
                   Paragraph(get(candidate, 'HocThemBaoNhieu'), DOC_STYLES['Body Right Style'])],
                  [u'Khác (ghi rõ): ', '', '',
                   Paragraph(get(candidate, 'HocThemBaoNhieu'), DOC_STYLES['Body Right Style'])]]
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[180, 30, 70, 150])
    table.setStyle(table_style)
    Story.append(table)

    # Communication
    Story.append(Paragraph(u'6. Sau khi nhận học bổng, bạn muốn liên lạc với Đồng Hành qua hình thức nào?',
                           DOC_STYLES['Heading I Style']))
    table_data = [
        [u'Trao đổi qua thư điện tử: ', YES_NO_ICON[get(candidate, 'LienLacCachNao1')], u'Nhận bản tin Đồng Hành: ',
         YES_NO_ICON[get(candidate, 'LienLacCachNao2')], ''],
        [u'Thông qua trang web, diễn đàn: ', YES_NO_ICON[get(candidate, 'LienLacCachNao3')], u'Gặp gỡ ở Việt Nam: ',
         YES_NO_ICON[get(candidate, 'LienLacCachNao4')], '']]
    table_style = VERTICAL_TRANSPARENT_NUMERIC_TABLE
    table = Table(table_data, colWidths=[200, 40, 200, 40, 10])
    table.setStyle(table_style)
    Story.append(table)

    # Other questions
    Story.append(
        Paragraph(('7. %s' % FIELD_NAMES_FULL['MongMuonNhanGiTuDH']).decode('utf-8'), DOC_STYLES['Heading I Style']))
    Story += [Paragraph(('<i>%s%s</i>' % (make_tabs(14), element)).decode('utf-8'), DOC_STYLES['Body Style']) for
              element in get(candidate, 'MongMuonNhanGiTuDH').split('\n')]
    Story.append(
        Paragraph(('8. %s' % FIELD_NAMES_FULL['KhoKhanLamHoSo']).decode('utf-8'), DOC_STYLES['Heading I Style']))
    Story += [Paragraph(('<i>%s%s</i>' % (make_tabs(14), element)).decode('utf-8'), DOC_STYLES['Body Style']) for
              element in get(candidate, 'KhoKhanLamHoSo').split('\n')]
    Story.append(Paragraph(('9. %s' % FIELD_NAMES_FULL['DeDatNhanNhu']).decode('utf-8'), DOC_STYLES['Heading I Style']))
    Story += [Paragraph(('<i>%s%s</i>' % (make_tabs(14), element)).decode('utf-8'), DOC_STYLES['Body Style']) for
              element in get(candidate, 'DeDatNhanNhu').split('\n')]

    Story.append(PageBreak())
    return Story


def step3(Story, candidate):
    '''
        This function creates "Thư xin học bổng đánh máy"
    '''

    if get(candidate, 'KhungVietThu') != "":
        # add logo
        logo_img, logo_text = createLogo(candidate)
        Story.append(Table([[logo_img, logo_text]]))
        # Title
        Story.append(Paragraph(u'THƯ XIN HỌC BỔNG', DOC_STYLES['Title Style']))

        # Body
        Story += \
            [Paragraph(('%s' % element).decode('utf-8'), DOC_STYLES['LoM Body Style']) for element in
             get(candidate, 'KhungVietThu').split('\n')]

    return Story


def step4(candidate, filename):
    '''
        This function downloads all files w.r.t the candidate
    '''
    # Initialize x that would tell us which documents have been updated: The transcription, the attestation, or both or none of them.
    # Download the files if any.
    has_file = {'ThuXinHocBongScan': 0, 'BangDiemScan': 0, 'ChungNhanKhoKhanScan': 0, 'GiayToKhacScan': 0}
    # Thư xin học bổng scan
    if get(candidate, 'KhungScanThu') != "" and get(candidate, 'KhungScanThu') != "no":
        download(get(candidate, 'KhungScanThu'), filename + '_2.pdf')
        has_file['ThuXinHocBongScan'] = 1;
    # Bảng điểm
    if get(candidate, 'BangDiemScan') != "" and get(candidate, 'BangDiemScan') != "no":
        download(get(candidate, 'BangDiemScan'), filename + '_3.pdf')
        has_file['BangDiemScan'] = 1;
    # Chứng nhận khó khăn/Sổ hộ nghèo
    if get(candidate, 'ChungNhanKhoKhanScan') != "" and get(candidate, 'ChungNhanKhoKhanScan') != "no":
        download(get(candidate, 'ChungNhanKhoKhanScan'), filename + '_4.pdf')
        has_file['ChungNhanKhoKhanScan'] = 1;
    # Giấy tờ khác
    if get(candidate, 'GiayToKhacScan') != "" and get(candidate, 'GiayToKhacScan') != "no":
        download(get(candidate, 'GiayToKhacScan'), filename + '_5.pdf')
        has_file['GiayToKhacScan'] = 1;
    return has_file


def step5(Story, candidate, filename):
    '''
        This function creates "Ý kiến đánh giá" page
    '''
    # add logo
    logo_img, logo_text = createLogo(candidate)
    Story.append(Table([[logo_img, logo_text]]))

    # heading
    Story.append(Paragraph(u'Ý KIẾN ĐÁNH GIÁ', DOC_STYLES['Title Style']))
    newLine(Story, 1)
    # body
    Story.append(Paragraph(u'Họ và tên người phỏng vấn: ', DOC_STYLES['Heading I Style']))
    Story.append(Paragraph(u'<b>Họ và tên sinh viên: </b>%s' % get(candidate, 'HoVaTen').decode('utf-8'),
                           DOC_STYLES['Body Style']))
    newLine(Story, 1)
    Story.append(Paragraph(u'1. Hoàn cảnh: ', DOC_STYLES['Heading I Style']))
    newLine(Story, 15)
    Story.append(Paragraph(u'2. Học tập: ', DOC_STYLES['Heading I Style']))
    newLine(Story, 10)
    Story.append(Paragraph(u'3. Ước mơ: ', DOC_STYLES['Heading I Style']))
    newLine(Story, 8)
    Story.append(Paragraph(u'4. Các phần khác: ', DOC_STYLES['Heading I Style']))
    newLine(Story, 8)
    # If the candidate declare some other documents, include them in this part to be checked by reviewer
    if len(get(candidate, 'GiayToKhacList')) >= 2:
        Story.append(Paragraph(u'Phần kiểm tra các giấy tờ khác', DOC_STYLES['Heading I Style']))
        Story.append(Paragraph(
            u'Người phỏng vấn đánh dấu ([X])vào ô các giấy tờ mà sinh viên có mang theo để ưu tiên khi đánh giá, xét chọn: ',
            DOC_STYLES['Body Style']))
        Story += [Paragraph(('[%s]<i>%s</i>' % (make_tabs(5), element)).decode('utf-8'), DOC_STYLES['Body Style']) for
                  element in get(candidate, 'GiayToKhacList').split('\n')]
    Story.append(
        Paragraph((u'Tại %s, ngày %s tháng %s năm %s' % (make_tabs(30), make_tabs(5), make_tabs(5), make_tabs(10))),
                  DOC_STYLES['Signature Style']))
    Story.append(Paragraph(u'Chữ kí người phỏng vấn%s' % make_tabs(30), DOC_STYLES['Signature Style']))
    return Story
