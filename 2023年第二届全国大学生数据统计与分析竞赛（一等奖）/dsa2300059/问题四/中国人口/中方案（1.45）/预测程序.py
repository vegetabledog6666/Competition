import pandas as pd
import numpy as np
import copy
import sys
# import multiprocessing as Pool

total_pop_cur=1411750000
CURRENT_YEAR=2022 ##现在的年份
chi_mean=float(1.45)     ##设置中国总和生育率
sd=10000     ##代表将其变成万
sex_bir_ratio=0.5     ##代表男女比例

age_sex = pd.read_csv("./age_sex.csv", header=None, 
    names=["age","total","male","female","total_prop","male_prop","female_prop","sex_ratio"])   ##读入相关的性别数据
#不知道的人口信息用第六次人口普查的代替
male_prop = age_sex['male']/sum(age_sex['total'])
female_prop = age_sex['female']/sum(age_sex['total'])      ##计算对应不同年龄段人口占总人口的比例

sex_n = pd.DataFrame({"male" : male_prop*total_pop_cur/sd,
                    "female" : female_prop*total_pop_cur/sd})
sex_n = sex_n.astype({"male":"int", "female":"int"})   ##对应的男女人口


#全国分年龄、性别的死亡人口状况							
age_death = pd.read_csv("./age_death_per_year.csv", header=None, 
    names=["age","total","male","female", "total_death", "male_death" ,"female_death",
           "total_dt","male_dt","female_dt"])
death_rate = age_death[{"male_dt","female_dt"}]/1000

#全国育龄妇女分年龄、孩次的生育状况
age_birth = pd.read_csv("./birth.csv", header = None,
    names=["age","total_women","total_birth","birth_rate","firstBirth_number","firstBirth_rate",
           "secondBirth_number","secondBirth_rate","thirdBirth_number","thirdBirth_rate"])

birth_rate_adj = pd.DataFrame({'age' : age_birth['age'], 
                   "firstBirth_rate" : age_birth["firstBirth_rate"]/sum(age_birth["firstBirth_rate"])})

class Person(object):   ##创建模拟类
    def __init__(self, sex,bir_yea,childNO):
        self.sex=sex 	#1是男性，2是女性
        self.bir_yea=bir_yea
        self.childNO=childNO     ##代表有无小孩
    def age(self,Year): ##代表返回其年龄
        return Year-self.bir_yea
    def status(self, Year):
        if self.sex==1: sexname = "male_dt"
        if self.sex==2: sexname = "female_dt"
        if self.age(Year)>100:
            dr=death_rate.iloc[100][sexname]
        else:
            dr=death_rate.iloc[self.age(Year)][sexname]
        return np.random.binomial(1,dr) #1代表死了，0代表活着
    def birth(self,Year,chi_mean):
        if self.age(Year)<15 or self.age(Year)>49 or self.sex==1 or self.status(Year)==1:  ##代表着不能生育的人
            return None
        else:
            br = birth_rate_adj.loc[birth_rate_adj['age']==self.age(Year)]['firstBirth_rate']
            bn = np.random.binomial(1,br*chi_mean)   ##设定其为二项分布，代表生育与否
            if bn==1:
                self.childNO+=bn
                cc=Person(np.random.binomial(1,sex_bir_ratio)+1,Year,0)
                return cc
            return None


# initiate a pool of starting population
def initPop():
    p_pool = []  ##人口池
    for iage, irow in sex_n.iterrows():  ##包含该行的信息以及对应的索引
        for ii in range(irow['female']):   ##计算一下人口的出生年份
            p_pool.append(Person(2,CURRENT_YEAR-iage,0))
        for jj in range(irow['male']):
            p_pool.append(Person(1,CURRENT_YEAR-iage,0))
    return p_pool


if __name__ == '__main__':
    p_pool = initPop()
    pop_log = {}
    year=2023
    while True:
        print(year)
        for p in p_pool:
            pbirth = p.birth(year, chi_mean)
            if pbirth is not None:    ##代表生育
                p_pool.append(pbirth)
            if p.status(year)==1:
                p_pool.remove(p)
        pop_log[year]=copy.deepcopy(p_pool) # deep copy. 
        if year==2100:
              break
        year=year+1
    out = open("中国人口预测.txt","w")
    out.write("Year\tMale_pop\tFemale_pop\n")
    for k,plist in pop_log.items():
        male_no = len([p for p in plist if p.sex == 1])
        female_no = len([p for p in plist if p.sex == 2])
        out.write(str(k) + "\t" + str(male_no) + "\t" + str(female_no) + "\n")
    out.close()