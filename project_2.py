#importing small data
from copy import deepcopy
file1 = open(r"L:\UCR\1_CS205-AI\project2\CS205_small_testdata__15.txt","r")
sm_15= file1.readlines()#small dataset
n_cols_15 =len(sm_15[0].split())
matrix_15=[]

for i in range(n_cols_15):
    columns =[]
    for j in sm_15:columns.append(j.split()[i])
    matrix_15.append(columns)

##importing large data

file2 = open(r"L:\UCR\1_CS205-AI\project2\CS205_large_testdata__7.txt","r")
lg_7= file2.readlines()
n_cols_7 =len(lg_7[0].split())
matrix_7=[]
for i in range(n_cols_7):
    columns =[]
    for j in lg_7:columns.append(j.split()[i])
    matrix_7.append(columns)

#feature_set stores all global
dataset = int(input("input 1 for small dataset and 2 for large dataset: "))
algorithm = int(input("input 1 for forward selection, 2 for backward elimination: "))
if algorithm==1:feature_set=set()#forward selection
else:
    if dataset==1:feature_set=set([i for i in range(1,11)])
    else:feature_set=set([i for i in range(1,251)])
    
def dist(p1,p2,features,dataset):#p1->test, p2->training
    distance = 0
    for i in range(len(features)):
        if dataset==1:#small dataset
            distance+=(float(matrix_15[features[i]][p1])-float(matrix_15[features[i]][p2]))**2
        else:
            distance+=(float(matrix_7[features[i]][p1])-float(matrix_7[features[i]][p2]))**2
    return distance
    
def classifier(features,new,dataset,point):#classifes the class of the datapoint in a given feature
    min_dist = 10**10
    nearest_point = 0
    if dataset==1:#small dataset
        for i in range(300):#i->training datapoint, point->test
            distance = dist(point,i,features,dataset)
            if i!=point and distance<min_dist:
                min_dist=distance
                nearest_point = i
        classifier = matrix_15[0][nearest_point]
    else:#large dataset
        for i in range(900):#i->training datapoint, point->test
            distance = dist(point,i,features,dataset)
            if i!=point and distance<min_dist:
                min_dist=distance
                nearest_point = i
        classifier = matrix_7[0][nearest_point]
    return classifier

def accuracy(features,new,dataset,algorithm):#accuracy of adding the given feature
    corrects = 0
    if algorithm==1:
        temp=list(features)
        temp.append(new)
    else:
        temp=deepcopy(features)
        temp.remove(new)
        temp=list(temp)
    if dataset==1:#small dataset
        for i in range(300):#all the test and train data
            if classifier(temp,new,dataset,i)==matrix_15[0][i]:corrects+=1#correctly classified
        accuracy = corrects/300
    else:#large dataset
        for i in range(900):#all the test and train data
            if classifier(temp,new,dataset,i)==matrix_7[0][i]:corrects+=1#correctly classified
        accuracy = corrects/900
##    print("the current feature set is:",temp,"and its accuracy is:",accuracy)
    return accuracy

def best(features,dataset):#inserts a new feature with highest accuracy
    best_accuracy = 0
    best_feature = 0
    if dataset==1:
        for i in range(1,11):#i-> feature being considered, features->global best set
            if i in features:continue#if the feature was already inserted before
            acc = accuracy(features,i,dataset,algorithm)
            if acc>best_accuracy:
                best_accuracy = acc
                best_feature = i
    else:
        for i in range(1,251):#i-> feature being considered, features->global best set
            if i in features:continue#if the feature was already inserted before
            acc = accuracy(features,i,dataset,algorithm)
            if acc>best_accuracy:
                best_accuracy = acc
                best_feature = i
        
    return [best_feature,best_accuracy]

def worst(features,dataset):#picks the worst dataset to remove
    best_accuracy = 0
    worst_feature = 0
    if dataset==1:
        for i in range(1,11):
            if i not in features:continue
            acc = accuracy(features, i, dataset,algorithm)
            if acc>best_accuracy:
                best_accuracy=acc
                worst_feature=i
    else:
        for i in range(1,251):
            if i not in features:continue
            acc = accuracy(features, i, dataset,algorithm)
            if acc>best_accuracy:
                best_accuracy=acc
                worst_feature=i
         
    #print(worst_feature,best_accuracy)
    return [worst_feature,best_accuracy]

#calculating default rate of both datasets
class_1_15=0#small
class_1_7=0#large
if dataset ==1:
    for i in range(300):
        if int(float(matrix_15[0][i]))==1:class_1_15+=1
    start_acc_15=max(class_1_15,300-class_1_15)/300
else:
    for i in range(900):
        if int(float(matrix_7[0][i]))==1:class_1_7+=1
    start_acc_7=max(class_1_7,900-class_1_7)/900

global_best_accuracy = 0
global_best_features = []
if dataset==1:
    for i in range(1,11):#all possible rounds
        if algorithm==1:
            if i==1:
                print("the starting set of features is : ",list(feature_set))
                print("the default rate is: ",start_acc_15)
            temp=best(feature_set,dataset)
            feature_set.add(temp[0])
        else:
            if i==1:
                temp1=set([i for i in range(1,10)])
                start = accuracy(temp1,10,dataset,1)
                print("starting set of features is :",list(feature_set))
                print("the starting accuracy =",start)
            temp=worst(feature_set,dataset)
            feature_set.remove(temp[0])
        if global_best_accuracy<temp[1]:
            global_best_accuracy=temp[1]
            global_best_features = list(feature_set)
        print("")
        print("current set of feature after round",i,"is:",list(feature_set))
        print("the best current accuracy =",temp[1])
else:
    for i in range(1,251):#all possible rounds
        if algorithm==1:
            if i==1:
                print("the starting set of features is : ",list(feature_set))
                print("the default rate is: ",start_acc_7)
            temp=best(feature_set,dataset)
            feature_set.add(temp[0])
        else:
            if i==1:
                temp1=set([i for i in range(1,250)])
                start = accuracy(temp1,250,dataset,1)
                print("starting set of features is :",list(feature_set))
                print("the starting accuracy =",start)
            temp=worst(feature_set,dataset)
            feature_set.remove(temp[0])
        if global_best_accuracy<temp[1]:
            global_best_accuracy=temp[1]
            global_best_features = list(feature_set)
        print("")
        print("current set of feature after round",i,"is:",list(feature_set))
        print("the best current accuracy =",temp[1])
print("")
print("the best global accuracy =",global_best_accuracy,"with features",global_best_features)
        
