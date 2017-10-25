
# coding: utf-8

# In[10]:

import os
import sys
import subprocess
import datetime
import time
import shutil
import pandas as pd
import sklearn_pandas
import sklearn2pmml
import re
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.externals import joblib
from sklearn import pipeline
from sklearn import feature_selection
pd.set_option('display.max_columns',None)


# In[11]:

def getPreNDay(n):
    return (datetime.datetime.today() + datetime.timedelta(days=-n)).strftime('%Y%m%d')


# In[12]:

def to_vector(data):
    if len(data)==0:
        return data
    data = data[data.system==0]
    data = pd.concat([data.loc[:,['op_type']],data.loc[:,'is_vip':'target']],axis=1) 
    data.loc[:,'op_type':'pre1min_phone_info_count'] = data.loc[:,'op_type':'pre1min_phone_info_count'].fillna(0)
    #pattern = re.compile('[0-9]+')
    #data.zhaopinrenshu=pd.Series(data.zhaopinrenshu.apply(lambda x:x if pattern.match(x) else '若干'))
    data.zhaopinrenshu = data.zhaopinrenshu.replace('若干','0')
    data.zhaopinrenshu = data.zhaopinrenshu.replace('(报名咨询Q:3381257137)','0')
    data.zhaopinrenshu = data.zhaopinrenshu.replace('报名Q:3381257137','0')
    data.gongzuonianxian = data.gongzuonianxian.replace('不限','-1')
    return data


# In[13]:

def read_vector(path):
    train_data = pd.DataFrame()
    for i in range(2,61):
        if os.path.isfile(path + '/' + getPreNDay(i)):
            data_i = pd.read_csv(path + '/' + getPreNDay(i),na_values='null')
            train_data = pd.concat([train_data,data_i],axis=0)
    train_vector = to_vector(train_data)
    test_data=pd.DataFrame()
    if os.path.isfile(path + '/' + getPreNDay(1)):
        test_data = pd.read_csv(path + '/' + getPreNDay(1),na_values='null')
    test_vector = to_vector(test_data)
    return train_vector,test_vector


# In[14]:

def read_model(path,version_old):
    cls_old = None
    if os.path.isfile(path + '/' + version_old + '.pkl'):       
        cls_old = joblib.load(path + '/' + version_old + '.pkl')
    return cls_old


# In[23]:

def train_model(train_vector):
    mapper = sklearn_pandas.DataFrameMapper([
            ('op_type',preprocessing.LabelEncoder()),
            (['is_vip','reg_life','pre7day_uid_ipcount','pre7day_uid_jobcount','pre7day_uid_citycount','pre7day_uid_infocount','pre7day_uid_sys_delete_count','pre7day_uid_man_delete_count','pre7day_uid_sys_backmodify_count','pre7day_uid_man_backmodify_count','license_enterpriseid_count','pre7day_ip_uidcount','pre7day_ip_jobcount','pre7day_ip_citycount','pre7day_ip_infocount','pre7day_ip_sys_delete_count','pre7day_ip_man_delete_count','pre7day_ip_sys_backmodify_count','pre7day_ip_man_backmodify_count','pre7day_userip_reguid_count','pre7day_userip_login_count','pre7day_phone_uidcount','pre7day_phone_jobcount','pre7day_phone_citycount','pre7day_phone_infocount','pre24hour_ip_uid_count','pre24hour_ip_job_count','pre24hour_ip_city_count','pre24hour_ip_info_count','pre24hour_uid_ip_count','pre24hour_uid_job_count','pre24hour_uid_city_count','pre24hour_uid_info_count','pre24hour_phone_uid_count','pre24hour_phone_job_count','pre24hour_phone_city_count','pre24hour_phone_info_count','pre24hour_ip_audit_pass_info_count','pre24hour_ip_audit_nopass_info_count','pre24hour_ip_audit_shuazuan_info_count','pre24hour_uid_audit_pass_info_count','pre24hour_uid_audit_nopass_info_count','pre24hour_uid_audit_shuazuan_info_count','pre24hour_phone_audit_pass_info_count','pre24hour_phone_audit_nopass_info_count','pre24hour_phone_audit_shuazuan_info_count','pre24hour_ip_sys_delete_count','pre24hour_ip_sys_backmodify_count','pre24hour_uid_sys_delete_count','pre24hour_uid_sys_backmodify_count','pre1hour_ip_uid_count','pre1hour_ip_job_count','pre1hour_ip_city_count','pre1hour_ip_info_count','pre1hour_uid_ip_count','pre1hour_uid_job_count','pre1hour_uid_city_count','pre1hour_uid_info_count','pre1hour_phone_uid_count','pre1hour_phone_job_count','pre1hour_phone_city_count','pre1hour_phone_info_count','pre1hour_title_uid_count','pre1hour_title_job_count','pre1hour_title_city_count','pre1hour_title_info_count','pre1hour_title_ip_count','pre5min_ip_uid_count','pre5min_ip_job_count','pre5min_ip_city_count','pre5min_ip_info_count','pre5min_uid_ip_count','pre5min_uid_job_count','pre5min_uid_city_count','pre5min_uid_info_count','pre5min_phone_uid_count','pre5min_phone_job_count','pre5min_phone_city_count','pre5min_phone_info_count','pre1min_ip_uid_count','pre1min_ip_job_count','pre1min_ip_city_count','pre1min_ip_info_count','pre1min_uid_ip_count','pre1min_uid_job_count','pre1min_uid_city_count','pre1min_uid_info_count','pre1min_phone_uid_count','pre1min_phone_job_count','pre1min_phone_city_count','pre1min_phone_info_count'],None),
            (['license'],[preprocessing.Imputer(strategy='most_frequent'),preprocessing.LabelEncoder()]),
            (['xingzhi'],[preprocessing.Imputer(strategy='most_frequent'),preprocessing.LabelEncoder()]),
            (['xinzi'],[preprocessing.Imputer(strategy='most_frequent'),preprocessing.LabelEncoder()]),    
            (['xueli'],[preprocessing.Imputer(strategy='most_frequent'),preprocessing.LabelEncoder()]),
            (['thirdcertificate'],[preprocessing.Imputer(strategy='most_frequent'),preprocessing.LabelEncoder()]),
            (['zhaopinrenshu'],preprocessing.Imputer(strategy='most_frequent')),
            (['gongzuonianxian'],[preprocessing.Imputer(strategy='most_frequent'),preprocessing.LabelEncoder()]),
            (['fulidaiyu_wuxian','fulidaiyu_canbu','fulidaiyu_huabu','fulidaiyu_fangbu','fulidaiyu_jiaotongbu','fulidaiyu_zhoumoshuangxiu','fulidaiyu_jiabanbu','fulidaiyu_baozhu','fulidaiyu_niandishuangxin','fulidaiyu_baochi','fulidaiyu_oversum','user_define_fulidaiyu_oversum','title_punctuationcount','title_rarecharcount','title_iscontainabnormalnumber','content_punctuationcount','content_suspectmaxlength','content_conpuncmaxsize','content_suspectzerocount','content_transitsum','content_transitrate','content_punctuationrate','content_rarecharcount','fuli_suspectmaxlength','fuli_suspectzerocount','fuli_rarecharcount','fuli_iscontainkeyword','fuli_iscontainabnormalnumber','enterprisereg_name_rarecharcount','enterprisereg_address_rarecharcount','enterprisereg_address_iscontain_local'],None),
            ('target',None)
    ])
    train = mapper.fit_transform(train_vector)
    pipeline_estimator = pipeline.Pipeline([
        ('estimator',RandomForestClassifier(n_estimators=300, max_depth=10, min_samples_split=2, n_jobs=3 ,random_state=0))
    ])
    #pipeline_params = dict(
        #selector__k=[90, 100, 110],
        #estimator__n_estimators=[200, 250, 300])
    #grid_search = model_selection.GridSearchCV(pipeline_estimator, param_grid=pipeline_params, n_jobs=3)
    #grid_search.fit(train[:,:-1],train[:,-1])
    #best_estimator = grid_search.best_estimator_
    pipeline_estimator.fit(train[:,:-1],train[:,-1])
    return pipeline_estimator,mapper


