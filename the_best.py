# -----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: *****PUT YOUR STUDENT NUMBER HERE*****
#    Student name: *****PUT YOUR NAME HERE*****
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).  91023PT
#
# --------------------------------------------------------------------#


# -----Assignment Description-----------------------------------------#
#
#  The Best, Then and Now
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application that allows the user to preview and print lists of
#  top-ten rankings.  See the specification document accompanying this
#  file for full details.
#
# --------------------------------------------------------------------#


# -----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.

# You MAY NOT use any other module other than those supplied in this template.
# You may negotiate a change of this restriction with your client (Donna Kingsbury)
# but be warned that non-standard modules such as 'Beautiful Soup' OR 'Pillow'
# will NOT be considered.

# You may need the following if there is a temporary SSL CERTIFICATE issue that is
# beyond your control.  Only uncomment the following two lines if that is the case.
##import ssl
##ssl._create_default_https_context = ssl._create_unverified_context

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution)
import os
from datetime import datetime
from time import gmtime, strftime
from urllib.request import urlopen
import webbrowser
# Import the standard Tkinter functions.
# (You WILL need to use these functions in your solution.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL


#
# --------------------------------------------------------------------#


# -----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

##### DEVELOP YOUR SOLUTION HERE #####
ABS_PATH = r'file:\\C:\Users\ADMIN\PycharmProjects\simple-is-the-best\{}'
def get_today_date():
    return datetime.today().strftime('%d-%m-%Y')


def find_oldest_file(dir_path, file_extension='.csv'):
    files = [os.path.join(dir_path, x) for x in os.listdir(dir_path) if x.endswith(file_extension)]
    oldest_file = min(files, key=os.path.getctime)
    return oldest_file


def log(message):
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), ':', message)


class WebCrawler:
    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path
        self.get()

    def get(self):
        log('Download data from ' + self.url)
        response = urlopen(self.url)
        data = response.read()  # a `bytes` object
        html = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
        with open(self.save_path, 'w', encoding='utf8') as fp:
            fp.write(html)


class Website:
    def __init__(self):
        self.rank = None
        self.site = None
        self.time_on_site = None
        self.views_per_visitor = None
        self.search_percent = None
        self.site_linking = None

    def show(self):
        print('Rank:', self.rank)
        print('Site:', self.site)
        print('Time On Site:', self.time_on_site)
        print('Views Per Visitor:', self.views_per_visitor)
        print('Search Percent:', self.search_percent)
        print('Linking Sites:', self.site_linking)


