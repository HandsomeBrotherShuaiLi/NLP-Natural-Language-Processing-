from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_digits
digits=load_digits()
X=digits.data
y=digits.target
X-=X.min()
X/=X.max()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35)
layers=[50,100,150,200,250]
iters=[1000,2000,3000,4000]
ans={}
max=0
key=None
for i in layers:
    for j in iters:
        model=MLPClassifier(hidden_layer_sizes=(i,),max_iter=j)
        model.fit(X_train,y_train)
        res=model.predict(X_test)
        count=0
        for w in range(len(y_test)):
            if y_test[w]==res[w]:
                count+=1
        print(("hidden_layer_sizes(%d,),max_iter%d,accuracy:%f")%(i,j,count/len(y_test)))
        ans[(i,j)]=count/len(y_test)
        if count/len(y_test)>max:
            max=count/len(y_test)
            key=(i,j)
print(("max accuracy is %f for thr args(hidden_layer_sizes and max_iter(%d,%d)")%(max,key[0],key[1]))

