# Module: others

# 获取软件包的本机版本
def get_current_version(package_name='guan'):
    import importlib.metadata
    try:
        current_version = importlib.metadata.version(package_name)
        return current_version
    except:
        return None

# 获取Python软件包的最新版本
def get_latest_version(package_name='guan', timeout=5):
    import requests
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=timeout)
    except:
        return None
    if response.status_code == 200:
        data = response.json()
        latest_version = data["info"]["version"]
        return latest_version
    else:
        return None

# 获取包含某个字符的进程PID值
def get_PID_array(name):
    import subprocess
    command = "ps -ef | grep "+name
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        ps_ef = result.stdout
    import re
    ps_ef_1 = re.split(r'\n', ps_ef)
    id_running_array = []
    for ps_ef_item in ps_ef_1:
        if ps_ef_item != '':
            ps_ef_2 = re.split(r'\s+', ps_ef_item)
            id_running_array.append(ps_ef_2[1])
    return id_running_array

# 每日git commit次数的统计
def statistics_of_git_commits(print_show=0, str_or_datetime='str'):
    import subprocess
    import collections
    since_date = '100 year ago'
    result = subprocess.run(
        ['git', 'log', f'--since={since_date}', '--pretty=format:%ad', '--date=short'],
        stdout=subprocess.PIPE,
        text=True)
    commits = result.stdout.strip().split('\n')
    counter = collections.Counter(commits)
    daily_commit_counts = dict(sorted(counter.items()))
    date_array = []
    commit_count_array = []
    for date, count in daily_commit_counts.items():
        if print_show == 1:
            print(f"{date}: {count} commits")
        if str_or_datetime=='datetime':
            import datetime
            date_array.append(datetime.datetime.strptime(date, "%Y-%m-%d"))
        elif str_or_datetime=='str':
            date_array.append(date)
        commit_count_array.append(count)
    return date_array, commit_count_array

# 将文件目录结构写入Markdown文件
def write_file_list_in_markdown(directory='./', filename='a', reverse_positive_or_negative=1, starting_from_h1=None, banned_file_format=[], hide_file_format=None, divided_line=None, show_second_number=None, show_third_number=None): 
    import os
    f = open(filename+'.md', 'w', encoding="utf-8")
    filenames1 = os.listdir(directory)
    u0 = 0
    for filename1 in filenames1[::reverse_positive_or_negative]:
        filename1_with_path = os.path.join(directory,filename1) 
        if os.path.isfile(filename1_with_path):
            if os.path.splitext(filename1)[1] not in banned_file_format:
                if hide_file_format == None:
                    f.write('+ '+str(filename1)+'\n\n')
                else:
                    f.write('+ '+str(os.path.splitext(filename1)[0])+'\n\n')
        else:
            u0 += 1
            if divided_line != None and u0 != 1:
                f.write('--------\n\n')
            if starting_from_h1 == None:
                f.write('#')
            f.write('# '+str(filename1)+'\n\n')

            filenames2 = os.listdir(filename1_with_path) 
            i0 = 0     
            for filename2 in filenames2[::reverse_positive_or_negative]:
                filename2_with_path = os.path.join(directory, filename1, filename2) 
                if os.path.isfile(filename2_with_path):
                    if os.path.splitext(filename2)[1] not in banned_file_format:
                        if hide_file_format == None:
                            f.write('+ '+str(filename2)+'\n\n')
                        else:
                            f.write('+ '+str(os.path.splitext(filename2)[0])+'\n\n')
                else: 
                    i0 += 1
                    if starting_from_h1 == None:
                        f.write('#')
                    if show_second_number != None:
                        f.write('## '+str(i0)+'. '+str(filename2)+'\n\n')
                    else:
                        f.write('## '+str(filename2)+'\n\n')
                    
                    j0 = 0
                    filenames3 = os.listdir(filename2_with_path)
                    for filename3 in filenames3[::reverse_positive_or_negative]:
                        filename3_with_path = os.path.join(directory, filename1, filename2, filename3) 
                        if os.path.isfile(filename3_with_path): 
                            if os.path.splitext(filename3)[1] not in banned_file_format:
                                if hide_file_format == None:
                                    f.write('+ '+str(filename3)+'\n\n')
                                else:
                                    f.write('+ '+str(os.path.splitext(filename3)[0])+'\n\n')
                        else:
                            j0 += 1
                            if starting_from_h1 == None:
                                f.write('#')
                            if show_third_number != None:
                                f.write('### ('+str(j0)+') '+str(filename3)+'\n\n')
                            else:
                                f.write('### '+str(filename3)+'\n\n')

                            filenames4 = os.listdir(filename3_with_path)
                            for filename4 in filenames4[::reverse_positive_or_negative]:
                                filename4_with_path = os.path.join(directory, filename1, filename2, filename3, filename4) 
                                if os.path.isfile(filename4_with_path):
                                    if os.path.splitext(filename4)[1] not in banned_file_format:
                                        if hide_file_format == None:
                                            f.write('+ '+str(filename4)+'\n\n')
                                        else:
                                            f.write('+ '+str(os.path.splitext(filename4)[0])+'\n\n')
                                else: 
                                    if starting_from_h1 == None:
                                        f.write('#')
                                    f.write('#### '+str(filename4)+'\n\n')

                                    filenames5 = os.listdir(filename4_with_path)
                                    for filename5 in filenames5[::reverse_positive_or_negative]:
                                        filename5_with_path = os.path.join(directory, filename1, filename2, filename3, filename4, filename5) 
                                        if os.path.isfile(filename5_with_path): 
                                            if os.path.splitext(filename5)[1] not in banned_file_format:
                                                if hide_file_format == None:
                                                    f.write('+ '+str(filename5)+'\n\n')
                                                else:
                                                    f.write('+ '+str(os.path.splitext(filename5)[0])+'\n\n')
                                        else:
                                            if starting_from_h1 == None:
                                                f.write('#')
                                            f.write('##### '+str(filename5)+'\n\n')

                                            filenames6 = os.listdir(filename5_with_path)
                                            for filename6 in filenames6[::reverse_positive_or_negative]:
                                                filename6_with_path = os.path.join(directory, filename1, filename2, filename3, filename4, filename5, filename6) 
                                                if os.path.isfile(filename6_with_path): 
                                                    if os.path.splitext(filename6)[1] not in banned_file_format:
                                                        if hide_file_format == None:
                                                            f.write('+ '+str(filename6)+'\n\n')
                                                        else:
                                                            f.write('+ '+str(os.path.splitext(filename6)[0])+'\n\n')
                                                else:
                                                    if starting_from_h1 == None:
                                                        f.write('#')
                                                    f.write('###### '+str(filename6)+'\n\n')
    f.close()

