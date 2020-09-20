from bs4 import BeautifulSoup
import requests
import datetime

# レバテックフリーランスにアクセスしてコンテンツの取得
html = requests.get('https://freelance.levtech.jp/')
soup = BeautifulSoup(html.text, 'lxml')

# ページトップの言語別の求人数の情報を取得
langJobs = soup.find('div', {'class': 'searchTab__body js-tabContent is-active'})
jobs = langJobs.find_all('li', {'class': 'searchLinkList__item'})

# テキストファイルへ言語別の求人情報を書き込み
# TODO: CSVで1ファイル管理
dt = datetime.datetime.now()
formatted = dt.strftime('%Y%m')
fileName = formatted + "jobs.txt"

with open(fileName, 'w') as f:
    for job in jobs:
        print(str(job.find('a').contents), end=",", file=f)
        print(str(job.find('span').contents), file=f)

# PHPの求人ページで単価を取得 (1ページ目)
phpPage = requests.get('https://freelance.levtech.jp/project/skill-5/')
soup = BeautifulSoup(phpPage.text, 'lxml')

jobTitles = soup.find_all('a', {'class': 'js-link_rel'})
jobRewards = soup.find_all('li', {'class': 'prjContent__summary__price'})
jobSkills = soup.select(
    'ul.prjTable > li:nth-child(3) > p.prjTable__item__desc.js-highlightArea')

fileName = formatted + "php.txt"


f = open(fileName, 'w')
for i in range(20):
    f.write(str(jobTitles[i].text) + ',')
    reward = int(jobRewards[i].find('span').text.replace(',', '').replace('円', ''))
    if reward < 100000:
        reward = reward * 160
    f.write(str(reward) + ',')
    f.write(str(jobSkills[i].contents) + '\n')

# PHPの求人ページで単価を取得 (2ページ目以降)
try:
    for i in range(2, 150):
        phpPage = requests.get(
            'https://freelance.levtech.jp/project/skill-5/' + 'p' + str(i) + '/')
        soup = BeautifulSoup(phpPage.text, 'lxml')
        jobTitles = soup.find_all('a', {'class': 'js-link_rel'})
        jobRewards = soup.find_all(
            'li', {'class': 'prjContent__summary__price'})
        jobSkills = soup.select(
            'ul.prjTable > li:nth-child(3) > p.prjTable__item__desc.js-highlightArea')

        for j in range(20):
            f.write(str(jobTitles[j].text) + ',')
            reward = int(jobRewards[j].find('span').text.replace(',', '').replace('円', ''))
            if reward < 100000:
                reward = reward * 160
            f.write(str(reward) + ',')
            f.write(str(jobSkills[j].contents) + '\n')

        print(i)

except Exception as e:
    print(str(i) + 'ページで処理が終了')
    print(e)

f.close()