class VietNamWebsiteRanking:
    """
    Quy trình: Crawl html => parse => lưu csv => đọc data từ csv
    Hàm init sẽ đọc dữ liệu nếu đã có (dựa theo ngày), Nếu hôm nay đã có thì không download nữa
    mà đọc từ file.
    Ngược lại, nếu hôm nay chưa tải html, hoặc chưa parse sang csv thì làm công việc đó.
    + current_sites_rank
    + previous_sites_rank
    """

    def __init__(self, url, save_dir):
        # Khởi tạo path html_file
        # File html là file tải từ web về, chưa xử lý gì
        self.current_html_file = os.path.join(save_dir, get_today_date()) + ".html"
        # Khởi tạo path csv_file
        # File csv là file đã xử lý
        self.current_csv_file = os.path.join(save_dir, get_today_date()) + ".csv"
        # Nếu chưa có file html thì tải về
        if not os.path.exists(self.current_html_file):
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            WebCrawler(url, self.current_html_file)
            self.current_sites_rank = self.parse_html()
            self.to_csv()
            self.export()
        # Đọc current sites ranking
        self.current_sites_rank = self.read_csv(self.current_csv_file)
        # Đọc previous ranking
        self.oldest_file = find_oldest_file(save_dir, file_extension='.csv')
        if self.oldest_file == self.current_csv_file:
            log('Oh, there is no previous ranking log!')
        self.previous_sites_rank = self.read_csv(self.oldest_file)

    def parse_html(self, top=10):
        log('Parse data from {} file.'.format(self.current_html_file))
        lines = [x.strip() for x in open(self.current_html_file, encoding='utf8').read().splitlines() if
                 len(x.strip()) > 0]
        html = '\n'.join(lines)
        term = "<div class=\"td\">{}</div>"

        # get top 10
        top_items = []
        for i in range(top):
            search_result = re.search(
                r'<div class="td">({})</div>\n.+\n.+\n<a href="[^>]+>([^<]+).+\n.+\n.+\n[^\d]+([^<]+).+\n[^\d]+(['
                r'^<]+).+[^\d]+([^<]+).+[^\d]+([^<]+).+'.format(
                    i + 1), html)
            website = Website()
            website.rank = search_result.group(1)
            website.site = search_result.group(2)
            website.time_on_site = search_result.group(3)
            website.views_per_visitor = search_result.group(4)
            website.search_percent = search_result.group(5)
            website.site_linking = search_result.group(6)
            top_items.append(website)
        return top_items

    def to_csv(self):
        log('Save data to {} file'.format(self.current_csv_file))
        with open(self.current_csv_file, 'w', encoding='utf8') as fp:
            for website in self.current_sites_rank:
                fp.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    website.rank,
                    website.site,
                    website.time_on_site,
                    website.views_per_visitor,
                    website.search_percent,
                    website.site_linking
                ))

    def read_csv(self, csv_file):
        log('Read data from {} file'.format(csv_file))
        if not os.path.exists(csv_file):
            print('File Not found! Delete', self.current_html_file, 'and run again!')
            exit(0)
        top_sites = []
        try:
            for line in open(csv_file, encoding='utf8').read().splitlines():
                parts = line.split('\t')
                website = Website()
                website.rank = parts[0]
                website.site = parts[1]
                website.time_on_site = parts[2]
                website.views_per_visitor = parts[3]
                website.search_percent = parts[4]
                website.site_linking = parts[5]
                top_sites.append(website)
        except:
            print('File formal error! Delete', csv_file, 'and run again!')
            exit(0)
        return top_sites

    def export(self):
        text = open('res/template.html', encoding='utf8').read()
        text = re.sub('{date}', get_today_date(), text)
        text = re.sub('{image}', '../res/website.png', text)
        data = '<tr>{}</tr>'.format('<th>#</th><th>Site</th><th>Time on Site'
                                    '</th><th>Views Per Visitor</th><th>Search Percent</th>'
                                    '<th>Count Linking Site</th>')
        for i, item in enumerate(self.current_sites_rank):
            data += ("<tr>"
                     + "<td>{}</td>".format(i + 1)
                     + "<td>{}</td>".format(item.site)
                     + "<td>{}</td>".format(item.time_on_site)
                     + "<td>{}</td>".format(item.views_per_visitor)
                     + "<td>{}</td>".format(item.search_percent)
                     + "<td>{}</td>".format(item.site_linking)
                     + "</tr>")
        text = re.sub('{data}', data, text)
        text = re.sub('{source}', 'https://www.alexa.com/topsites/countries/VN', text)
        with open('achieves/export_web_' + get_today_date() + ".html", 'w', encoding='utf8') as fp:
            fp.write(text)


class Music:
    def __init__(self):
        self.rank = None
        self.name = None
        self.author = None

    def show(self):
        print('Rank:', self.rank)
        print('Name:', self.name)
        print('Author:', self.author)