# 从网页的标签中获取内容
def get_html_from_tags(link, tags=['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'a']):
    from bs4 import BeautifulSoup
    import urllib.request
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    html = urllib.request.urlopen(link).read().decode('utf-8')
    soup = BeautifulSoup(html, features="lxml")
    all_tags = soup.find_all(tags)
    content = ''
    for tag in all_tags:
        text = tag.get_text().replace('\n', '')
        if content == '':
            content = text
        else:
            content = content + '\n\n' + text
    return content

# 从HTML中获取所有的链接
def get_links_from_html(html_link, links_with_text=0):
    from bs4 import BeautifulSoup
    import urllib.request
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    html = urllib.request.urlopen(html_link).read().decode('utf-8')
    soup = BeautifulSoup(html, features="lxml")
    a_tags = soup.find_all('a')
    if links_with_text == 0:
        link_array = [tag.get('href') for tag in a_tags if tag.get('href')]
        return link_array
    else:
        link_array_with_text = [(tag.get('href'), tag.text) for tag in a_tags if tag.get('href')]
        return link_array_with_text

# 检查链接的有效性
def check_link(url, timeout=3, allow_redirects=True):
    import requests
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=allow_redirects)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

# 检查链接数组中链接的有效性
def check_link_array(link_array, timeout=3, allow_redirects=True, try_again=0, print_show=1):
    import guan
    failed_link_array0 = []
    for link in link_array:
        if link=='#' or guan.check_link(link, timeout=timeout, allow_redirects=allow_redirects):
            pass
        else:
            failed_link_array0.append(link)
            if print_show:
                print(link)
    failed_link_array = []
    if try_again:
        if print_show:
            print('\nTry again:\n')
        for link in failed_link_array0:
            if link=='#' or guan.check_link(link, timeout=timeout, allow_redirects=allow_redirects):
                pass
            else:
                failed_link_array.append(link)
                if print_show:
                    print(link)
    else:
        failed_link_array = failed_link_array0
    return failed_link_array

# 生成二维码
def creat_qrcode(data="https://www.guanjihuan.com", filename='a', file_format='.png'):
    import qrcode
    img = qrcode.make(data)
    img.save(filename+file_format)

# 将PDF文件转成文本
def pdf_to_text(pdf_path):
    from pdfminer.pdfparser import PDFParser, PDFDocument
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.layout import LAParams, LTTextBox
    from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
    import logging 
    logging.Logger.propagate = False 
    logging.getLogger().setLevel(logging.ERROR) 
    praser = PDFParser(open(pdf_path, 'rb'))
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        content = ''
        for page in doc.get_pages():
            interpreter.process_page(page)                        
            layout = device.get_result()                     
            for x in layout:
                if isinstance(x, LTTextBox):
                    content  = content + x.get_text().strip()
    return content

# 获取PDF文件页数
def get_pdf_page_number(pdf_path):
    import PyPDF2
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    return num_pages

# 获取PDF文件指定页面的内容
def pdf_to_txt_for_a_specific_page(pdf_path, page_num=1):
    import PyPDF2
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    for page_num0 in range(num_pages):
        if page_num0 == page_num-1:
            page = pdf_reader.pages[page_num0]
            page_text = page.extract_text()
    pdf_file.close()
    return page_text

# 获取PDF文献中的链接。例如: link_starting_form='https://doi.org'
def get_links_from_pdf(pdf_path, link_starting_form=''):
    import PyPDF2
    import re
    reader = PyPDF2.PdfReader(pdf_path)
    pages = len(reader.pages)
    i0 = 0
    links = []
    for page in range(pages):
        pageSliced = reader.pages[page]
        pageObject = pageSliced.get_object() 
        if '/Annots' in pageObject.keys():
            ann = pageObject['/Annots']
            old = ''
            for a in ann:
                u = a.get_object() 
                if '/A' in u.keys():
                    if '/URI' in u['/A']: 
                        if re.search(re.compile('^'+link_starting_form), u['/A']['/URI']):
                            if u['/A']['/URI'] != old:
                                links.append(u['/A']['/URI']) 
                                i0 += 1
                                old = u['/A']['/URI']
    return links

# 通过Sci-Hub网站下载文献
def download_with_scihub(address=None, num=1):
    from bs4 import BeautifulSoup
    import re
    import requests
    import os
    if num==1 and address!=None:
        address_array = [address]
    else:
        address_array = []
        for i in range(num):
            address = input('\nInput：')
            address_array.append(address)
    for address in address_array:
        r = requests.post('https://sci-hub.st/', data={'request': address})
        print('\nResponse：', r)
        print('Address：', r.url)
        soup = BeautifulSoup(r.text, features='lxml')
        pdf_URL = soup.embed['src']
        # pdf_URL = soup.iframe['src'] # This is a code line of history version which fails to get pdf URL.
        if re.search(re.compile('^https:'), pdf_URL):
            pass
        else:
            pdf_URL = 'https:'+pdf_URL
        print('PDF address：', pdf_URL)
        name = re.search(re.compile('fdp.*?/'),pdf_URL[::-1]).group()[::-1][1::]
        print('PDF name：', name)
        print('Directory：', os.getcwd())
        print('\nDownloading...')
        r = requests.get(pdf_URL, stream=True)
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=32):
                f.write(chunk)
        print('Completed!\n')
    if num != 1:
        print('All completed!\n')

