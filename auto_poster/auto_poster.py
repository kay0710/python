from arti_crawl import article_crawler

site_list = {"cnn": "cnn", "h_cs": "h_cs"}
arti_subject = ("fitness", "food", "sleep", "mindfulness", "relationships")
dirName = "articles"

ac = article_crawler(arg_site=site_list['cnn'], arg_subject=arti_subject, 
                  arg_category="fitness", arg_dirName=dirName)

tmp = ac.get_article()
print("<<tmp>>")
print(tmp)