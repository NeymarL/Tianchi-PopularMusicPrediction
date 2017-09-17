# Tianchi Popular Music Prediction Competition
> Team `42`

---
## 逐天预测（代码在`old`文件夹里）
### data 目录结构(没push到远程仓库)

* `datas`
    * `feats`       存放生成好的特征，文件名格式：feats20150901.csv
    * `final`       存放每天的训练结果，文件名格式：20150901.csv
    * `labels`      存放每天的训练标签，文件名格式：label20150831.csv
    * `preduced`    存放经过处理的每天的训练结果，用于加入下一天的训练数据
        * `data.csv`      训练出的下一天的训练数据，不包括20150830以前的
    * `raw_train_result`  存放每天训练好的标签，用于生成可提交版本
    * `train_data.csv`    经过与处理的用户交互数据
    * `mars_tianchi_user_actions.csv`
    * `mars_tianchi_songs.csv`


### 训练流程

**pre_process.py**

* 对原始用户交互数据做预处理，生成 `train_data.csv` ,只需做一次
* param : 无

**make_train_feats.py**

* 生成 train_day 的特征，存放到 `datas/feats` 目录下
* params :
      * train_day       训练日的日期（train_day打标签）
      * b1_day          训练日前一天的日期
      * b7_day          训练日前7天的日期
      * b30_day         训练日前30天日期
      * b90_day         训练日前90天日期
* eg. `python make_train_feats.py 20150830 20150829 20150823 20150801 20150601`
* note : 提取 train_day 的特征并不需要这一天的数据，只需要它的历史数据就够了

**make_label.py**

* 为 label_day 打标签(需要已知这一天的数据), 结果放到 `datas/labels` 目录下
* params :
      * label_day       需要打标签的日期
      * b30_day         label_day 的30天前的日期
* eg. `python make_label.py 20150830`


**train.py**

* 训练模型，预测. 生成临时预测结果放到 `datas/raw_train_result` 目录下，生成新的训练数据放到 `datas/preduced` 目录下
* params :
      * train_day
      * predict_day     train_day的后一天的日期
* 用 train_day 的特征拟合这天的label, 然后带入 predict_day 的特征，预测下一天的label
* eg. `python train.py 20150831 20150901`


**result_add_train_set.py**

* 把新生成的训练数据合并到 `datas/preduced/data.csv`
* param :
      * 需要合并的日期, 要保证在 `datas/preduced` 中存在对应文件
* eg. `python result_add_train_set.py 20150831`


**submit.py**

* 处理中间预测结果，生成可以提交的格式，存放在 `datas/finals` 目录下
* param :
      * 需要处理的日期，要保证在 `datas/raw_train_result` 中存在对应文件
* eg. `python submit.py 20150831`


**42.sh**

* 串联整个流程，连续训练出60天的结果

## 直接预测60天

尝试的各种模型都在主文件夹下，第二赛季的SQL代码在`p2`目录下。