# 将字符串转成音频
def str_to_audio(str='hello world', filename='str', rate=125, voice=1, read=1, save=0, compress=0, bitrate='16k', print_text=0):
    import pyttsx3
    import guan
    if print_text==1:
        print(str)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[voice].id)
    engine.setProperty("rate", rate)
    if save==1:
        engine.save_to_file(str, filename+'.wav')
        engine.runAndWait()
        print('Wav file saved!')
        if compress==1:
            import os
            os.rename(filename+'.wav', 'temp.wav')
            guan.compress_wav_to_mp3('temp.wav', output_filename=filename+'.mp3', bitrate=bitrate)
            os.remove('temp.wav')
    if read==1:
        engine.say(str)
        engine.runAndWait()

# 将txt文件转成音频
def txt_to_audio(txt_path, rate=125, voice=1, read=1, save=0, compress=0, bitrate='16k', print_text=0):
    import pyttsx3
    import guan
    f = open(txt_path, 'r', encoding ='utf-8')
    text = f.read()
    if print_text==1:
        print(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[voice].id)
    engine.setProperty("rate", rate)
    if save==1:
        import re
        filename = re.split('[/,\\\]', txt_path)[-1][:-4]
        engine.save_to_file(text, filename+'.wav')
        engine.runAndWait()
        print('Wav file saved!')
        if compress==1:
            import os
            os.rename(filename+'.wav', 'temp.wav')
            guan.compress_wav_to_mp3('temp.wav', output_filename=filename+'.mp3', bitrate=bitrate)
            os.remove('temp.wav')
    if read==1:
        engine.say(text)
        engine.runAndWait()

