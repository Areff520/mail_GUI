import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,QDateTime

import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import re
import os

Text_mail = ''
ASIN = ''
EAN = ''
vendorID = ''
title = ''
mail_label = ''
count = 0


class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("start.ui", self)

        self.button_vendor_first_contact.clicked.connect(self.clicked_VFC)
        self.button_soft_pull.clicked.connect(self.clicked_SP)
        self.button_reminder.clicked.connect(self.clicked_R)
        self.buton_multiple_asins.clicked.connect(self.clicked_MA)
        self.button_no_stock.clicked.connect(self.clicked_NS)
        self.current_count=0
    def gotovendor(self):
        if self.current_count==0:
            login = VendorScreen()
            widget.addWidget(login)
            login1 = ResultScreen()
            widget.addWidget(login1)
            self.current_count+=1

        widget.setCurrentIndex(widget.currentIndex() + 1)

    def clicked_VFC(self):
        global Text_mail
        Text_mail = """Merhaba,

Asin: ASIN
Ean: EAN
Ürün Adı: title
Ürün Linki: https://www.amazon.com.tr/dp/ASIN

Yukarıda bilgilerini paylaştığım ürün ile ilgili ulaşmaktayım. Müşterilerimizden aldığımız geri bildirime göre, xxx. Müşteri geri bildirimini depolarımızda teyit ettirebildik. Satış sayfasındaki bilgileri teyit etmenizi rica ederim. 
"""
        self.gotovendor()

    def clicked_SP(self):
        global Text_mail
        Text_mail = """Merhaba, 

Asin: ASIN
Ean: EAN
Ürün Adı: title
Ürün Linki: https://www.amazon.com.tr/dp/ASIN
Yukarıda bilgilerini paylaştığım ürünle ilgili olarak ürünün iade oranlarının normalin üstüne çıkması sebebiyle ulaşıyoruz. Bu ürünle ilgili bir sorun olup olmadığını anlamak amacıyla yukarıda paylaşılan linkten ürünün katalog sayfasına ulaşmanızı, ürün detaylarını ve müşteri yorumlarını kontrol etmenizi rica ederiz. 

Sorunun hızlı bir şekilde çözülebilmesi için aşağıdaki sorulara cevap vermenizi önemle rica ederiz. 

• Ürünün bilinen kronik bir problemi var mıdır?
• Belirtilen ürün için tarafınıza iade gelen ürünlerin yüzde oranını paylaşabilir misiniz?
• Ürünün detay sayfasını veya müşteri yorumlarını incelediğinizde bir sorun tespit edebildiniz mi? Eğer ettiyseniz konuyla ilgili bilgilendirmenizi rica ederiz.
• Sorun müşteri yanlış anlamasından kaynaklanıyor ise müşterilere yardımcı olabilmek adına satış sayfasına girebileceğimiz bir kullanım talimatı veya yardımcı bir bilgi iletmenizi rica ederim.

Bu konu yüksek önem düzeyinde müşteri problemi olması sebebiyle en geç 12 saat içerisinde bu maili cevaplayarak dönüş yapılması rica ederiz.
"""

        self.gotovendor()

    def clicked_R(self):
        global Text_mail
        Text_mail = """Merhaba,

Barkod: EAN
Asin: ASIN
Link: https://www.amazon.com.tr/dp/ASIN
Müşteri Şikayeti: 

Müşterimiz yukarıda bilgileri bulunan ürün için tekrar eden hasar bildiriminde bulunmuştur. Müşterimizin ilk siparişinde ve değişim için verdiği 2. siparişte de ürünün aynı hasarla tarafına ulaştığını belirtmiştir.

Sorunun hızlı bir şekilde çözülebilmesi için aşağıdaki sorulara cevap vermenizi önemle rica ederiz.

•Müşterilerin belirttiği gibi ürünün kronik bir sorunu bulunmakta mıdır? Sorun müşteri yanlış anlamasından kaynaklanıyor ise müşterilere yardımcı olabilmek adına satış sayfasına girebileceğimiz bir kullanım talimatı veya yardımcı bir bilgi iletmenizi rica ederim.
•Belirtilen ürün için tarafınıza iade gelen ürünlerin yüzde oranını paylaşabilir misiniz?

Bu konu yüksek önem düzeyinde müşteri problemi olduğundan en geç 12 saat içerisinde dönüş yapılması rica ederiz.
"""

        self.gotovendor()

    def clicked_MA(self):
        global Text_mail
        Text_mail = """Hello,

The XXX vendor's product with ASIN Asin has been reported to Andon Cord due to customer complaints. Customers are receiving an error message on the checkout page stating "this product cannot be shipped to the specified addresses". When we investigated the issue, we found that the Asin could not be shipped to any address, so all of the customers are unable to buy this product. We have implemented the methods determined to solve the problem, but the Asin is still giving an error. Since Andon Cord has been notified constantly about the problem for a long time and in order to stop the inconvenience of customers, I request that you to Boss the Asin.

Regards,

"""

        self.gotovendor()

    def clicked_NS(self):
        global Text_mail
        Text_mail = """Merhaba,

Asin: ASIN
Ean: EAN
Ürün Adı: title
Ürün Linki: https://www.amazon.com.tr/dp/ASIN

Yukarıda bilgilerini paylaştığım ürün ile ilgili ulaşmaktayım. Müşterilerimizden aldığımız geri bildirime göre, müşterilerimize ulaşan ürün ile satış sayfasındaki bilgiler birbiriyle uyuşmamaktadır. Maalesef ki ürünümüz stoklarda kalmadığı için sorunu inceleyemiyoruz, bu yüzden sizin yardımınıza ihtiyacımız var. Ürün bilgilerini teyit etmenizi rica ederim.
"""

        self.gotovendor()


