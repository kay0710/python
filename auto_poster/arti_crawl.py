import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

class article_crawler():
    def __init__(self, arg_site=None, 
                 arg_subject=("fitness", "food", "sleep", "mindfulness", "relationships"), 
                 arg_category=None,
                 arg_dirName="article"): # arg_url=None
        # super().__init__(**kwargs)
        self.site = arg_site
        self.subject = arg_subject
        self.category = arg_category
        self.dirName = arg_dirName
        # self.url = arg_url
        self.now = str(datetime.now().strftime("%Y_%m_%d"))
        self.browser = webdriver.Chrome()
        time.sleep(2)
        
    # def ad_closer(self):
    #     post_page = self.browser.find_elements(By.ID, "bx-close-inside-2133287")
    #     for i, href in enumerate(post_page):
    #         if i == 0:
    #             href.click()
    #             print("log: pop-up is closed.")
    #         else:
    #             print("None")
    
    # get text
    def get_article(self):
        # arg_url = self.url
        tmp_txt = None
        site_browser = self.browser
        news_site = self.site
 
        url_dict = {"cnn": "https://edition.cnn.com/health", 
                    "h_cs": "https://health.chosun.com/list.html?menu=01010107&nowcode=01010107&pn=1"}
        site_browser.get(url_dict[news_site])
        site_browser.maximize_window()
        
        if news_site == "cnn":
            cnn_subject = self.subject
            cnn_category = self.category
            print("log: " + cnn_category + " is selected")
            time.sleep(2)
            
            find_category = site_browser.find_elements(By.CLASS_NAME, "header__nav-item-link")
            
            # access to article
            for i, href in enumerate(find_category):
                if i == 0:
                    pass
                elif i == 1:
                    if cnn_category == cnn_subject[0]:
                        href.click()
                        site_browser.minimize_window()
                        break
                    else:
                        pass
                elif i == 2:
                    if cnn_category == cnn_subject[1]:
                        href.click()
                        site_browser.minimize_window()
                        break
                    else:
                        pass
                elif i == 3:
                    if cnn_category == cnn_subject[2]:
                        href.click()
                        site_browser.minimize_window()
                        break
                    else:
                        pass
                elif i == 4:
                    if cnn_category == cnn_subject[3]:
                        href.click()
                        site_browser.minimize_window()
                        break
                    else:
                        pass
                elif i == 5:
                    if cnn_category == cnn_subject[4]:
                        href.click()
                        site_browser.minimize_window()
                        break
                    else:
                        pass
                else:
                    print("Error: No Category Matched")

            # article crawling                    
            copy_article = site_browser.find_elements(By.CLASS_NAME, 'article__content')
            for i, paragraph in enumerate(copy_article):
                print("log: [article] >> " + paragraph.text)
                print("log: [legth] >> " + len(paragraph.text))
                tmp_txt = paragraph.text
                site_browser.quit()
            
            return tmp_txt
            # return paragraph.text
            
        elif news_site == "h_cs":
            site_browser.minimize_window()
            
        else:
            pass
        
    def txt_saver(self):
        save_now = self.now
        article_dirName = self.dirName
        
        if not os.path.exists(article_dirName):
            os.mkdir(article_dirName)
        
        with open(article_dirName + '/' + save_now + ".txt", "w", encoding='utf-8') as f:
            f.write(article_crawler.get_article())
            print("Complete save txt file:" + save_now)

