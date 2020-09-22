from bs4 import BeautifulSoup
import requests
import datetime


# ########## variables ##########

# レバテックサイトトップのURL
siteUrl = 'https://freelance.levtech.jp/'

# レバテックサイトトップ 言語別求人数ボックス class名
languageJobsBox = 'searchTab__body js-tabContent is-active'
languageJobsList = 'searchLinkList__item'

# レバテックPHPの求人ページ
phpJobsUrl = 'https://freelance.levtech.jp/project/skill-5/'

# PHP求人ページの求人カード内のwebエレメント
jobTitleAnchorClass = 'js-link_rel'
jobRewardListClass = 'prjContent__summary__price'
jobSkillParagraphSelector = 'ul.prjTable > li:nth-child(3) > p.prjTable__item__desc.js-highlightArea'

# htmlタグ名
anchorTag = 'a'
spanTag = 'span'
divTag = 'div'
listTag = 'li'
classAttribute = 'class'

# 稼働時間
monthlyHours = 160

# forループ
loops = 20

# 時間単価か月額報酬かどうかを判定する金額
hourlyWageFlag = 100000

# 求人ページ数
second = 2
last = 150

# ########## variables ##########


# レバテックフリーランスにアクセスしてコンテンツの取得
html = requests.get(siteUrl)
soup = BeautifulSoup(html.text, 'lxml')

# ページトップの言語別の求人数の情報を取得
langJobs = soup.find(divTag, {classAttribute: languageJobsBox})
jobs = langJobs.find_all(listTag, {classAttribute: languageJobsList})

# テキストファイルへ言語別の求人情報を書き込み
# TODO: CSVで1ファイル管理
dt = datetime.datetime.now()
formatted = dt.strftime('%Y%m')
fileName = formatted + "jobs.txt"

with open(fileName, 'w') as f:
    for job in jobs:
        print(str(job.find(anchorTag).contents), end=",", file=f)
        print(str(job.find(spanTag).contents), file=f)

# PHPの求人ページで単価を取得 (1ページ目)
phpPage = requests.get(phpJobsUrl)
soup = BeautifulSoup(phpPage.text, 'lxml')

jobTitles = soup.find_all(anchorTag, {classAttribute: jobTitleAnchorClass})
jobRewards = soup.find_all(listTag, {classAttribute: jobRewardListClass})
jobSkills = soup.select(jobSkillParagraphSelector)

fileName = formatted + "php.txt"


f = open(fileName, 'w')
for i in range(loops):
    f.write(str(jobTitles[i].text) + ',')
    reward = int(jobRewards[i].find(
        spanTag).text.replace(',', '').replace('円', ''))
    if reward < hourlyWageFlag:
        reward = reward * monthlyHours
    f.write(str(reward) + ',')
    f.write(str(jobSkills[i].contents) + '\n')

# PHPの求人ページで単価を取得 (2ページ目以降)
try:
    for i in range(second, last):
        phpPage = requests.get(
            phpJobsUrl + 'p' + str(i) + '/')
        soup = BeautifulSoup(phpPage.text, 'lxml')
        jobTitles = soup.find_all(
            anchorTag, {classAttribute: jobTitleAnchorClass})
        jobRewards = soup.find_all(
            listTag, {classAttribute: jobRewardListClass})
        jobSkills = soup.select(jobSkillParagraphSelector)

        for j in range(loops):
            f.write(str(jobTitles[j].text) + ',')
            reward = int(jobRewards[j].find(
                spanTag).text.replace(',', '').replace('円', ''))
            if reward < hourlyWageFlag:
                reward = reward * monthlyHours
            f.write(str(reward) + ',')
            f.write(str(jobSkills[j].contents) + '\n')

        print(i)

except Exception as e:
    print(str(i) + 'ページで処理が終了')
    print(e)

f.close()