---
题目位置
[https://tianchi.shuju.aliyun.com/competition/information.htm?spm=5176.100067.5678.2.85Ngjc&raceId=231531](https://tianchi.shuju.aliyun.com/competition/information.htm?spm=5176.100067.5678.2.85Ngjc&raceId=231531)

# Introduction

This competition (Big Data Challenge) launched on ‘Tianchi Big Data Platform’ is endorsed by the ministry of education and co-sponsored by Tsinghua University and Alicloud. It is opened for the global data enthusiasts, aiming at enhancing people’s data analysis/processing ability and algorithm research ability, to explore the core science and technology issues of big data, to propel the big data research and applications.

During this contest, participants are expected to find the future popular artist and accurately predict the number of plays at each stage based on historical subscription data. Finally, they should be able to find the music popularity trend during a period of time.This contest will openthe “song-artist” sampling data and provide historical records of subscribers’ actions.The participantsshould design corresponding algorithm to do data analysis and processing. We will use online evaluation procedures to match results in accordance with the evaluation index and give the rankings.

## Rules

This contest will be divided into three stages: preliminaries, semi-finals and finals. In preliminaries, participants will download the data and compete locally. In semi-finals, candidates are required to access the data sets, debug their programs with ODPS MapReduce, SQL, and machine learning algorithm packages integrated into the platform. In finals, candidates are required to do presentation and reply on site. The specific schedules are shown as follows:
Preliminaries (May 17 –Jun. 14)

1. Participants download data, conduct the debugged program locally and submit the results. You can submit as many results as you want, but only the latest submission count.
2. From May 17th, we will conduct the evaluation once per day. The deadline for submission is 10:00 A.M. The leaderboard will be updated every day in which the F1 scores will be sorted from the highest to the lowest. The leaderboard shows the best scores at this stage.
3. On June 7th, there will be a new data set and the leaderboard will be updated on June 8th.
4.On the deadline of preliminaries (10:00AM, on June 14th), the Top 500 teams who have verified accounts will enter the semi-finals. (Verification entry: Tianchi Home- My Page –Verify your account –Verified Alipay account). Please verify your account before 10:00 A.M. (GMT+8) June 7th, 2016.

## Grant Privileges (Jun. 14- Jun. 16)
1. In semi-finals, candidates are required to log in the Tianchi Platform to complete the competition on the Yushanfang platform.
2. From 10:00 A.M. on June 14th, we start to grant data privileges to you. At 12:00 P.M. on June 16th, we will terminate to grant privileges.
3. After granted with corresponding privileges, you can enter into the platform by clicking the menu “Yushanfang” in the left part of [Competition Details] page. (Note: you should use the same Taobao account/Alicloud account to log in Yushanfang and sign up the competition.)
Semi-finals (Jun.17—Jul.15)
1.  You are not allowed to download the data. Participants are required to login the Tianchi Platform to access the data sets, debug their programs with ODPS MapReduce, SQL, Graph and machine learning algorithm packages integrated into the platform.
2. Starting on June 17th, the leaders will be tracked on a leaderboard that is updated at 10:00 A.M. (GMT+8) daily.
3. The data set will be updated at 12:00 AM (GMT+8), July 8th. Please note the new table name when access to the data. The leaderboard will be updated at July 9th.
4. The leaderboard will be updated at 10:00 AM (GMT+8), July 15th for the last time. The Top 5 teams will be invited to the finals.

## Finals (Late August)
1. Candidates are required to prepare for the review materials (PPT and source code) in advance.
2. The top 3 teams will be granted corresponding rewards and certificate based on the algorithm, historical performances, and the scores given by judges.
Eligibility
All the data enthusiasts
The candidate can participate in the competition individually or join in a team. (Each team may have up to 3 people.)
Note: Alibaba and Xiami employees are not allowed to participate.

## Team rules:
1.    Each person can only participate in one team.
2.    Participants must ensure that their registration information is valid, or they will be disqualified for the competitions and awards.
3.    The persons of Alibaba and Xiami are not allowed to participate.
4.    The submitted result should be completed alone and cannot be borrowed indiscriminately from other people. Otherwise your competition qualification will be cancelled.
5.    The provided data set and platform are only available for this contest and shall not be used for any other purposes. Once you break this rule and cause losses for data providers and platform providers, you will bear all the responsibilities.
Registration Method

1.    You can participate in the competition simply by login the official website with your Taobao or Aliyun account and complete your personal information.
2.    The deadline of registration, team modification and real name verification: 10:00 A.M., June 7, 2016.
3.    Official AliWangWang Group: 1270938233.

## Awards
1.        Awards ofPreliminaries
The first prize: Champion, ￥30,000 and certificate
The second prize: the second place and the third place, ￥10,000 and certificate
The third prize: the forth place - the tenth place, ￥5,000 and certificate
Note: The awards mentioned above are based on your PPT, algorithm, and historical performances.
2.        Awards of Finals
Champion: 1 team, ￥200,000 and certificate
First runner-up: 1 team, ￥50,000 and certificate
Second runner-up: 1team, ￥20,000 and certificate.
(The above awards are based on the ranking in the finals. Top 10 players can directly enter the final interview of Alibaba recruitments.
3.   Stars of the Week
The Top 3 teams on the leaderboard every Monday will become the Stars of the Week and each team member will receive a Tianchi souvenir.
4.   Geek Awards
Top 20 players in the semi-finalswill receive Geek Certificates and go into the green channel of Alibaba' s campus recruitment (i.e. players are qualified to skip resume screen and written interview exam in the recruitment process). The green channel will be valid before the graduation date of players.
5.    Other Awards
-      AliCloud Talent Certification: Top 20 players in Season 2 will acquire AliCloud ACP certification (Big Data Cate). Top 50 players can get certain scores to offset AliCloud ACA certification score. Top 100 players can get certain scores to offset AliCloud ACP certification score.
-      Tianchi Points and Coupons
Your team will get corresponding points according to the final rankings in the competition (including preliminaries and semi-finals). For details, please refer to link
Your team will get corresponding coupons according to the final rankings in the competition (including preliminaries and semi-finals).

## Rules:
Rank 1 to 10: 11000 Coupons
Rank 10 to 50: 2500 Coupons
Rank 50 to 100: 1200 Coupons
Assignment method: The couponswill be assigned to every team member averagely.
Assignment time: within two weeks after the Season 2 is end.
The coupons are used for buying the Tianchi Souvenirs. 查看纪念品(View Tianchi Souvenirs)
Sponsor
College Computer Professional Teaching Steering Committee (Ministry of Education)
College Software Engineering Teaching Steering Committee (Ministry of Education)
University Computer Course Teaching Steering Committee (Ministry of Education)
National Institute of Computer Education
Organizer
       Tsinghua University
Supporter
       Alibaba Group (Xiami Music, Alicloud)

## 中国高校计算机大赛——大数据挑战赛
2016中国高校计算机大赛——大数据挑战赛（Big Data Challenge）是由教育部高等学校计算机类专业教学指导委员会、软件工程专业教学指导委员会、计算机课程教学指导委会和全国高等学校计算机教育研究会联合主办，清华大学和阿里云联合承办，在“天池大数据众智平台”上开展的高端算法竞赛。大赛面向全球开放，旨在通过竞技的方式提升人们对数据分析与处理的算法研究与技术应用能力，探索大数据的核心科学与技术问题，尝试创新大数据技术，推动大数据的产学研用。
本次大赛以阿里音乐用户的历史播放数据为基础，期望参赛队伍通过对阿里音乐平台上每个时间段内艺人的试听量进行预测，挖掘出即将成为潮流的艺人，从而实现对一个时间段内音乐流行趋势的准确把控。大赛将开放一定规模的抽样歌曲艺人数据以及与这些艺人相关的用户行为，参赛队伍需要设计相应的算法进行数据分析和处理，比赛结果按照规定的评价指标使用在线评测程序进行评阅和排名，结果最优者获胜。

## 赛制说明
本次大赛分为第一赛季、第二赛季和决赛三个阶段，其中：第一赛季由参赛队伍下载数据在本地进行算法设计和调试；第二赛季要求参赛者在线进行数据分析和处理；决赛要求参赛者进行现场演示和答辩。具体安排和要求如下：

### 第一赛季（5月17日—6月14日）
1.  参赛队伍可下载数据，并在本地调试算法，提交结果。若参赛队伍在一天内多次提交结果，新结果版本将覆盖旧版本。
2.  从5月17日起，系统每天进行一次评测和排名，评测开始时间为当天10:00 AM，按照评测指标从高到低进行排序，每天更新排行榜；排行榜将选择参赛队伍在本阶段的历史最优成绩进行排名展示。
3.  系统在6月7日将进行数据切换，参赛队伍在访问赛题数据时须注意更换表名，第一赛季成绩排行榜将选取6月8日起产生的成绩进行重新排名。
4.  第一赛季截止时间是6月14日10:00AM，成绩排名前500名且通过支付宝实名认证的参赛队伍将进入第二赛季。（认证入口：天池网站-个人中心-认证-支付宝实名认证，要求第一赛季截至前完成认证，要求6月7日10:00AM 前完成认证）

### 平台赋权（6月14日—6月16日）
1.  第二赛季需通过天池官网进入御膳房平台进行参赛。
2.  6月14日10:00 AM开始赋权，6月16日12:00PM完成赋权。
3.  第二赛季队伍获得御膳房平台权限后，比赛详情页面左侧将显示“御膳房”菜单，点击进入平台（注：登录御膳房平台需使用和报名比赛同一个淘宝/阿里云账号）；

### 第二赛季（6月17日—7月15日）
1.  第二赛季的数据不可下载，选手需要使用平台完成数据处理、建模、算法调试、产出结果等所有环节，可使用基于ODPS的Map Reduce、SQL、GRAPH及平台集成的各种机器学习算法包/模型。
2.  从6月17日起，系统每天进行一次评测和排名，评测开始时间为当天10:00 AM，按照评测指标从高到低进行排序，每天更新排行榜。
3.  系统在7月8日12:00PM将进行一次数据切换，参赛队伍在访问赛题数据时须注意更换表名，第二赛季成绩排行榜将选取7月9日起产生的成绩进行重新排名。
4.  第二赛季截止时间是7月15日10:00AM，成绩排名前5名的选手将受邀参加决赛的现场答辩。

### 决赛（8月下旬）
1. 决赛将以现场答辩会的形式进行，具体安排另行通知。
2. 参赛队伍应提前准备现场答辩材料，包括PPT、算法代码。
3. 组委会将根据参赛队伍的算法原理、历史成绩和评委打分，评选出整个大数据挑战赛的冠亚季军，并现场颁发奖金及证书。

### 参赛对象
本次大赛面向全社会开放，高等院校、科研单位、互联网企业、创客团队等人员均可报名参赛。参赛队伍可以单人参赛或自由组队（最多不超过3人，可以跨单位组队）。
参赛队伍要求：
1. 每人只能参加一支队伍。
2. 保证参赛队员报名信息准确有效，否则将被取消参赛资格及奖励。
3. 大赛主办和技术支持单位如有机会接触赛题相关数据的人员不允许参赛。
4. 提交的参赛作品必须是团队或个人独立完成的原创作品，不得抄袭，不得违反任何相关的法律法规，否则将取消参赛资格。
5. 大赛所提供的数据集和平台仅限于此次大赛使用，不得用于其他任何目的。若因违反此规定而给数据提供方或平台提供方造成损失的，参赛队伍所在单位和选手须承担全部责任。

### 报名方式
1. 报名方式：用淘宝或阿里云账号登录大赛官网，完成个人信息注册，即可报名参赛。
2. 报名、组队变更和实名认证截止时间均为2016年6月7日10:00 AM。
3. 大赛官方交流群——旺旺群：1270938233。

### 奖项设置
1.    第一赛季奖项
一等奖：第1名队伍，奖金叁万元，颁发获奖证书
二等奖：第2-3名队伍，奖金壹万元，颁发获奖证书
三等奖：第4-10名队伍，奖金伍仟元，颁发获奖证书
说明：上述奖项将结合参赛队伍的总结PPT、算法原理、历史成绩进行评审，确定最终排名及奖项；如有必要将组织现场答辩。（解释权归组委会）
2. 决赛奖项
冠军：1支队伍，奖金贰拾万元，颁发获奖证书
亚军：1支队伍，奖金伍万元，颁发获奖证书
季军：1支队伍，奖金贰万元，颁发获奖证书
说明：上述奖项以决赛现场答辩的最终名次决定，第二赛季排名TOP10的主要参赛选手可直接入围阿里校招终面（在校期间均有效）。
3. 周星星
自大赛排行榜开榜起，每周一榜单排名前三名的参赛队伍将成为周星星，其队员可获得天池礼品一份。
4. 极客奖
第二赛季排名TOP20的选手将获得极客奖证书，并入围阿里巴巴校园招聘绿色通道。(即招聘流程省略简历筛选及笔试筛选阶段，直接进入面试阶段 ，在校期间均有效）
5. 其他激励
-      阿里云人才认证：第二赛季最终排行前20名选手可获得阿里云ACP人才认证；前50名可抵扣ACA考试分数；前100名可抵扣ACP考试分数。
-      天池积分及粮票发放：
       积分发放：在赛季中产出过成绩的队伍，根据该赛季最终排名获得相应排名的积分奖励；包括第一赛季及第二赛季。具体发放规则：参照链接
       粮票发放：在赛季中产出过成绩的队伍，根据该赛季最终排名获得相应排名的粮票奖励；包括第一赛季及第二赛季。
       激励标准：
      第1-10名队伍：11000粮票
      第10-50名队伍：2500 粮票
      第50-100名队伍：1200粮票
分配方式：若队伍由多人组成，粮票最终将平均分配。
发放时间：第二赛季截止后的两周内完成发放。
粮票可兑换天池纪念品，查看纪念品

### 主办单位
教育部高等学校计算机类专业教学指导委员会
教育部高等学校软件工程专业教学指导委员会
教育部高等学校大学计算机课程教学指导委会
全国高等学校计算机教育研究会
承办单位
       清华大学
赞助单位
       阿里巴巴集团（阿里音乐、阿里云）