# 将PDF文件转成音频
def pdf_to_audio(pdf_path, rate=125, voice=1, read=1, save=0, compress=0, bitrate='16k', print_text=0):
    import pyttsx3
    import guan
    text = guan.pdf_to_text(pdf_path)
    text = text.replace('\n', ' ')
    if print_text==1:
        print(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[voice].id)
    engine.setProperty("rate", rate)
    if save==1:
        import re
        filename = re.split('[/,\\\]', pdf_path)[-1][:-4]
        engine.save_to_file(text, filename+'.wav')
        engine.runAndWait()
        print('Wav file saved!')
        if compress==1:
            import os
            os.rename(filename+'.wav', 'temp.wav')
            guan.compress_wav_to_mp3('temp.wav', output_filename=filename+'.mp3', bitrate=bitrate)
            os.remove('temp.wav')
    if read==1:
        engine.say(text)
        engine.runAndWait()

# 将wav音频文件压缩成MP3音频文件
def compress_wav_to_mp3(wav_path, output_filename='a.mp3', bitrate='16k'):
    # Note: Beside the installation of pydub, you may also need download FFmpeg on http://www.ffmpeg.org/download.html and add the bin path to the environment variable.
    from pydub import AudioSegment
    sound = AudioSegment.from_mp3(wav_path)
    sound.export(output_filename,format="mp3",bitrate=bitrate)

# 将WordPress导出的XML格式文件转换成多个MarkDown格式的文件
def convert_wordpress_xml_to_markdown(xml_file='./a.xml', convert_content=1, replace_more=[]):
    import xml.etree.ElementTree as ET
    import re
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for item in root.findall('.//item'):
        title = item.find('title').text
        content = item.find('.//content:encoded', namespaces={'content': 'http://purl.org/rss/1.0/modules/content/'}).text
        if convert_content == 1:
            content = re.sub(r'<!--.*?-->', '', content)
            content = content.replace('<p>', '')
            content = content.replace('</p>', '')
            content = content.replace('<ol>', '')
            content = content.replace('</ol>', '')
            content = content.replace('<ul>', '')
            content = content.replace('</ul>', '')
            content = content.replace('<strong>', '')
            content = content.replace('</strong>', '')
            content = content.replace('</li>', '')
            content = content.replace('<li>', '+ ')
            content = content.replace('</h3>', '')
            content = re.sub(r'<h2.*?>', '## ', content)
            content = re.sub(r'<h3.*?>', '### ', content)
            content = re.sub(r'<h4.*?>', '#### ', content)
            for replace_item in replace_more:
                content = content.replace(replace_item, '')
            for _ in range(100):
                content = content.replace('\n\n\n', '\n\n')
        else:
            pass
        markdown_content = f"# {title}\n{content}"
        markdown_file_path = f"{title}.md"
        cleaned_filename = re.sub(r'[/:*?"<>|\'\\]', ' ', markdown_file_path)
        with open(cleaned_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)

# 凯利公式
def kelly_formula(p, b, a=1):
    f=(p/a)-((1-p)/b)
    return f

# 获取所有股票
def all_stocks():
    import numpy as np
    import akshare as ak
    stocks = ak.stock_zh_a_spot_em()
    title = np.array(stocks.columns)
    stock_data = stocks.values
    return title, stock_data

# 获取所有股票的代码
def all_stock_symbols():
    import guan
    title, stock_data = guan.all_stocks()
    stock_symbols = stock_data[:, 1]
    return stock_symbols

