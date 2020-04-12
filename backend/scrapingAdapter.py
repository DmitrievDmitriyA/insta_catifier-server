
import sys
import os
sys.path.append(os.path.abspath('..\\'))
import insta_catifier.catifier.scraping as scraping


def scrapePhotos(userName):
    sys.argv[1] = userName
    print(sys.argv[1])
    sourceUserFolder = 'C:\\Users\\frank\\Desktop\\insta_sources\\' + userName + '\\'
    scraping.scrape_photos(sourceUserFolder)
    print("ANd now here")
