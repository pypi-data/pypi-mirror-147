# this is releaseed version 1.0
import os
import re
import datetime


# def name paser
# Function describe: This will unzip and parse dqe into multiple list.
class hkex_tools():

    def __init__(self):
        # def __init__( self , source_folder: str , current_file: str):
        # In this init, it will open the file and read.
        # caustion: if not source file exist, no need to read.
        # Other attribute, will be fill by related def because they will verify.
        # self.open_file(source_folder, current_file)
        # self.current_file = current_file
        # self.source_folder = source_folder
        pass

    #@classmethod
    def open_file( source_folder, current_file):
        # print('open_file')
        # print(self)

        self.current_file = str(current_file)
        self.source_folder = source_folder
        if os.path.isfile(self.source_folder + self.current_file):
            f = open(self.source_folder + self.current_file, 'r')
            self.lines = f.readlines()
            f.close()
        else:
            self.error = True

        if self.current_file[0:3] == 'hhif':
            # print('hhif reading')
            pass

        if self.current_file[0:4] == 'hsif':
            # print('hsif reading')
            self.slicing_hsif()

        if self.current_file[0:3] == 'dqe':
            self.slicing_dqe()
        # if os.path.exists(source_folder, current_file):
        #    return True

    def line_remove_symbol(self, line):
        line = re.sub(r'\*', '', line)
        line = re.sub(r'\n', '', line)
        line = re.sub(r'"', '', line)
        return line

    def verify_hsif_header(self):
        # Version of this parse is 220317
        # From time to time if HKEx update HSIF release html, this paser need upgrade.
        version = '220317_a'

        verify_result = False
        verify_marks = 0

        # c_files = open(self.source_folder+'\\' + self.current_file , 'r' )
        # multiple_lines = self.lines

        hkex_define_header = open("define_hsif_version_2022_02_18.txt", "r")
        hkex_define_header_lines = hkex_define_header.readlines()
        if hkex_define_header_lines[0] == self.lines[0]: verify_marks += 1
        if hkex_define_header_lines[1] == self.lines[1]: verify_marks += 1
        if hkex_define_header_lines[2] == self.lines[2]: verify_marks += 1
        if hkex_define_header_lines[3] == self.lines[3]: verify_marks += 1
        if hkex_define_header_lines[4] == self.lines[4]: verify_marks += 1
        if hkex_define_header_lines[5] == self.lines[5]: verify_marks += 1
        if hkex_define_header_lines[6] == self.lines[6]: verify_marks += 1
        if hkex_define_header_lines[7] == self.lines[7]: verify_marks += 1
        if hkex_define_header_lines[8][0:30] == self.lines[8][0:30]: verify_marks += 1
        if hkex_define_header_lines[9] == self.lines[9]: verify_marks += 1
        if hkex_define_header_lines[10] == self.lines[10]: verify_marks += 1

        # print("Verify Marks_" + str(verify_marks))
        if verify_marks > 9:
            verify_result = True

        return verify_result

    def slicing_hsif(self):
        verify_hsif = self.verify_hsif_header()
        if not (verify_hsif):
            print('version not correct, reading pause')
        lens = len(self.lines)

        ### Trade day of this file ###
        self.tradeday = datetime.datetime.strptime(re.sub('"', '', re.split(r',', self.lines[10])[7]), '%d %b %Y')
        # print(re.sub('"', '', re.split(r',', self.lines[10])[7]))
        self.pre_trade_day = datetime.datetime.strptime(re.sub('"', '', re.split(r',', self.lines[10])[1]), '%d %b %Y')

        # print(self.tradeday)
        # print(self.pre_trade_day)
        # Start from line 14

        ### Session start: This is header of this version" ###
        n = 14
        temp1 = re.sub('\*', '', self.lines[n])
        temp1 = re.sub('"', '', temp1)
        current_header = re.split(r',', temp1)
        current_header[16] = re.sub(r'\n', '', current_header[16])
        will_break = False
        # print('Current header {0}'.format(current_header))

        n = 15
        if not (self.lines[n] == '\n'):
            print('Format Error: This line is an empty line.'.format)

        n = 16
        # First product current period contract
        # =
        current_row = re.split(',', self.line_remove_symbol(self.lines[n]))
        self.current_month_product = {}
        # self.closing = self.current_month_product['Close Price']
        self.current_month_product['Trade Day'] = self.tradeday
        for i in range(0, 16 + 1):
            self.current_month_product[current_header[i]] = current_row[i]
            # print('debug i {0} : header: {1} | current_row : {2}'.format(i,current_header[i] , current_row[i]))
        # print(self.current_month_product)
        self.closing = self.current_month_product['Close Price']

        # Second product is the Next period contract
        n = 17
        temp1 = self.line_remove_symbol(self.lines[n])

        current_row = re.split(r',', temp1)
        self.next_month_product = {}
        self.next_month_product['Trade Day'] = self.tradeday
        for i in range(0, 16 + 1):
            self.next_month_product[current_header[i]] = current_row[i]
        # print('next month product')
        # print(self.next_month_product)

        n = 19
        while (will_break == False):
            if self.lines[n] == '\n':
                will_break = True
                # print('n:{0}'.format(n))

            if re.search('END OF REPORT', self.lines[n]):
                will_break = True
            current_row = re.split(r',', self.lines[n])
            if len(current_row) > 1:
                current_row[16] = re.sub('\n', '', current_row[16])
                # print(current_row[16])

            n += 1
            #    print('End of report :{0}'.format(n))

    def historical_to_list(self):
        # slice all kind of hkex product
        if self.current_file[0:4] == 'hsif':
            self.slicing_hsif()

    def verify_dqe_header(self):
        # Version of this parse is 220317
        # From time to time if HKEx update HSIF release html, this paser need upgrade.
        version = '220317_a'

        verify_result = False
        verify_marks = 0
        hkex_define_header = open("define_dqe_version_2022_02_18.txt", "r")
        hkex_define_header_lines = hkex_define_header.readlines()
        if hkex_define_header_lines[0] == self.lines[0]: verify_marks += 1
        if hkex_define_header_lines[1] == self.lines[1]: verify_marks += 1
        if hkex_define_header_lines[2] == self.lines[2]: verify_marks += 1
        if hkex_define_header_lines[3] == self.lines[3]: verify_marks += 1
        if hkex_define_header_lines[4] == self.lines[4]: verify_marks += 1
        if hkex_define_header_lines[5] == self.lines[5]: verify_marks += 1
        if hkex_define_header_lines[6][0:30] == self.lines[6][0:30]: verify_marks += 1
        if hkex_define_header_lines[7] == self.lines[7]: verify_marks += 1
        if hkex_define_header_lines[8] == self.lines[8]: verify_marks += 1
        if hkex_define_header_lines[9] == self.lines[9]: verify_marks += 1
        if hkex_define_header_lines[10] == self.lines[10]: verify_marks += 1

        # print("Verify Marks_" + str(verify_marks))
        if verify_marks > 9:
            verify_result = True

        return verify_result

    def slicing_dqe(self):
        verify_dqe = self.verify_dqe_header()
        # print(verify_dqe)
        if not (verify_dqe):
            print('dqe version not correct, reading pause')
        lens = len(self.lines)
        ## Trade day of this file
        temp = re.sub('\n', '', re.sub('STOCK OPTIONS DAILY MARKET REPORT AS AT ', '', re.sub('"', '', self.lines[6])))
        self.tradeday = datetime.datetime.strptime(temp, '%d %b %Y')
        # print(self.tradeday)
        # print(self.pre_trade_day)
        # Start from line 14
        temp = self.lines[116]
        temp1 = re.split(',', self.lines[114])
        temp1 = re.sub('\n', '', temp1[9])
        self.tencent_iv = temp1

        ### Session start: This is header of this version" ##