# In[16]:

def save_model_performance(estimator_old,estimator_new,mapper,test_vector,path,version_old,is_online):
    test = mapper.transform(test_vector)
    test_X = test[:,:-1]
    test_y = test[:,-1]
    test_pred_new = estimator_new.predict(test_X)
    test_prob_new = estimator_new.predict_proba(test_X)
    precision_new = metrics.precision_score(test_y,test_pred_new)
    recall_new = metrics.recall_score(test_y,test_pred_new)
    auc_new = metrics.roc_auc_score(test_y,test_prob_new[:,1])
    version_new = 'RandomForest_' + repr(int(time.time()))
    performance = pd.DataFrame([['_','-1','-1','-1'],[version_new,round(precision_new,4),round(recall_new,4),round(auc_new,4)]],columns=['version','precision','recall','auc'])
    if is_online=='1':
        test_pred_old = estimator_old.predict(test_X)
        test_prob_old = estimator_old.predict_proba(test_X)
        precision_old = metrics.precision_score(test_y,test_pred_old)
        recall_old = metrics.recall_score(test_y,test_pred_old)
        auc_old = metrics.roc_auc_score(test_y,test_prob_old[:,1])
        performance = pd.DataFrame([[version_old,round(precision_old,4),round(recall_old,4),round(auc_old,4)],[version_new,round(precision_new,4),round(recall_new,4),round(auc_new,4)]],columns=['version','precision','recall','auc'])
    # 删除上次生成的模型文件
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    # 保存pkl模型
    joblib.dump(estimator_new,path + '/' + version_new + '.pkl',compress=6)
    # 保存pmml模型
    sklearn2pmml.sklearn2pmml(estimator_new,mapper,path + '/'+ version_new + '.pmml',with_repr=False,debug=False)
    # 保存性能对比
    performance.to_csv(path + '/' + version_new + '.performance',index=None)  


# In[17]:

def main():
    # 设置执行sklearn2pmml的jdk版本
    os.environ['PATH']='/opt/soft/jdk/jdk1.7.0_80/bin:/opt/soft/jdk/jdk1.7.0_80/jre/bin'
    # load数据
    train_vector,test_vector = read_vector(sys.argv[1])
    # 判断模型是否初次部署
    estimator_old = None
    if sys.argv[5]=='1':    
        # load线上模型
        estimator_old = read_model(sys.argv[2],sys.argv[3])
    # 训练新模型
    estimator_new,mapper = train_model(train_vector)
    # 评估和持久化模型
    save_model_performance(estimator_old,estimator_new,mapper,test_vector,sys.argv[4],sys.argv[3],sys.argv[5])


# In[ ]:

train_vector,test_vector = read_vector("D:\changguizhuzuan")

estimator_new,mapper = train_model(train_vector)