class VietNamMusicRanking:
    """
        Quy trình: Crawl html => parse => lưu csv => đọc data từ csv
        Hàm init sẽ đọc dữ liệu nếu đã có (dựa theo ngày), Nếu hôm nay đã có thì không download nữa
        mà đọc từ file.
        Ngược lại, nếu hôm nay chưa tải html, hoặc chưa parse sang csv thì làm công việc đó.
        + current_sites_rank
        + previous_sites_rank
        """

    def __init__(self, url, save_dir):
        # Khởi tạo path html_file
        # File html là file tải từ web về, chưa xử lý gì
        self.current_html_file = os.path.join(save_dir, get_today_date()) + ".html"
        self.current_data_date = None
        # Khởi tạo path csv_file
        # File csv là file đã xử lý
        self.current_csv_file = os.path.join(save_dir, get_today_date()) + ".csv"
        # Nếu chưa có file html thì tải về
        if not os.path.exists(self.current_html_file):
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            WebCrawler(url, self.current_html_file)
            self.current_musics_rank = self.parse_html()
            self.to_csv()
            self.export()
        # Đọc current sites ranking
        self.current_musics_rank = self.read_csv(self.current_csv_file)
        # Đọc previous ranking
        self.oldest_file = find_oldest_file(save_dir, file_extension='.csv')
        if self.oldest_file == self.current_csv_file:
            log('Oh, there is no previous ranking log!')
        self.previous_musics_rank = self.read_csv(self.oldest_file)

    def parse_html(self, top=10):
        log('Parse data from {} file.'.format(self.current_html_file))
        lines = [x.strip() for x in open(self.current_html_file, encoding='utf8').read().splitlines() if
                 len(x.strip()) > 0]
        html = '\n'.join(lines)

        self.current_data_date = re.search('<h2><strong>[^>]+>([^<]+)</h2>', html).group(0).strip()
        top_items = []

        for i, founds in enumerate(re.findall(r'(<h3 class="h3"><a[^>]+>(?:[^<]+).+\n<h4.+<a[^>]+>(?:[^<]+).+)', html)):
            if i >= top:
                break
            music = Music()
            music.rank = str(i + 1)
            music.name, music.author = re.split('\n\\s*', re.sub('<[^>]*>', '', founds))
            music.name = music.name.strip()
            music.author = music.author.strip()
            top_items.append(music)
        return top_items

    def to_csv(self):
        log('Save data to {} file'.format(self.current_csv_file))
        with open(self.current_csv_file, 'w', encoding='utf8') as fp:
            for music in self.current_musics_rank:
                fp.write("{}\t{}\t{}\n".format(
                    music.rank,
                    music.name,
                    music.author
                ))

    def read_csv(self, csv_file):
        log('Read data from {} file'.format(csv_file))
        if not os.path.exists(csv_file):
            print('File Not found! Delete', self.current_html_file, 'and run again!')
            exit(0)
        top_musics = []
        try:
            for line in open(csv_file, encoding='utf8').read().splitlines():
                parts = line.split('\t')
                music = Music()
                music.rank = parts[0]
                music.name = parts[1]
                music.author = parts[2]
                top_musics.append(music)
        except:
            log('File formal error! Delete {} and run again!'.format(csv_file))
            exit(0)
        return top_musics

    def export(self):
        text = open('res/template.html', encoding='utf8').read()
        text = re.sub('{date}', self.current_data_date, text)
        text = re.sub('{image}', '../res/music.png', text)
        data = '<tr>{}</tr>'.format('<th>#</th><th>Name</th><th>Author'
                                    '</th>')
        for i, item in enumerate(self.current_musics_rank):
            data += ("<tr>"
                     + "<td>{}</td>".format(i + 1)
                     + "<td>{}</td>".format(item.name)
                     + "<td>{}</td>".format(item.author)
                     + "</tr>")
        text = re.sub('{data}', data, text)
        text = re.sub('{source}', 'https://www.nhaccuatui.com/bai-hat/top-20.nhac-viet.html', text)
        with open('achieves/export_music_' + get_today_date() + ".html", 'w', encoding='utf8') as fp:
            fp.write(text)