# 股票代码的分类
def stock_symbols_classification():
    import guan
    import re
    stock_symbols = guan.all_stock_symbols()
    # 上交所主板
    stock_symbols_60 = []
    for stock_symbol in stock_symbols:
        find_600 = re.findall(r'^600', stock_symbol)
        find_601 = re.findall(r'^601', stock_symbol)
        find_603 = re.findall(r'^603', stock_symbol)
        find_605 = re.findall(r'^605', stock_symbol)
        if find_600 != [] or find_601 != [] or find_603 != [] or find_605 != []:
            stock_symbols_60.append(stock_symbol)
    # 深交所主板
    stock_symbols_00 = []
    for stock_symbol in stock_symbols:
        find_000 = re.findall(r'^000', stock_symbol)
        find_001 = re.findall(r'^001', stock_symbol)
        find_002 = re.findall(r'^002', stock_symbol)
        find_003 = re.findall(r'^003', stock_symbol)
        if find_000 != [] or find_001 != [] or find_002 != [] or find_003 != []:
            stock_symbols_00.append(stock_symbol)
    # 创业板
    stock_symbols_30 = []
    for stock_symbol in stock_symbols:
        find_300 = re.findall(r'^300', stock_symbol)
        find_301 = re.findall(r'^301', stock_symbol)
        if find_300 != [] or find_301 != []:
            stock_symbols_30.append(stock_symbol)
    # 科创板
    stock_symbols_68 = []
    for stock_symbol in stock_symbols:
        find_688 = re.findall(r'^688', stock_symbol)
        find_689 = re.findall(r'^689', stock_symbol)
        if find_688 != [] or find_689 != []:
            stock_symbols_68.append(stock_symbol)
    # 新三板
    stock_symbols_8_4 = []
    for stock_symbol in stock_symbols:
        find_82 = re.findall(r'^82', stock_symbol)
        find_83 = re.findall(r'^83', stock_symbol)
        find_87 = re.findall(r'^87', stock_symbol)
        find_88 = re.findall(r'^88', stock_symbol)
        find_430 = re.findall(r'^430', stock_symbol)
        find_420 = re.findall(r'^420', stock_symbol)
        find_400 = re.findall(r'^400', stock_symbol)
        if find_82 != [] or find_83 != [] or find_87 != [] or find_88 != [] or find_430 != [] or find_420 != [] or find_400 != []:
            stock_symbols_8_4.append(stock_symbol)
    # 检查遗漏的股票代码
    stock_symbols_others = []
    for stock_symbol in stock_symbols:
        if stock_symbol not in stock_symbols_60 and stock_symbol not in stock_symbols_00 and stock_symbol not in stock_symbols_30 and stock_symbol not in stock_symbols_68 and stock_symbol not in stock_symbols_8_4:
            stock_symbols_others.others.append(stock_symbol) 
    return stock_symbols_60, stock_symbols_00, stock_symbols_30, stock_symbols_68, stock_symbols_8_4, stock_symbols_others

# 股票代码各个分类的数量
def statistics_of_stock_symbols_classification():
    import guan
    stock_symbols_60, stock_symbols_00, stock_symbols_30, stock_symbols_68, stock_symbols_8_4, stock_symbols_others = guan.stock_symbols_classification()
    num_stocks_60 = len(stock_symbols_60)
    num_stocks_00 = len(stock_symbols_00)
    num_stocks_30 = len(stock_symbols_30)
    num_stocks_68 = len(stock_symbols_68)
    num_stocks_8_4 = len(stock_symbols_8_4)
    num_stocks_others= len(stock_symbols_others)
    return num_stocks_60, num_stocks_00, num_stocks_30, num_stocks_68, num_stocks_8_4, num_stocks_others

# 从股票代码获取股票名称
def find_stock_name_from_symbol(symbol='000002'):
    import guan
    title, stock_data = guan.all_stocks()
    for stock in stock_data:
        if symbol in stock:
           stock_name = stock[2]
    return stock_name

# 市值排序
def sorted_market_capitalization(num=10):
    import numpy as np
    import guan
    title, stock_data = guan.all_stocks()
    new_stock_data = []
    for stock in stock_data:
        if np.isnan(float(stock[9])):
            continue
        else:
            new_stock_data.append(stock)
    new_stock_data = np.array(new_stock_data)
    list_index = np.argsort(new_stock_data[:, 17])
    list_index = list_index[::-1]
    if num == None:
        num = len(list_index)
    sorted_array = []
    for i0 in range(num):
        stock_symbol = new_stock_data[list_index[i0], 1]
        stock_name = new_stock_data[list_index[i0], 2]
        market_capitalization = new_stock_data[list_index[i0], 17]/1e8
        sorted_array.append([i0+1, stock_symbol, stock_name, market_capitalization])
    return sorted_array

