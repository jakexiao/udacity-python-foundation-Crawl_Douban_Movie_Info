import expanddouban
import bs4
import csv
#任务1:获取每个地区、每个类型页面的URL
def getMovieUrl(category, location):
    url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category,location)
    return url
#print(getMovieUrl("动作","美国"))

#任务2: 获取电影页面 HTML
url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,动作,美国"
html = expanddouban.getHtml(url)
#print(html)

#任务3: 定义电影类
class Movie:
    def __init__(self, name,rate,location,category,info_link,cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link
    def print_data(self):
        return "{},{},{},{},{},{}".format(self.name,self.rate,self.location,self.category,self.info_link,self.cover_link)

#任务4: 获得豆瓣电影的信息
def getMovies(category, location):
    movies = []

    #for loc in location:
    url = getMovieUrl(category, location)
    html = expanddouban.getHtml(url)
    soup = bs4.BeautifulSoup(html, "html.parser")
    content = soup.find(id="app").find(class_="list-wp").find_all("a",recursive=False)
    for element in content:
        name = element.find(class_="title").string
        rate = element.find(class_="rate").string
        info_link = element.get("href")
        cover_link = element.find("img").get("src")
        movies.append(Movie(name,rate,location,category,info_link,cover_link).print_data())
    return movies
#print(getMovies("剧情","美国"))

#任务5: 构造电影信息数据表
favorite_list = []
location_list = ["中国大陆", "美国", "中国香港", "中国台湾", "日本", "韩国", "英国", "法国", "德国", "意大利", "西班牙", "印度", "泰国", "俄罗斯", "伊朗", "加拿大", "澳大利亚","爱尔兰", "瑞典", "巴西", "丹麦"]
#location_list = ["中国大陆"]
for location in location_list:
    favorite_list += getMovies("动作", location)
    favorite_list += getMovies("剧情", location)
    favorite_list += getMovies("历史", location)
#print(favorite_list)

with open("movies.csv", "w", encoding='utf-8-sig', newline="") as f:
    movies_writer = csv.writer(f, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    for favorite_movie in favorite_list:
        movie = favorite_movie.split(",", -1)
        movies_writer.writerows([movie])

#任务6: 统计电影数据
with open("movies.csv", 'r', newline='',encoding='utf_8_sig')as f:
    reader = csv.reader(f)
    texts = list(reader)
    action_count = 0
    drama_count = 0
    history_count = 0
    action_count_dict = {}
    drama_count_dict = {}
    history_count_dict = {}

for movie in texts:
    if movie[3]=="动作":
	    action_count += 1
	    if movie[2] in action_count_dict:
	        action_count_dict[movie[2]] += 1
	    else:
		    action_count_dict[movie[2]] = 1

    elif movie[3]=="剧情":
	    drama_count += 1
	    if movie[2] in drama_count_dict:
		    drama_count_dict[movie[2]] += 1
	    else:
		    drama_count_dict[movie[2]] = 1

    elif movie[3]=="历史":
	    history_count += 1
	    if movie[2] in history_count_dict:
		    history_count_dict[movie[2]] += 1
	    else:
		    history_count_dict[movie[2]] = 1
#print(history_count_dict)
sorted_action_movie_country = sorted(action_count_dict.items(),key = lambda x:x[1],reverse=True)
sorted_drama_movie_country = sorted(drama_count_dict.items(),key = lambda x:x[1],reverse=True)
sorted_history_movie_country = sorted(history_count_dict.items(),key = lambda x:x[1],reverse=True)

def find_three(sorted_dict,movies_qty,movies_cate_qty):
    count = 0
    for key,value in sorted_dict:
       count += 1
       if count <=3:
            country_rate = round(movies_qty[key]/movies_cate_qty*100,2)
            country_key = key
            return country_key,country_rate

with open('output.txt', 'w', encoding='utf-8') as f:
    print('动作电影前三名及比例{}%'.format(find_three(sorted_action_movie_country,action_count_dict,action_count)),file = f)
    print('剧情电影前三名及比例{}%'.format(find_three(sorted_drama_movie_country,drama_count_dict,drama_count)),file = f)
    print('历史电影前三名及比例{}%'.format(find_three(sorted_history_movie_country,history_count_dict,history_count)),file = f)
