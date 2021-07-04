import requests
from bs4 import BeautifulSoup
import csv
import json


# a fost selectata DATA FONDĂRII F.R.S. / DATE OF RCF’S SETTING UP: 04.01.1925

#CAMPIONATELE NAŢIONALE DE SENIORI/NATIONAL CHAMPIONSHIPS FOR MEN -> incepe cu unu cu data de 1926
if __name__ == '__main__':

   
    page = requests.get('http://frsah.ro/index.php/file-de-istorie-1/') # extragere pagina
    soup = BeautifulSoup(page.content, features='html.parser') # setam parser
    table =  soup.find("div", class_ ="td-page-content").find("table", class_="file") # obtinem tabela
    table_rows = table.find_all("tr") # obtine randurile de la tabela

    list_of_lines = []
    for row in table_rows:
        text_from_tds = [
            td.get_text() for td in row.find_all('td')
        ]
        list_of_lines.append(text_from_tds)
    
    
    
    f1 = open('data.csv','w',  encoding='UTF8')
    writer =  csv.writer(f1)

    for row in list_of_lines:
        writer.writerow(row)
   
    f1.close()



    f2 = open('data.json','w')
    json.dump(list_of_lines, f2, indent=2)
    f2.close()


    print(list_of_lines) 
