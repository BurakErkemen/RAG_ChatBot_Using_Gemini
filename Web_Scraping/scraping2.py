
from bs4 import BeautifulSoup
import requests
from fpdf import FPDF

url = 'https://yazilimtf.firat.edu.tr/academic-staffs'

response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
pdf = FPDF()
pdf.add_page()
pdf.add_font("ArialUnicode", fname=r"C:\Users\burak\Downloads\ArialUnicodeMSRegular\ArialUnicodeMSRegular.ttf")        
pdf.set_font("ArialUnicode", size=12)  # Bu satır eklenmiş


element_main = soup.select('.personnel-card-info-abs-link')

for main_element in element_main:
    # Bağlantı URL'sini bulma
    link_element = main_element.find('a')
    if link_element:
        link_url = link_element.get('href')

        # Bağlantıya istek yapma
        inner_response = requests.get(link_url, verify=False)
        inner_soup = BeautifulSoup(inner_response.text, 'html.parser')

        # Gerekli bilgileri çekme
        profile_div = inner_soup.find('div', class_='profile')
        institution = profile_div.find('span', text='Kurum Bilgileri :').find_parent('div').find('p').get_text(strip=True).replace(" ", "").replace("\n", "")
        title = profile_div.find('h4').get_text(strip=True)
        name = profile_div.find('h2').get_text(strip=True)
        expertise = profile_div.find('p', id='uzmanlik_text').get_text(strip=True)
        yok_ID = profile_div.find('span', text='Kurum Bilgileri :').find_next('span').find_next('p').get_text(strip=True)

        # Sonuçları yazdır
        print( institution)
        print("Ünvan:", title)
        print("Ad:", name)
        print(expertise)
        print(yok_ID)

        pdf.cell(200, 10, txt= institution, ln=True)
        pdf.cell(200, 10, txt="Ünvan: " + title, ln=True)
        pdf.cell(200, 10, txt="Ad: " + name, ln=True)
        pdf.cell(200, 10, txt= expertise, ln=True)
        pdf.cell(200, 10, txt= yok_ID, ln=True)
        pdf.cell(200, 10, txt="", ln=True)  # Satır boşluğu ekleyerek bir sonraki profili ayır



from lxml import etree
url_ann = "https://yazilimtf.firat.edu.tr/announcements-all/1"

# Sayfayı indir
response = requests.get(url_ann, verify=False)

# BeautifulSoup kullanarak HTML'i parse et
soup = BeautifulSoup(response.content, 'html.parser')

pages_div = soup.find('div', id='pages')


# BeautifulSoup objesini lxml.etree.Element ile dönüştürme
root = etree.HTML(str(pages_div))

last_page_link = root.xpath('//*[@id="pages"]/a[@class="more-button"]/following-sibling::a')[0]
last_page_text = last_page_link.text

for link_num in range(1,int(last_page_text) + 1):
    url_page = f"https://yazilimtf.firat.edu.tr/announcements-all/{link_num}"

    response = requests.get(url_page,verify=False)

    soup = BeautifulSoup(response.content, 'html.parser')


    element_main = soup.select('.news-section-card.mb-3')

    for main_element in element_main:
        # Bağlantı URL'sini bulma
        link_elements = main_element.find_all('a')
        for link_element in link_elements:
            link_url = link_element.get('href')

            # Bağlantıya istek yapma
            inner_response = requests.get(link_url, verify=False)
            inner_soup = BeautifulSoup(inner_response.text, 'html.parser')

            # Gerekli bilgileri çekme
            annoc_div = inner_soup.find('div', class_='index-content-info')
            date = annoc_div.find('div', class_='new-section-detail-date').get_text(strip=True).replace(" ", "").replace("\n", "")
            title = annoc_div.find('div', class_='new-section-detail-title').get_text(strip=True)
            content = annoc_div.find('div', class_='new-section-detail-explanation').get_text(strip=True)

            print(date)
            print(title)
            print(content)
            print("\n")

            pdf.cell(200, 10, txt="Title: " + title, ln=True)
            pdf.cell(200, 10, txt="Content: " + content, ln=True)
            pdf.cell(200, 10, txt= "Date: " + date, ln=True)
            pdf.cell(200, 10, txt="", ln=True)  # Satır boşluğu ekleyerek bir sonraki profili ayır



# PDF dosyasını kaydet
pdf_file_path = "D:/GitHub/RAG_ChatBot_Using_Gemini/faculty_information2.pdf"
pdf.output(pdf_file_path)

print("PDF dosyası oluşturuldu:", pdf_file_path)