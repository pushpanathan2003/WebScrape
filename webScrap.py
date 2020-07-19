import requests
from bs4 import BeautifulSoup
import pandas as pd


@plac.annotations(
    url=("base url", "option", "f", str),
    output_dir=("output directory. Location to save the file", "option", "o", str),
   
)

def main(url,output_dir):
    #get html source
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    #finding the corresponding pattern
    mydivs = soup.findAll("div", {"class": ["col-10 text-left"]})
    mydivs=mydivs[1]
    mydivs=mydivs.find_all("p")
    
    #extracting pdf link
    link=[]
    seclink=[]
    finlink=[]
    for i in range(len(mydivs)):
        url=url+mydivs[i].find("a")['href']
        link.append(url)
        seclink.append(mydivs[i].find("a").contents)
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        table=soup.find('table')
        finlink.append(url+table.find('tr').find('a')['href'])

    
    data = {'filename':seclink, 'link':link,'doc':finlink}
    df=pd.DataFrame(data) 
    df.to_csv(output_dir,index=False,encoding='utf-8')
    

if __name__ == "__main__":
    plac.call(main)
    


#Run: python scra.py -f "https://www.privacy.gov.ph/memorandum-circulars/" -o '/output.csv'