if __name__ == '__main__':
    if not os.path.exists('achieves'):
        os.mkdir('achieves')
    website_rank = VietNamWebsiteRanking('https://www.alexa.com/topsites/countries/VN', 'VietNam_Website_Ranking')
    # for web in r.current_sites_rank:
    #     web.show()
    #     print()
    music_rank = VietNamMusicRanking('https://www.nhaccuatui.com/bai-hat/top-20.nhac-viet.html',
                                     'VietNam_Music_Ranking')
    # for web in r.current_musics_rank:
    #     web.show()
    #     print()
    window = Tk()
    window.geometry('400x300')
    window.title("Best Then and Now")
    # Thêm label
    lbl = Label(window, text="Simply The Best", font=("Arial Bold", 25))
    lbl.configure(anchor=CENTER)
    lbl.pack()

    canvas = Canvas(window, width=128, height=128, borderwidth=2, relief="groove")
    canvas.place(bordermode=OUTSIDE, x=20, y=70)
    img = PhotoImage(file="res/like.png")
    canvas.create_image(0, 0, anchor=NW, image=img)

    lbl = Label(window, text="VietNam Website Rank", font=("Aria Bold", 15))
    lbl.place(x=170, y=70)

    rank_option = IntVar()
    rad1 = Radiobutton(window, text='Previous', value=1, variable=rank_option)
    rad2 = Radiobutton(window, text='Current', value=2, variable=rank_option)
    rad1.place(x=200, y=100)
    rad2.place(x=280, y=100)

    lbl = Label(window, text="VietNam Music Rank", font=("Aria Bold", 15))
    lbl.place(x=170, y=140)

    rad1 = Radiobutton(window, text='Previous', value=3, variable=rank_option)
    rad2 = Radiobutton(window, text='Current', value=4, variable=rank_option)
    rad1.place(x=200, y=180)
    rad2.place(x=280, y=180)


    def get_value_for_new_window():
        values = {}
        option = rank_option.get()
        if option == 1 or option == 2:
            values['title'] = '{} VietNam Website ranking'.format('Previous' if option == 1 else 'Current')
            values['image'] = 'res/website.png'
            values['items'] = [x.site for x in website_rank.previous_sites_rank] if option == 1 else [x.site for x in
                                                                                                      website_rank.current_sites_rank]
        elif option > 2:
            values['title'] = '{} VietNam Music ranking'.format('Previous' if option == 3 else 'Current')
            values['image'] = 'res/music.png'
            values['items'] = [x.name for x in music_rank.previous_musics_rank] if option == 1 else [x.name for x in
                                                                                                     music_rank.current_musics_rank]
        return values


    def preview_clicked():
        values = get_value_for_new_window()
        if not values:
            return
        viewer = Toplevel(window)
        viewer.geometry('500x600')
        viewer.title(values['title'])
        label = Label(viewer, text=values['title'], font=("Arial Bold", 20))
        label.configure(anchor=CENTER)
        label.pack()

        cv = Canvas(viewer, width=130, height=128, borderwidth=2, relief="groove")
        cv.place(bordermode=OUTSIDE, x=20, y=200)
        global img1
        img1 = PhotoImage(file=values['image'])
        cv.create_image(0, 0, anchor=NW, image=img1)
        for i, item in enumerate(values['items']):
            label = Label(viewer, text='{}. {}'.format(i + 1, item), font=("Arial Bold", 13), wraplength=300)
            label.place(x=200, y=80 + i * 50)


    def export_click():
        values = get_value_for_new_window()
        if not values:
            return
        path = ''
        option = rank_option.get()
        if option == 1:
            path = 'achieves/export_web_{}.html'.format(website_rank.oldest_file.split('\\')[-1][:-4])
            text = open(path, encoding='utf8').read()
            text = re.sub('<title>[^<]+</title>', '<title>{}</title>'.format(values['title']), text)
            text = re.sub('<h2>[^<]+</h2>', '<h2>{}</h2>'.format(values['title']), text)
            with open(path, 'w', encoding='utf8') as fp:
                fp.write(text)
        elif option == 2:
            path = 'achieves/export_web_{}'.format(website_rank.current_html_file.split('\\')[-1])
            text = open(path, encoding='utf8').read()
            text = re.sub('<title>[^<]+</title>', '<title>{}</title>'.format(values['title']), text)
            text = re.sub('<h2>[^<]+</h2>', '<h2>{}</h2>'.format(values['title']), text)
            with open(path, 'w', encoding='utf8') as fp:
                fp.write(text)
        elif option == 3:
            path = 'achieves/export_music_{}.html'.format(music_rank.oldest_file.split('\\')[-1][:-4])
            text = open(path, encoding='utf8').read()
            text = re.sub('<title>[^<]+</title>', '<title>{}</title>'.format(values['title']), text)
            text = re.sub('<h2>[^<]+</h2>', '<h2>{}</h2>'.format(values['title']), text)
            with open(path, 'w',
                      encoding='utf8') as fp:
                fp.write(text)
        elif option == 4:
            path = 'achieves/export_music_{}'.format(music_rank.current_html_file.split('\\')[-1])
            text = open(path, encoding='utf8').read()
            text = re.sub('<title>[^<]+</title>', '<title>{}</title>'.format(values['title']), text)
            text = re.sub('<h2>[^<]+</h2>', '<h2>{}</h2>'.format(values['title']), text)
            with open(path, 'w', encoding='utf8') as fp:
                fp.write(text)
        webbrowser.open(ABS_PATH.format(path))


    btn_preview = Button(window, text="Preview", command=preview_clicked)
    btn_export = Button(window, text="Export", command=export_click)
    btn_preview.place(x=60, y=240, width=100, height=40)
    btn_export.place(x=230, y=240, width=100, height=40)

    window.mainloop()
