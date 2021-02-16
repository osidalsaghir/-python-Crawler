import os
import scrapy
import datetime
import threading
import datetime
import json


class AuthorSpider(scrapy.Spider):
    name = 'n11product'
    timeAndDateNow = str(datetime.datetime.now()).replace(" ","_").replace(".","").replace(":",".")
    start_url = 'https://www.n11.com/cok-satanlar'

    def start_requests(self):
        # ***************************************
        #***************************************
        self.refactoringJsonFile('n11product\\products_'+ self.timeAndDateNow +'.json')
        fileNames={"n11product\\products_"+ self.timeAndDateNow +".txt" , "n11product\\products_urls_"+ self.timeAndDateNow +".txt" }
        self.refactoringTextFiles(fileNames)
        # ***************************************
        # ***************************************
        yield scrapy.Request(url=self.start_url, callback=self.parse)





    def parse(self, response):
        for newUrl in response.css('div.tab.categoryMenuTab ul li'):
            theNewUrlToVisit = newUrl.css('a').attrib['href']
            if theNewUrlToVisit == self.start_url:
                pass
            else:
                yield scrapy.Request(url=theNewUrlToVisit, callback=self.parseUrls)

    def parseUrls(self , response):
        for newUrl in response.css('li.column'):
            theNewUrlToVisit = newUrl.css('div.columnContent div.pro a').attrib['href']
            toBeSavedUral = theNewUrlToVisit + "\n"
            self.writtingToFile(toBeSavedUral, "n11product\\products_urls_"+ self.timeAndDateNow +".txt")
            yield scrapy.Request(url=theNewUrlToVisit, callback=self.parseData)


    def parseData(self, response):

        proTitle = str(response.css('h1.proName::text').get()).strip()
        proPrice= str(response.css('div.newPrice ins::text').get()).strip()
        if proTitle == "None":
            proTitle = str(response.css('h1.pro-title_main::text').get()).strip()
        if proPrice == "None":
            proPrice = str(response.css('span.price-amount::text').get()).strip()

        jsonTitle = proTitle
        proTitle = str(proTitle + " : "+proPrice+" " + "TL" + "\n")

        y = threading.Thread(target=self.writtingToFile, args=(proTitle,  "n11product\\products_"+ self.timeAndDateNow +".txt"))
        y.start()

        productInfo =  {
                "Product Title": jsonTitle,
                "Product Price": proPrice,
                "Product URL": response.url,
                "Last Update Time": str(datetime.datetime.now().time())
            },

        self.writtingToJsonFile(productInfo,"n11product\\products_"+ self.timeAndDateNow +".json")





    def writtingToFile(self, content , filename):
        with open(filename, 'ab') as f:
            try:
                f.write(content.encode("utf-8"))
                f.close()
            except Exception as e:
                print(e)


    def writtingToJsonFile(self,content ,filename):
        with open(filename,'r+') as j:
            try:
                data = json.load(j)
                temp = data["products"]
                temp.append(content)
                j.seek(0)
                json.dump(data, j)
            except Exception as e:
                print(e)

        j.close()

    def refactoringJsonFile(self,fileName):
        if os.path.exists(fileName):
            os.remove(fileName)
            with open(fileName, 'w+') as j:
                data = {
                    "products": [
                    ]
                }
                try:
                    json.dump(data, j)
                except Exception as e:
                    print(e)

            j.close()
        else:
            with open(fileName, 'w+') as j:
                data = {
                          "products": [
                          ]
                        }
                try:
                    json.dump(data, j)
                except Exception as e:
                    print(e)

            j.close()

    def refactoringTextFiles(self,fileNames):
        for file in fileNames :
            if os.path.exists(file):
                os.remove(file)
                with open(file, 'w+') as j:
                    try:
                        j.write("")
                    except Exception as e:
                        print(e)
                j.close()
            else:
                with open(file, 'w+') as j:
                    try:
                        j.write("")
                    except Exception as e:
                        print(e)

                j.close()