# 美股市值排序
def sorted_market_capitalization_us(num=10):
    import akshare as ak
    import numpy as np
    stocks = ak.stock_us_spot_em()
    stock_data = stocks.values
    new_stock_data = []
    for stock in stock_data:
        if np.isnan(float(stock[9])):
            continue
        else:
            new_stock_data.append(stock)
    new_stock_data = np.array(new_stock_data)
    list_index = np.argsort(new_stock_data[:, 9])
    list_index = list_index[::-1]
    if num == None:
        num = len(list_index)
    sorted_array = []
    for i0 in range(num):
        stock_symbol = new_stock_data[list_index[i0], 15]
        stock_name = new_stock_data[list_index[i0], 1]
        market_capitalization = new_stock_data[list_index[i0], 9]/1e8
        sorted_array.append([i0+1, stock_symbol, stock_name, market_capitalization])
    return sorted_array

# 获取单个股票的历史数据
def history_data_of_one_stock(symbol='000002', period='daily', start_date="19000101", end_date='21000101'):
    # period = 'daily'
    # period = 'weekly'
    # period = 'monthly'
    import numpy as np
    import akshare as ak
    stock = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date)
    title = np.array(stock.columns)
    stock_data = stock.values[::-1]
    return title, stock_data

# 绘制股票图
def plot_stock_line(date_array, opening_array, closing_array, high_array, low_array, lw_open_close=6, lw_high_low=2, xlabel='date', ylabel='price', title='', fontsize=20, labelsize=20, adjust_bottom=0.2, adjust_left=0.2, fontfamily='Times New Roman'):
    import guan
    plt, fig, ax = guan.import_plt_and_start_fig_ax(adjust_bottom=adjust_bottom, adjust_left=adjust_left, labelsize=labelsize, fontfamily=fontfamily)
    if fontfamily=='Times New Roman':
        ax.set_title(title, fontsize=fontsize, fontfamily='Times New Roman')
        ax.set_xlabel(xlabel, fontsize=fontsize, fontfamily='Times New Roman') 
        ax.set_ylabel(ylabel, fontsize=fontsize, fontfamily='Times New Roman')
    else:
        ax.set_title(title, fontsize=fontsize)
        ax.set_xlabel(xlabel, fontsize=fontsize)
        ax.set_ylabel(ylabel, fontsize=fontsize)
    for i0 in range(len(date_array)):
        if opening_array[i0] <= closing_array[i0]:
            ax.vlines(date_array[i0], opening_array[i0], closing_array[i0], linestyle='-', color='red', lw=lw_open_close)
            ax.vlines(date_array[i0], low_array[i0], high_array[i0], color='red', linestyle='-', lw=lw_high_low)
        else:
            ax.vlines(date_array[i0], opening_array[i0], closing_array[i0], linestyle='-', color='green', lw=lw_open_close)
            ax.vlines(date_array[i0], low_array[i0], high_array[i0], color='green', linestyle='-', lw=lw_high_low)
    plt.show()
    plt.close('all')

# Guan软件包的使用统计（仅仅统计装机数和import次数）
def statistics_of_guan_package(function_name=None):
    import guan
    try:
        import socket
        datetime_date = guan.get_date()
        datetime_time = guan.get_time()
        current_version = guan.get_current_version('guan')
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(0.5)
        client_socket.connect(('socket.guanjihuan.com', 12345))
        mac_address = guan.get_mac_address()
        if function_name == None:
            message = {
                'server': 'py.guanjihuan.com',
                'date': datetime_date,
                'time': datetime_time,
                'version': current_version,
                'MAC_address': mac_address,
            }
        else:
            message = {
                'server': 'py.guanjihuan.com',
                'date': datetime_date,
                'time': datetime_time,
                'version': current_version,
                'MAC_address': mac_address,
                'function_name': function_name
            }
        import json
        send_message = json.dumps(message)
        client_socket.send(send_message.encode())
        client_socket.close()
    except:
        pass

# # Guan软件包升级检查和提示（如果无法连接或者版本为最新，那么均没有提示）
# def notification_of_upgrade(timeout=5):
#     try:
#         import guan
#         latest_version = guan.get_latest_version(package_name='guan', timeout=timeout)
#         current_version = guan.get_current_version('guan')
#         if latest_version != None and current_version != None:
#             if latest_version != current_version:
#                 print('升级提示：您当前使用的版本是 guan-'+current_version+'，目前已经有最新版本 guan-'+latest_version+'。您可以通过以下命令对软件包进行升级：pip install --upgrade guan -i https://pypi.python.org/simple 或 pip install --upgrade guan')
#     except:
#         pass