class VendorScreen(QDialog):
    def __init__(self):
        super(VendorScreen, self).__init__()
        loadUi("vendor.ui", self)
        self.go_button.clicked.connect(self.selenium_go)
        self.back_button.clicked.connect(self.back_button_clicked)
    def gotoResult(self):

        widget.setCurrentIndex(widget.currentIndex() + 1)

    def back_button_clicked(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def seleniumm(self):
        profile_name = 'Mail_Automation'
        profile_path = rf'{os.path.expanduser("~")}\Chrome Profiles\{profile_name}'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-data-dir={profile_path}')
        chrome_options.add_argument(f'--profile-directory={profile_name}')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome( options=chrome_options)

    def selenium_go(self):
        global count
        if count == 0:
            count += 1
            self.seleniumm()


        try:
            print('at selenium_go stage')
            global ASIN
            global EAN
            global vendorID
            global title
            global mail_label

            vendorID = ''
            ASIN = ''
            EAN = ''
            title = ''
            mail_label = ''
            Ticket = self.ticketid_field.text()

            self.driver.get(f'https://t.corp.amazon.com/{Ticket}/communication')
            WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "plain-text-display")))

            try:
                EAN_source = re.search(r'\nEAN : \w{13}', self.driver.page_source)
                EAN_code = EAN_source.group()
                EAN = EAN_code[6:19]

                ASIN_source = re.search(r'\nASIN: \w{10}', self.driver.page_source)
                ASIN_code = ASIN_source.group()
                ASIN = ASIN_code[7:17]
            except:
                print('Ticket information automation did not work.')
                ticket_title = self.driver.find_element(By.ID, 'sim-title')
                ASIN = re.findall('B\w{9}', ticket_title.text)
                if type(ASIN)==list and len(ASIN)>0:
                    if 'B' not in ASIN[0]:
                        ASIN = re.findall('\d{10}', ticket_title.text)
                        print(ASIN)
                        ASIN = ASIN[0]
                    else:
                        ASIN = ASIN[0]
                    print('ASIN is ;', ASIN)
                else:
                    if 'B' not in ASIN:
                        ASIN = re.findall('\d{10}', ticket_title.text)
                        print(ASIN)
                        ASIN = ASIN[0]
                    else:
                        ASIN = ASIN
                    print('ASIN is ;', ASIN)
            self.driver.get(f'https://www.amazon.com.tr/dp/{ASIN}')
            title_info = self.driver.find_element(By.ID, 'productTitle')
            title = title_info.text
            print('Title is;', title)
            self.driver.get(
                f'https://procurementportal-eu.corp.amazon.com/bp/asin?asin={ASIN}&lei=141&marketplaceid=A33AVAJ2PDY3EV&dateRange=lastYear&conditions=Submitted%2CCompletelyConfirmed%2CComplete')
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "react-grid-Container")))

            vendorID_source = re.findall(f'(?:href="/bp/vendor\?vendorCodes=)(\w\w\w\w\w)(?:">)',
                                         self.driver.page_source)
            vendor_dict = {}
            score = 1
            prev_vendor = ''
            for vendorID in vendorID_source:
                vendor_dict[vendorID] = score
                if prev_vendor == vendorID:
                    score += 1
                    vendor_dict[vendorID] = score
                else:
                    score = 0
                    prev_vendor = vendorID
            print('vendor dict is:', vendor_dict)

            score = 0
            for x in vendor_dict:
                if score < vendor_dict[x]:
                    score = vendor_dict[x]
                    vendorID = x
            print('vendorID and title is,', vendorID, title)
            if vendorID == '':
                print('No vendor ID, probably no retail offer.')
            else:
                self.driver.get(f'https://scip.corp.amazon.com/contacts/vendorcode/{vendorID}')
                b = self.driver.find_element(By.CLASS_NAME, 'smallBottomMargin')
                b = b.text.split()
                b = b[11:]
                text = ''
                text_list = []
                mail_list = []
                for content in b:
                    text = text + content + ' '
                    if content == 'ADDRESS':
                        text_list.append(text)
                        text = ''
                for contents in text_list:
                    if 'Primary Account' in contents:
                        mail = re.findall('(?:Account Rep ).*?(?: ADDRESS)', contents)
                        mail = mail[0].split()
                        mail = mail[6]
                        mail_list.append(mail)
                    elif 'Catalog' in contents:
                        mail = re.findall('(?:Catalog ).*?(?: ADDRESS)', contents)
                        mail = mail[0].split()
                        mail = mail[5]
                        mail_list.append(mail)
                vendor_mail = set(mail_list)
                vendor_mail = list(vendor_mail)
                for vendor in vendor_mail:
                    if '@' in vendor:
                        mail_label = mail_label + vendor + ';'
                if len(mail_label) < 5:
                    mail_label = vendorID
                self.ticketid_field.clear()
                # changing widget

        except Exception as e:
            print('Automation failed at one point', traceback.format_exc())
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ResultScreen(QDialog):

    def __init__(self):
        global Text_mail
        global ASIN
        global EAN
        global title
        global mail_label
        global vendorID

        super(ResultScreen, self).__init__()
        loadUi("sayfa3.ui", self)

        self.info = Text_mail.replace('ASIN', ASIN).replace('EAN', EAN).replace('title', title).replace('XXX',vendorID)
        subject = (f'Amazon.com.tr Ürün Teyidi ASIN: {ASIN}')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatele)
        self.timer.start(1)



        self.subject_label.setText(subject)
        self.label.setText(self.info)
        self.mail_label.setText(mail_label)



        self.copy_mail.clicked.connect(self.copyToClipboard_mail)
        self.copy_subject.clicked.connect(self.copyToClipboard_subject)
        self.copy_button.clicked.connect(self.copyToClipboard_button)
        self.another_button.clicked.connect(self.go_another)

    def updatele(self):
        self.info = Text_mail.replace('ASIN', ASIN).replace('EAN', EAN).replace('title', title).replace('XXX',vendorID)
        subject = (f'Amazon.com.tr Ürün Teyidi ASIN: {ASIN}')
        self.label.setText(self.info)
        self.mail_label.setText(mail_label)
        self.subject_label.setText(subject)

        QtGui.QGuiApplication.processEvents()
        self.subject_label.repaint()
        self.label.repaint()
        self.label.adjustSize()

    def copyToClipboard_mail(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.mail_label.text(), mode=cb.Clipboard)

    def copyToClipboard_subject(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.subject_label.text(), mode=cb.Clipboard)

    def copyToClipboard_button(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.label.text(), mode=cb.Clipboard)

    def go_another(self):
        # self.subject_label.clear()
        # self.label.clear()
        # self.mail_label.clear()

        widget.setCurrentIndex(widget.currentIndex() - 2)






# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(650)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec_())

except:
    print("Exiting")


