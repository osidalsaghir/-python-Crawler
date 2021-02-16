import os
import scrapy
import threading
import datetime
import json


class AuthorSpider(scrapy.Spider):
    name = 'TopRatedMovies'
    timeAndDateNow = str(datetime.datetime.now()).replace(" ","_").replace(".","").replace(":",".")
    start_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

    def start_requests(self):
        print(self.timeAndDateNow)
        # ***************************************
        #***************************************
        self.refactoringJsonFile('TopRatedMovies\\films_'+ self.timeAndDateNow +'.json')
        fileNames={"TopRatedMovies\\films_"+ self.timeAndDateNow +".txt" , "TopRatedMovies\\films_urls_"+ self.timeAndDateNow +".txt" }
        self.refactoringTextFiles(fileNames)
        # ***************************************
        # ***************************************
        yield scrapy.Request(url=self.start_url, callback=self.parse)





    def parse(self, response):
        print("\n\n\n\n\nhere\n\n\n\n\n")
        for newUrl in response.css('table.chart.full-width tbody.lister-list tr'):
            theNewUrlToVisit =str(newUrl.css('td.titleColumn a').attrib['href'])
            theNewUrlToVisit = "https://www.imdb.com/"+theNewUrlToVisit
            self.writtingToFile(theNewUrlToVisit + "\n", 'TopRatedMovies\\films_urls_'+ self.timeAndDateNow +'.txt')
            yield scrapy.Request(url=theNewUrlToVisit, callback=self.parseData)




    def parseData(self, response):

        filmTitle = str(response.css('div.title_wrapper h1::text').get()).strip()
        director= str(response.css('div.credit_summary_item a::text').get()).strip()
        rate = str(response.css('div.ratingValue strong span::text').get()).strip()
        rate = rate + "/10"

        toBeSavedString = str(filmTitle + " Directed By "+director+" Rated as "+rate+"\n")

        y = threading.Thread(target=self.writtingToFile, args=(toBeSavedString,  "TopRatedMovies\\films_"+ self.timeAndDateNow +".txt"))
        y.start()

        fimetInfo ={
                "film Title": filmTitle,
                "rate" : rate,
                "director": director,
                "film IMDb URL": response.url,
                "Last Update Time": str(datetime.datetime.now().time())
            },

        self.writtingToJsonFile(fimetInfo,"TopRatedMovies\\films_"+ self.timeAndDateNow +".json")





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
                temp = data["films"]
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
                    "films": [
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
                          "films": [
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