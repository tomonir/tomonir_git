from bs4 import BeautifulSoup
import requests


url = 'https://namazvakitleri.diyanet.gov.tr/de-DE/10327/gebetszeit-fur-villingen-schwen'
output_html_file_location = "./html/table-10/"




class HTMLParser:
    def __init__(self):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text,'lxml')

    def get_prayer_list(self):
        return self.soup.find_all("div",class_='tpt-title')
    def get_prayerTime_list(self):
        return self.soup.find_all("div",class_='tpt-time')
    def get_date_of_prayer_list(self):
        return self.soup.find_all("div",class_='ti-miladi')

    def get_active_list(self):
        return self.soup.find_all("div",class_='active-tpt-cell')



class ContentMaker:
    def __init__(self):
        with open(output_html_file_location+"template.html", "r", encoding='utf-8') as f:
            self.html_text= f.read()



    def get_html_page(self):

        #print (parser.get_active_list())

        self.html_text = self.html_text.replace("$PRAYERCONTENT",contentMaker.makePrayerContent(parser.get_prayer_list(),parser.get_prayerTime_list()))
        self.html_text = self.html_text.replace("$DATECONTENT", contentMaker.makeDateContent(parser.get_date_of_prayer_list()))
       
        self.write_to_a_file(output_html_file_location+'index.html',self.html_text)

    def get_html_prayerDate_content(self,date):
        html_txt = ''
        bg_style= 'bg-info'
        html_txt= "<tr class=\""+bg_style+"\">"
        html_txt+= "<td style=\"text-align: center;font-size:300%;font-family: 'Orbitron', sans-serif;\">"+date+"</td>"
        html_txt+= "</tr>"
        return html_txt

    def get_html_remainingTime_content(self,time):
        html_txt = ''
        html_txt+= "<td style=\"text-align: center;font-size:300%;font-family: 'Orbitron', sans-serif;\">"+time+"</td>"
        return html_txt

    def write_to_a_file(self,file_name,content):
        f = open(file_name, "w")
        f.write(content)
        f.close()

    def get_html_prayer_content(self,id,prayerType,time):

        html_txt = ''
        if (time==''):
            return html_txt
        
        if (id%2==0):
            bg_style= 'bg-info'
        else:
            bg_style= 'bg-success'


        if (id <7):
        #print (prayerType)
            html_txt= "<tr class=\""+bg_style+"\">"
            html_txt+= "<td style=\"font-size:300%;font-family: 'Orbitron', sans-serif;\">"+prayerType+"</td>"
            html_txt+= "<td style=\"font-size:300%;font-family: 'Orbitron', sans-serif;\">"+time+"</td>"
            html_txt+= "</tr>"

        return html_txt
				     

    def makePrayerContent(self,prayer_list,prayerTime_list):

        html_content= "<table class='table table-dark'><thead><tr class='bg-dark'><th></th><th></th></tr></thead><tbody>"

        id = 0
        for prayer, time in zip (prayer_list,prayerTime_list):
            #print(prayer.text, time.text)
            html_content+=self.get_html_prayer_content(id,prayer.text,time.text)
            id+=1
        html_content+="</tbody>"

        return html_content

    def makeDateContent(self,date_of_prayer_list):
        html_content=""
        for prayerDate in date_of_prayer_list:
            html_content = self.get_html_prayerDate_content(prayerDate.text)
        return html_content








if __name__ == "__main__":
    parser = HTMLParser()

    contentMaker = ContentMaker()
    contentMaker.get_html_page()
    

