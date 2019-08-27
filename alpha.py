from PyQt5 import QtWidgets, uic
#import time
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import association_rules
import random


def eval_func(a):
    return eval(str(a))
def mul_func(a):
    return int(a)*500
def make_list(a):
    return list(a)
def div_func(a):
    return a/500

def getItemsUsed(w,c):
    # item count
    i = c.__len__()-1
    # weight
    currentW =  len(c[0])-1
    
    # set everything to not marked
    marked = []
    for i in range(i+1):
        marked.append(0)

    while (i >= 0 and currentW >=0):
        # if this weight is different than
        # the same weight for the last item
        # then we used this item to get this profit
        #
        # if the number is the same we could not add
        # this item because it was too heavy		
        if (i==0 and c[i,np.int(currentW)] >0 )or c[i,np.int(currentW)] != c[i-1,np.int(currentW)]:
            marked[i] =1
            currentW = currentW-w[i]
        i = i-1
    return marked
# v = list of item values or profit
# w = list of item weight or cost
# W = max weight or max cost for the knapsack
def zeroOneKnapsack(profit, weight, total):
    # c is the cost matrix
    n = profit.__len__()
    #  set inital values to zero
    selection = np.zeros((n,total+1))
    #the rows of the matrix are weights
    #and the columns are items
    #cell c[i,j] is the optimal profit
    #for i items of cost j
    print(weight)
    #print(cost)
    #for every item
    for i in range(0,n):
        #for ever possible weight
        for j in range(0,total+1):
            #if this weight can be added to this cell
            #then add it if it is better than what we aready have

            if (weight[i] > j):
				# this item is to large or heavy to add
				# so we just keep what we aready have
				
                selection[i,j] = selection[i-1,j]
            else:
				# we can add this item if it gives us more value
				# than skipping it
				
				# c[i-1][j-w[i]] is the max profit for the remaining 
				# weight after we add this item.
				
				# if we add the profit of this item to the max profit
				# of the remaining weight and it is more than 
				# adding nothing , then it't the new max profit
				# if not just add nothing.
				
                selection[i,j] = np.maximum(selection[i-1,j],profit[i]+selection[i-1,j-np.int(weight[i])])
    return [selection[n-1,np.int(total)],getItemsUsed(weight,selection)]


def recommendation():
    df = pd.read_csv('files/newresultapriori.csv')
    df['itemsets'] = df['itemsets'].apply(eval_func)
    df['support'] = df['support'].apply(eval_func)
    df2 = pd.read_csv('files/TopActors.csv')
    df2 = df2.drop(columns=['Unnamed: 0'])
    df2['Top 10 Actors'] = df2['Top 10 Actors'].apply(eval_func)
    req = pd.read_csv('req.csv')
    req['normalizedRating'] = req['normalizedRating'].apply(eval_func)
    req['googleHits'] = req['googleHits'].apply(eval_func).apply(div_func)
    rules = association_rules(df,metric='lift',min_threshold=10)
    genre_list = ['Adventure','Action','Comedy','Crime','Drama','Family','Fantasy','Thriller','Romance','Horror','Musical']
    print(genre_list)
    bud1 = int(dig.budgetBox.toPlainText())
    budget = bud1*100000
    input_genre = dig.genreBox.currentText()
    abascus = list(df2[df2['Genre'] == input_genre.capitalize()]['Top 10 Actors'])
    top_actor = abascus[0][random.randint(0,9)][0]
    c = []
    a = list(rules[rules['antecedents'].apply(lambda x:set([top_actor]).issubset(x))]['consequents'])
    for each in a:
        if len(eval_func(each))>1:
              c.append(each)
    supporting_actors = list(frozenset.union(*c))
    supporting_actors.append(top_actor)
    daa = req.loc[req['actorName'].isin(supporting_actors)]
    profit = list(daa['normalizedRating'].values)
    cost = list(daa['googleHits'].values)
    W = np.int(div_func(budget))
#W = 50
    if W<0:
        print('Budget too low for the desired genre')
    select = zeroOneKnapsack(profit,cost,W)
    print(select)
    name_index = []
    for i in range(0,len(select[1])):
        if select[1][i] == 1:
            name_index.append(i)
        #print(name_index)
    bud = []
    for each in name_index:
        bud.append(cost[int(each)])
    name = []
    for each in name_index:
        name.append(supporting_actors[int(each)])
    #print(name)
    to = mul_func(sum(bud))    
    if to/100000>bud1:
        recommendation()
    else:
        res.show()
        res.finalBudget.setText(str(to/100000))
        res.actorList.clear()
        res.actorList.addItems(name) 
    






def actorEvaluation():
    budget = float(dig.budgetBox.toPlainText())
    genre = dig.genreBox.currentText()
    noOfActors = str(dig.noOfActors.value())
    
    res.show()
    #time.sleep(5)

    res.actorList.clear()
    res.actorList.addItems([str(budget),genre,noOfActors])
    

app = QtWidgets.QApplication([])
dig = uic.loadUi("projectUI.ui")
res = uic.loadUi("result.ui")

genreList = ['Adventure','Action','Comedy','Crime','Drama','Family','Fantasy','Thriller','Romance','Horror','Musical']
dig.genreBox.addItems(genreList)

dig.submit.clicked.connect(recommendation)
res.refreshResult.clicked.connect(recommendation)

dig.setWindowTitle("Star Cast Prediction")
res.setWindowTitle("Optimal star cast")

dig.show()
app.exec()