def test():
    print("PCAA test")
    return
def library():
    print("""import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
import kagglehub
import cv2""")
    return
def noklearn():
    print("""# %%
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt 

# %% [markdown]
# # LAB 1 (Matrix and Gradient Descent)
# 

# %%

a=np.array([[1,2,3],[4,5,6]])
b=np.array([[4,5],[6,7],[8,9]])
print(a)
print(b)

# %%
print(a.shape,b.shape)

# %%
###dot product(matrix mul)
c=np.dot(a,b)
print(c)

# %%
## Element wise multiplicationn
a=np.array([[1,2,3],[4,5,6]])
d = np.array([[2],[3]])
print(d.shape)
c1= a*d  ## same as the fisrt matrix, this is element wise multiplication(either row same or column same)
print(c1)


# %%
## now normal mul 
d=a*a
print(d)
e = np.dot(a,a.T)
print(e)

# %%
##Checking for time 
a=np.random.rand(10000)   ##10000,null
b=np.random.rand(10000)
a.shape

# %%
### cal time for dot product
tic=time.time()    
c=np.dot(a,b)
toc=time.time()
d= 1000*(toc-tic)
print(d)

# %%
### cal time for for loop
c=0
tic=time.time() 
for i in range(10000):
    c+=a[i]*b[i]     
toc=time.time()
d= 1000*(toc-tic)
print(c)
print(d)

# %%
a= np.random.rand(2,5)
b = np.random.rand(2,1)   #one row or column vector must be present 

# %%
a

# %%
b

# %%
a*b

# %%
##Operations 
a  = np.array([[1,2,3],[4,5,6]])
print(a)

# %%
a.sum(axis=1)  #horizontal sum

# %%
a.sum(axis=0)  ## vertical sum 

# %%
a+5   #will add in every element 

# %%
a= np.random.rand(6)
a.shape

# %%
a= np.random.rand(6).reshape(-1,1)
a.shape

# %%
d=np.dot(a,a.T)  ##(6,1)*(1,6)
d.shape

# %%
x = np.random.rand(3,3,2)       
x1=x.reshape(x.shape[0]*x.shape[1],x.shape[2])
x1.shape   

# %%
##reshape 
b=np.random.rand(2,3)
b.reshape(3,2)

# %%
##GRADIENT DESCENT 
x = np.array([0.8,1,1.2,1.4,1.6,1.8,2,2.2,2.4,2.6])
y = np.array([0.7,0.65,0.9,0.95,1.1,1.15,1.2,1.4,1.55,1.5])

##for lopp
theta0 = 0.10
theta1= 0.20
a = 0.01
m= x.shape[0]
cost =[]
epoch= 1000

for i in range(epoch):
    h = theta0+theta1*x
    j=np.sum((h-y)**2)/(2*m)
    dtheta0 = np.sum(h-y)/m
    dtheta1 =np.sum((h-y)*x)/m
    if i%500 ==0:
        print(f"cost:{j},iteration:{i}")
    theta0=theta0-a*dtheta0
    theta1=theta1-a*dtheta1
    cost.append(j)
    
print(theta0,theta1)
##PLOT
plt.plot(cost)

# %%
x.shape

# %%


# %%
# ASSIGNMENT  (using for loop)
x1 = np.array([0.4,0.8,1,1.2,1.4,1.6,1.8,2,2.4,2])
x2= np.array([0.8,1,1.2,1.4,1.6,1.8,2,2.2,2.4,2.6])
y =np.array([0.7,0.65,0.9,0.95,1.1,1.15,1.2,1.4,1.55,1.5])

theta0 = 0.10
theta1= 0.20
theta2 = 0.30
a=0.01
epoch=1000
m= x.shape[0]
cost =[]

for i in range(epoch):
    h = theta0+theta1*x1+theta2*x2
    j=np.sum((h-y)**2)/(2*m)
    dtheta0 = np.sum(h-y)/m
    dtheta1 =np.sum((h-y)*x1)/m
    dtheta2 =np.sum((h-y)*x2)/m
    if i%100 ==0:
        print(f"cost:{j},iteration:{i}")
    theta0=theta0-a*dtheta0
    theta1=theta1-a*dtheta1
    theta2=theta2-a*dtheta2
    cost.append(j)
    
print(theta0,theta1,theta2)


# %%
##using function 
x1 = np.array([0.4,0.8,1,1.2,1.4,1.6,1.8,2,2.4,2])
x2= np.array([0.8,1,1.2,1.4,1.6,1.8,2,2.2,2.4,2.6])
y =np.array([0.7,0.65,0.9,0.95,1.1,1.15,1.2,1.4,1.55,1.5])
x=np.array([x1,x2])

def LGD(x1,x2,y,a,epoch):
    theta0 = 0.10
    theta1= 0.20
    theta2 = 0.30
    m= x1.shape[0]
    cost =[]

    for i in range(epoch):
            
        h = theta0+theta1*x1+theta2*x2
        j=np.sum((h-y)**2)/(2*m)
        dtheta0 = np.sum(h-y)/m
        dtheta1 =np.sum((h-y)*x1)/m
        dtheta2 =np.sum((h-y)*x2)/m
        if i%100 ==0:
            print(f"cost:{j},iteration:{i}")
        theta0=theta0-a*dtheta0
        theta1=theta1-a*dtheta1
        theta2=theta2-a*dtheta2
        cost.append(j)
        plt.plot(cost)
    
    print(theta0,theta1,theta2)

# %%
x.shape

# %%
LGD(x1,x2,y,0.01,1000)

# %%
""")
def yesklearn():
 print("""# %%
##Check the answer using linear regression (sklearn)
import sklearn.linear_model as lm

# %%
x = np.array([x1,x2])
x.T    ##for m,nx


# %%
lr = lm.LinearRegression()
lr.fit(x.T,y)
print(lr.intercept_)
print(lr.coef_)

# %% [markdown]
# # LAB 2 (ML GRADIENT DESCENT)

# %%
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt 

# %%
np.random.seed(5)
X = np.array([[5,3],[6,4],[7,6],[9,8]])
y = np.array([2,4,7,8]).reshape(-1,1)
print(X)
print()
print(y)

# %%
##Function 

def lgr(X,y,lr,epoch):
    m = X.shape[0]
    nx =X.shape[1]
    w = np.random.rand(nx,1)
    b=0
    cost=[]
    
    for i in range(epoch):
        h = np.dot(X,w)+b          
        error= (h-y)
        cost1 =np.dot(error.T,error)/(2*m)   ## (h-y)**2/2m
        cost.append(cost1)
        dw = np.dot(X.T,error)/m        ## (2,4) (4,1)= (2,1)  (h-y)x/m
        db = np.sum(h-y)/m              ## (h-y)/m
        w= w -lr*dw
        b=b-lr*db
    return w,b


# %%

lgr(X,y,0.01,100000)

# %%
##Question 1
np.random.seed(123)
X= np.random.rand(100,8)
y= np.random.rand(100,1)

# %%
##Function 

def lgr(X,y,lr,epoch):
    m = X.shape[0]
    nx =X.shape[1]
    w = np.random.rand(nx,1)
    b=0
    cost=[]
    
    for i in range(epoch):
        h = np.dot(X,w)+b
        error= (h-y)
        cost1 =np.dot(error.T,error)/(2*m)
        cost.append(cost1[0])
        dw = np.dot(X.T,error)/m        #(h-y)x/m
        db = np.sum(h-y)/m
        w= w -lr*dw
        b=b-lr*db
    plt.plot(cost)
    return w,b

# %%
lgr(X,y,0.01,100000)

# %%
##Question 2
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt 
from sklearn.preprocessing import scale

# %%
df = pd.read_csv("advertising.csv")
df

# %%
df[["TV","Radio","Newspaper"]]=scale(df[["TV","Radio","Newspaper"]],with_mean=True ,with_std =True)

# %%
X = df.iloc[:,0:3]
y = df.iloc[:,-1]
X = np.asarray(X)
y = np.asarray(y).reshape(-1,1)

# %%
def lgr(X,y,lr,epoch):
    m = X.shape[0]
    nx =X.shape[1]
    w = np.random.rand(nx,1)
    b=0
    cost=[]
    
    for i in range(epoch):
        h = np.dot(X,w)+b
        error= (h-y)
        cost1 =np.dot(error.T,error)/(2*m)
        cost.append(cost1[0])
        dw = np.dot(X.T,error)/m        ## 
        db = np.sum(h-y)/m
        w= w -lr*dw
        b=b-lr*db
    plt.plot(cost)
    return w,b

# %%
lgr(X,y,0.01,10000)

# %%
#ASSIGNMENT 2

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt 
from sklearn.preprocessing import scale
import sklearn.linear_model as lm

# %%
df = pd.read_csv("auto.csv")
df

# %%
df[['displacement', 'horsepower', 'weight', 'acceleration']]=scale(df[['displacement', 'horsepower', 'weight', 'acceleration']],with_mean=True ,with_std =True)

# %%
df

# %%
X = df.iloc[:,0:5]
y = df.iloc[:,-1]
X = np.asarray(X)
y = np.asarray(y).reshape(-1,1)


# %%
def lgr(X,y,lr,epoch):
    m = X.shape[0]
    nx =X.shape[1]
    w = np.random.rand(nx,1)
    b=0
    cost=[]
    
    for i in range(epoch):
        h = np.dot(X,w)+b
        error= (h-y)
        cost1 =np.dot(error.T,error)/(2*m)
        cost.append(cost1[0])
        dw = np.dot(X.T,error)/m        ## 
        db = np.sum(h-y)/m
        w= w -lr*dw
        b=b-lr*db
    plt.plot(cost)
    return w,b

# %%
lgr(X,y,0.01,100000)

# %%
##CHECK
model=lm.LinearRegression()
model.fit(X,y)
print(model.coef_)
print(model.intercept_)

# %% [markdown]
# # LAB 3 (Logistic Gradient Descent)

# %%
##Question
X1=np.array([[1.,2.,-1.],[3.,4.,-3.2]])
Y1=np.array([[1,0,1]])
print(X1)
print()
print(Y1)

# %%
X=X1.T
Y=Y1.T #Converting NN to ML set

# %%
def sigmoid(z):
    a=1/(1+np.exp(-z))
    return a

# %%
def LOGR(X,Y,lr,epoch):

    m=X.shape[0]
    nx=X.shape[1]
    w=np.random.rand(nx,1)
    b=0
    cost=[]
    for i in range(epoch):
        h =np.dot(X,w)+b
        a=sigmoid(h)
        cost1=-(np.sum(Y*np.log(a)+(1-Y)*np.log(1-a)))/m
        cost.append(cost1)
        dw=np.dot(X.T,(a-Y))/m
        db=(np.sum(a-Y))/m
        w=w-lr*dw
        b=b-lr*db
    plt.plot(cost)
    return w,b
    

# %%
LOGR(X,Y,0.01,100)

# %%
##Assignment 
x=pd.read_csv("Iris.csv")
x


# %%
x=x.drop(["Id"],axis=1)

# %%
x

# %%
x=x.iloc[:100]
x

# %%
X_1= x.iloc[:,0:4]
Y_1 =x.iloc[:,-1]


# %%
X_1=np.asarray(X_1)
Y_1=np.array(Y_1).reshape(-1,1)   ##check the shape before doing asarray 
Y_1.shape

# %%
from sklearn.preprocessing import LabelEncoder
#Y_1=Y_1.replace("Iris-setosa",1)
#Y_1=Y_1.replace("Iris-versicolor",0)
le =LabelEncoder()
Y_1=le.fit_transform(Y_1).reshape(-1,1)

# %%
Y_1.shape

# %%
def LOGR(X,Y,lr,epoch):

    m=X.shape[0]
    nx=X.shape[1]
    w=np.random.rand(nx,1)
    b=0
    cost=[]
    for i in range(epoch):
        h =np.dot(X,w)+b
        a=sigmoid(h)
        cost1=-(np.sum(Y*np.log(a)+(1-Y)*np.log(1-a)))/m
        cost.append(cost1)
        dw=np.dot(X.T,(a-Y))/m
        db=(np.sum(a-Y))/m
        w=w-lr*dw
        b=b-lr*db
    plt.plot(cost)
    return w,b
    

# %%
w,b =LOGR(X_1,Y_1,0.01,10000)

# %%
##yhat
y=np.dot(X_1,w)+b
y.shape

# %%
a=sigmoid(y)
a.shape

# %%
yhat= np.array( [np.round(x) for x in a]).reshape(-1,1)

# %%
np.sum(yhat)

# %%
##c=[np.round(x) for x in Y_1] 

# %%
##np.sum(c)

# %%
##Confusion Matrix
from sklearn import metrics
m=metrics.confusion_matrix(Y_1,yhat)

# %%
m

# %% [markdown]
# # LAB 4 (Activation functions and Forward propagation)

# %%
##1.Sigmoid Activation Function 
def sig(z):
    s=1/(1+np.exp(-z))
    return s

def dsig(s):
    das=s*(1-s)
    return das


# %%
##TANH ACTIVATION FUNCTION
def tanh(z):
    s= (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))
    return s

def dtanh(s):
    dat=(1-s**2)
    return dat
    

# %%
##Relu activation function 
def relu(z):
    s=np.maximum(0,z)
    return s 

def drelu(s):
    dar=(np.int64(s>0))
    return dar

# %%
##Leaky Relu 
def lrelu(z):
    s=np.maximum(0.01*z,z)     ## we can also take 0.01
    return s 

def dlrelu(s,alpha=0.01):
    dal=(np.where(s>0,1,alpha))
    return dal



# %%
##Softmax (similar as sigmoid , with multiple dimension and used for multiclass)
def softmax(z):
    e = np.exp(z)
    s=e/np.sum(e)
    return s

# %%

X=np.random.randn(2,3)
print(X)
y = (np.random.randn(1,3)>0)   ## if > 0 its true or else its false
print(y)
y.shape[1]

# %%
##Forward Propagation

##DEFINE THE SHAPE 
def layers_size(X,y,node):
    n_x=X.shape[0]
    n_h= node
    n_y=y.shape[0]
    return n_x,n_y,n_h

np.random.seed(2)
#initialization 
def intz(n_x,n_y,n_h):
    w1=np.random.randn(n_h,n_x)*0.01   ##0.01 value chota krne liya hai , can be ignored 
    b1= np.zeros((n_h,1))
    w2=np.random.randn(n_y,n_h)*0.01
    b2= np.zeros((n_y,1))   
    
    parameters = {"w1":w1,"b1":b1,"w2":w2,"b2":b2}   ##for ease 
    return parameters 


##Forward Propogation 
def fwd(X,parameters):
    w1=parameters["w1"]
    b1=parameters["b1"]
    w2=parameters["w2"]
    b2=parameters["b2"]
    
    z1= np.dot(w1,X)+b1
    a1=tanh(z1)  ## np.tanh
    z2=np.dot(w2,a1)+b2
    a2=np.array(sig(z2))
    
    cache={"z1":z1,"a1":a1,"z2":z2,"a2":a2}
    return a2,cache 

##COST 
def compute_cost(a2,y):
    m= y.shape[1]
    logp =np.multiply(np.log(a2),y)+np.multiply(np.log(1-a2),(1-y))
    cost = -np.sum(logp)/m
    cost = float(np.squeeze(cost))    ## optional 
    return cost 
    


# %%
a,b,c = layers_size(X,y,4)  ##4 nodes

# %%
parameters = intz(a,b,c)
parameters

# %%
a2 , cache = fwd(X,parameters)
cache

# %%
cost =compute_cost(a2,y)
cost

# %%
#Backward Propagation
def BWP(parameters,X,y,cache):
    w1=parameters["w1"]
    b1=parameters["b1"]
    w2=parameters["w2"]
    b2=parameters["b2"]
    
    a1= cache["a1"]
    a2= cache["a2"]
    
    m=y.shape[1]  ##y.size
    
    dz2=a2-y
    dw2 = np.dot(dz2,a1.T)/m
    db2=np.sum(dz2,axis=1,keepdims=True)/m
    da1= np.dot(w2.T,dz2)
    dz1= da1*(1-a1**2) ##np.power(a1,2) , dtanh(a1)
    dw1=np.dot(dz1,X.T)/m
    db1=np.sum(dz1,axis=1,keepdims=True)/m
    
    grades = {"dw1":dw1,"db1":db1,"dw2":dw2,"db2":db2}
    return grades

#7.Update Grades
def update(parameters,grades,lr=0.01):
    w1=parameters["w1"]
    b1=parameters["b1"]
    w2=parameters["w2"]
    b2=parameters["b2"]

    dw1=grades["dw1"]
    db1=grades["db1"]
    dw2=grades["dw2"]
    db2=grades["db2"]


    w1=w1-lr*dw1
    b1=b1-lr*db1
    w2=w2-lr*dw2
    b2=b2-lr*db2

    parameters={"w1":w1,"b1":b1,"w2":w2,"b2":b2}

    return parameters

# %%
grades=BWP(parameters,X,y,cache)
grades

# %%
parameters=update(parameters,grades,lr=0.01)
print(parameters)

# %%
##CREATE OWN NN
def NN(X,y,itr=10000,print_cost=True,layers=4):
    np.random.seed(3)
    n_x,n_h,n_y=layers_size(X, y,layers)
    parameters=intz(n_x, n_h, n_y)

    for i in range (itr):
        a2, cache = fwd(X, parameters)
        cost=compute_cost(a2, y)
        grades=BWP(parameters,X,y,cache)
        parameters=update(parameters,grades,lr=0.01)

        if print_cost and i%100==0:
            print(f"cost{i}: {cost}")
            
    return parameters

# %%
NN(X,y)

# %%
##Assignment 5 
X= np.random.randn(4,10)
y = (np.random.randn(1,10)>0) 


# %%
##Forward Propogation
np.random.seed(1)
def layers_size(X,y,node1,node2,node3):
    n_x=X.shape[0]
    n_h1= node1
    n_h2=node2
    n_h3=node3
    n_y=y.shape[0]
    return n_x,n_y,n_h1,n_h2,n_h3

def intz(n_x,n_y,n_h1,n_h2,n_h3):
    w1=np.random.randn(n_h1,n_x)*0.01   ##0.01 value chota krne liya hai , can be ignored 
    b1= np.zeros((n_h1,1))
    w2=np.random.randn(n_h2,n_h1)*0.01
    b2= np.zeros((n_h2,1))
    w3=np.random.randn(n_h3,n_h2)*0.01
    b3= np.zeros((n_h3,1))
    w4=np.random.randn(n_y,n_h3)*0.01
    b4= np.zeros((n_y,1))
    
    
    parameters = {"w1":w1,"b1":b1,"w2":w2,"b2":b2,"w3":w3,"b3":b3,"w4":w4,"b4":b4}   ##for ease 
    return parameters 

def fwd1(X,parameters):
    w1=parameters["w1"]
    b1=parameters["b1"]
    w2=parameters["w2"]
    b2=parameters["b2"]
    w3=parameters["w3"]
    b3=parameters["b3"]
    w4=parameters["w4"]
    b4=parameters["b4"]
    
    z1= np.dot(w1,X)+b1
    a1=relu(z1)               ## np.tanh
    z2=np.dot(w2,a1)+b2
    a2=relu(z2)
    z3=np.dot(w3,a2)+b3
    a3=lrelu(z3)
    z4=np.dot(w4,a3)+b4
    a4=sig(z4)
    
    
    cache={"z1":z1,"a1":a1,"z2":z2,"a2":a2,"z3":z3,"a3":a3,"z4":z4,"a4":a4}
    return a4,cache 

def compute_cost(a4,y):
    m= y.shape[1]
    logp =np.multiply(np.log(a4),y)+np.multiply(np.log(1-a4),(1-y))
    cost = -np.sum(logp)/m
    cost = float(np.squeeze(cost))    ## optional 
    return cost 


# %%
n_x,n_y,n_h1,n_h2,n_h3=layers_size(X,y,4,3,2)

# %%
parameters= intz(n_x,n_y,n_h1,n_h2,n_h3)
parameters

# %%
a4 , cache = fwd1(X,parameters)
cache

# %%
x = compute_cost(a4,y)
x

# %%
##Backward Prpogation
def BWP1(parameters,X,y,cache):
    w1=parameters["w1"]
    b1=parameters["b1"]
    w2=parameters["w2"]
    b2=parameters["b2"]
    w3=parameters["w3"]
    b3=parameters["b3"]
    w4=parameters["w4"]
    b4=parameters["b4"]
    
    
    a1= cache["a1"]
    a2= cache["a2"]
    a3= cache["a3"]
    a4 = cache["a4"]
    
    m=y.shape[1]  ##y.size
    
    dz4=a4-y
    dw4 =np.dot(dz4,a3.T)/m
    db4=np.sum(dz4,axis=1,keepdims=True)/m
    da3= np.dot(w4.T,dz4)
    
    dz3= da3*dlrelu(a3) ##np.power(a1,2) , dtanh(a1)
    dw3=np.dot(dz3,a2.T)/m
    db3=np.sum(dz3,axis=1,keepdims=True)/m
    da2= np.dot(w3.T,dz3)
    
    dz2=da2*drelu(a2)
    dw2 = np.dot(dz2,a1.T)/m
    db2=np.sum(dz2,axis=1,keepdims=True)/m
    da1= np.dot(w2.T,dz2)
    
    dz1= da1*drelu(a1)
    dw1=np.dot(dz1,X.T)/m
    db1=np.sum(dz1,axis=1,keepdims=True)/m
    
    
    grades = {"dw4":dw4,"db4":db4,"dw3":dw3,"db3":db3,"dw2":dw2,"db2":db2,"dw1":dw1,"db1":db1}
    return grades

# %%
##7.Update Grades
def update1(parameters,grades,lr=0.01):
    w1=parameters["w1"]
    b1=parameters["b1"]
    w2=parameters["w2"]
    b2=parameters["b2"]
    w3=parameters["w3"]
    b3=parameters["b3"]
    w4=parameters["w4"]
    b4=parameters["b4"]
   
    

    dw1=grades["dw1"]
    db1=grades["db1"]
    dw2=grades["dw2"]
    db2=grades["db2"]
    dw3=grades["dw3"]
    db3=grades["db3"]
    dw4=grades["dw4"]
    db4=grades["db4"]


    w1=w1-lr*dw1
    b1=b1-lr*db1
    w2=w2-lr*dw2
    b2=b2-lr*db2
    w3=w3-lr*dw3
    b3=b3-lr*db3
    w4=w4-lr*dw4
    b4=b4-lr*db4

    parameters= {"w4":w4,"b4":b4,"w3":w3,"b3":b3,"w2":w2,"b2":b2,"w1":w1,"b1":b1}

    return parameters

# %%
def NN1(X,y,itr=10000,print_cost=True):
    np.random.seed(3)
    n_x,n_y,n_h1,n_h2,n_h3=layers_size(X,y,4,3,2)
    parameters= intz(n_x,n_y,n_h1,n_h2,n_h3)
    
    cost = []

    for i in range (itr):
        a4, cache = fwd1(X, parameters)
        cost1=compute_cost(a4, y)
        cost.append(cost1)
        grades=BWP1(parameters,X,y,cache)
        parameters=update(parameters,grades,lr=0.01)

        if print_cost and i%1000==0:
            print("cost % i:%f" %(i,cost1))
    plt.plot(cost)        
    return parameters

# %%
grades = BWP1(parameters,X,y,cache)
grades

# %%
parameters=update1(parameters,grades,lr=0.01)
print(parameters)

# %%
NN1(X,y,itr=1000)

# %% [markdown]
# # LAB 5 (ANN Tensorflow)
# 

# %%
##Binary 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense ##dense for ann , con for cnn
import matplotlib.pyplot as plt

# %%
from numpy import loadtxt  ##for dataset 

# %%
df = loadtxt('diabetes.csv',delimiter=',')
df

# %%
X = df[:,0:8]
Y= df[:,8]

# %%
X.shape

# %%
Y.shape

# %%
## NN - Build a 3 layers model(layer_1 with 12 nodes with activation function relu, layer_2 with 8 nodes with activation function relu and layer_3 with output layer)

# %%
model = Sequential()
model.add(Dense(12,activation='relu',input_shape=(8,)))
model.add(Dense(8,activation='relu'))
model.add(Dense(1,activation='sigmoid'))   ##binary cross entropy ,if linear write linear

## 108+104+9 = 221 total parameters

# %%
model.summary()

# %%
## cost is called as compile 
model.compile(loss='binary_crossentropy',optimizer = 'adam',metrics=['accuracy'])

# %%
model.fit(X,Y,epochs =100,batch_size=10)
## stochastic gradient , all together 
## batch gradient , uses output of one as the initialization of the second

# %%
history_X= model.fit(X,Y,epochs=100,batch_size=10)

# %%
plt.plot(history_X.history['loss'],label='train')

# %%
## increase epoch 
history_X= model.fit(X,Y,epochs=100)

# %%
plt.plot(history_X.history['loss'],label='train')

# %%
model.evaluate(X,Y) ##Accuracy

# %%
P =model.predict(X)
Y_P=(P>0.5).astype(int)

# %%
print(Y_P)

# %%
## MULTICLASS
from keras.datasets import mnist
(train_images,train_labels),(test_images,test_labels)=mnist.load_data()

# %%
train_images.shape


# %%
test_images.shape


# %%
plt.imshow(test_images[102,:,:])         

# %%
##NN , 512 nodes with nodes
model = Sequential()
model.add(Dense(512,activation='relu',input_shape=(28*28,)))   ## greay scale , *3 if RGB
model.add(Dense(10,activation='softmax'))

# %%
model.summary()

# %%
## cost is called as compile 
model.compile(loss='categorical_crossentropy',optimizer = 'rmsprop',metrics=['accuracy'])

# %%
## Get it in proper structure 
train_images=train_images.reshape(60000,28*28) ##train_images.shape[0],train_images.shape[1]*train_images.shape[2]
## To make it standardise 
train_images =train_images.astype('float32')/255

test_images=test_images.reshape(10000,28*28)
test_images =test_images.astype('float32')/255


# %%
train_images.shape
test_images.shape

# %%
train_labels

# %%
## now for one hot encoding 
from tensorflow.keras.utils import to_categorical
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# %%
print(train_labels)

# %%
history_X =model.fit(train_images,train_labels,epochs =10,batch_size=128)


# %%
plt.plot(history_X.history['loss'],label='train')

# %%
train_loss,train_accuracy = model.evaluate(train_images,train_labels)
test_loss,test_accuracy = model.evaluate(test_images,test_labels)

# %%
print(train_loss,train_accuracy)

# %%
##ASSIGNMENT(ANN MULTICLASS)
from keras.datasets import fashion_mnist
(train_images,train_labels),(test_images,test_labels)=fashion_mnist.load_data()


# %%
train_images.shape


# %%
test_images.shape


# %%
plt.imshow(test_images[234,:,:])         

# %%
##NN , 512 nodes with nodes
model = Sequential()
model.add(Dense(1028,activation='relu',input_shape=(28*28,)))  ## greay scale , *3 if RGB
model.add(Dense(512,activation='leaky_relu')) 
model.add(Dense(10,activation='softmax'))

# %%
model.summary()

# %%
## cost is called as compile 
model.compile(loss='categorical_crossentropy',optimizer = 'rmsprop',metrics=['accuracy'])

# %%
## Get it in proper structure 
train_images=train_images.reshape(60000,28*28) ##train_images.shape[0],train_images.shape[1]*train_images.shape[2]
## To make it standardise 
train_images =train_images.astype('float32')/255

test_images=test_images.reshape(10000,28*28)
test_images =test_images.astype('float32')/255



# %%
train_labels

# %%
## now for one hot encoding 
from tensorflow.keras.utils import to_categorical
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# %%
print(train_labels)

# %%
history_X =model.fit(train_images,train_labels,epochs =10,batch_size=128)


# %%
plt.plot(history_X.history['loss'],label='train')

# %%
train_loss,train_accuracy = model.evaluate(train_images,train_labels)
test_loss,test_accuracy = model.evaluate(test_images,test_labels)

# %%
print(train_loss,train_accuracy)

# %%
model.predict(test_images).round()

# %% [markdown]
# # Image Classification

# %%
import cv2
import numpy as np
from matplotlib import pyplot as plt 
from numpy import asarray
from PIL import Image
import os
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense ##dense for ann , con for cnn
import pickle

# %%
cap = cv2.VideoCapture(0)
count = 0
while True:
    ret, frame = cap.read()
    count += 1
    face = cv2.resize(frame, (200,400))
    file_name_path = "C:/Users/rodea/OneDrive/Desktop/FOML/Images/WITH/" + str(count) + '.jpg'
    cv2.imwrite(file_name_path, face)
    cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
    cv2.imshow('Face Cropper', face)

    if cv2.waitKey(1) == 13 or count == 20:
        break

cap.release()
cv2.destroyAllWindows()
print("Collecting Samples Complete")

# %%
img = 'C:/Users/rodea/OneDrive/Desktop/FOML/Images/WITH'
img2 = 'C:/Users/rodea/OneDrive/Desktop/FOML/Images/WITHOUT'

# %%
def get_image_array(path):
    image_list=os.listdir(path)
    images=[]
    for img in image_list:
        img=cv2.imread(path+ '/' + img,0)
        images.append(img)
    return np.array(images)

# %%
img1=get_image_array(img) ##WITH
img1.shape

# %%
img2 = get_image_array(img2)  #WITHOUT
img2.shape

# %%
fig=plt.figure(figsize=(8,6))
for i in range (20):
    ax=fig.add_subplot(4,5,i+1,xticks=[],yticks=[])
    ax.imshow(img1[i],cmap=plt.cm.bone)

# %%
train_image1 = img1.reshape((20,400*200))
train_image1 = train_image1.astype('float32')/255
train_image2 = img2.reshape((20,400*200))
train_image2 = train_image2.astype('float32')/255

# %%
images_con = np.concatenate((train_image1,train_image2))

# %%
Y = np.concatenate((np.ones(20,dtype=int),np.zeros(20,dtype=int)))


# %%
Y.shape

# %%
model = Sequential()
model.add(Dense(32,activation='relu',input_shape=(400*200,)))
model.add(Dense(16,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

# %%
model.summary()

# %%
## cost is called as compile 
model.compile(loss='binary_crossentropy',optimizer = 'adam',metrics=['accuracy'])

# %%
model.fit(images_con,Y,epochs =100,batch_size=10)
## stochastic gradient , all together 
## batch gradient , uses output of one as the initialization of the second

# %%
history_X= model.fit(images_con,Y,epochs=100,batch_size=10)

# %%
model.evaluate(images_con,Y) ##Accuracy

# %%
model.predict(images_con).round()

# %%
img1 = 'C:/Users/rodea/OneDrive/Desktop/FOML/Images/WITHTEST'
img2 = 'C:/Users/rodea/OneDrive/Desktop/FOML/Images/WITHOUTTEST'

# %%
img1=get_image_array(img1) ##WITH
img1.shape

# %%
img2=get_image_array(img2) ##WITH
img2.shape

# %%
test_image1 = img1.reshape((5,400*200))
test_image1 = test_image1.astype('float32')/255
test_image2 = img2.reshape((5,400*200))
test_image2 = test_image2.astype('float32')/255

# %%
model.predict(test_image1).round()    ## this should predict one 

# %%
model.predict(test_image2).round()

# %%
##for multiclass
#Multiclass


# Generate example labels for 7 classes (0 to 6)
#labels = y = np.repeat([0,1],50)

# Perform one-hot encoding
#y = tf.keras.utils.to_categorical(labels)
# Print the first 10 encoded labels for demonstration
#print(y[10])

# %% [markdown]
# # LDA(Linear Discriminant Analysis)

# %%
##INTUITION AND STEP BY STEP CODE 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
df = pd.read_excel("lda data.xlsx")

# %%
df

# %%
plt.scatter(df.iloc[:,0],df.iloc[:,1],c=df.iloc[:,2]) #2 is class, 0 is x1, 1 is x2
plt.show()

# %%
df.shape #(m,nx)

# %%
df1=df[df["Group"]==1]
df2=df[df["Group"]==2]

# %%
#Calculate between variability
u11=np.mean(df1['X1'])
u21=np.mean(df1['X2'])
u12=np.mean(df2['X1'])
u22=np.mean(df2['X2'])

mu=[u11-u12,np.round(u21-u22)] #rounded as the fraction part might create problems
mu=np.array(mu).reshape(1,2)

SB=np.dot(mu.T,mu)
SB

# %%
#Calc within variability 
df1['x1']=df1['X1']-u11
df1['x2']=df1["X2"]-u21
df2['x1']=df2['X1']-u12
df2['x2']=df2['X2']-u22

# %%
df1

# %%
x12=df1.iloc[:,3:5] #Group1 (x-mean(x))
x22=df2.iloc[:,3:5] #Group2 (x-mean(x))
sw1=np.dot(x12.T,x12)/len(df1)
sw2= np.dot(x22.T,x22)/len(df2)
sw = sw1+sw2
sw

# %%
A = np.dot(np.linalg.pinv(sw),SB)
A

# %%
#calculate eigen val and eigen vectors
eigval,eigvec=np.linalg.eig(A)
eigval,eigvec

# %%
#pick the highest eigen values--. vector
idx=eigval.argsort()[::-1]
print(idx)
val=eigval[idx]
print(val)
eigvec=eigvec[:,idx]
print(eigvec)
eig=eigvec[:,:1]
eig

# %%
df1

# %%
##Scalar Projections  (Eigen vector(unit vector) multiplied with the classes)
k = df1.iloc[:,0:2]            #z score
length_C1 = np.dot(k,eig)
l = df2.iloc[:,0:2]
length_C2 = np.dot(l,eig)
print(length_C1)
print()
print(length_C2)


# %%
##Vector Projection (scalar proj * eigen vetor)
proj_1 = length_C1*eig.T
proj_2 = length_C2*eig.T
print(proj_1)
##CUTOFF POINT AND PREDICTION REMAINING

# %%
p1=pd.DataFrame(proj_1)
p2=pd.DataFrame(proj_2)
df_new=pd.concat([p1, p2])
plt.scatter(df_new.iloc[:,0],df_new.iloc[:,1],c=df.iloc[:,2])
plt.show()

# %%
#USING SKLEARN 
##Calculate the grant mean then creat cut off point and findout the misclassification

# %%

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler, LabelEncoder
X = df.iloc[:,0:2].values
y = df.iloc[:,2:3].values
#sc = StandardScaler()
#X = sc.fit_transform(X)
#le = LabelEncoder()
#y = le.fit_transform(y)

# %%

lda = LDA(n_components=1)     ## N-1 , AND BY DEFAULT IT WILL BE 1 
k = lda.fit(X,y)
X_lda = lda.transform(X)   ## transform it to 1 dimension(dimensions are reduced) (here 10 rows but only 1 column(feature))
predict = lda.predict(X)


# %%
from sklearn.metrics import confusion_matrix  
from sklearn.metrics import accuracy_score

cm = confusion_matrix(y, predict)  
print(cm)  
print('Accuracy' + str(accuracy_score(y, predict))) 

# %%
##ASSIGNMENT IRIS DATASET

# %%
df=pd.read_csv('Iris.csv')
df

# %%
setosa = df.iloc[0:50]
versicolor = df.iloc[50:100]
virginica = df.iloc[100:150]

# %%
mu11 = setosa["SepalLengthCm"].mean()
mu21 = versicolor["SepalLengthCm"].mean()
mu31 = virginica["SepalLengthCm"].mean()
mu12 = setosa["SepalWidthCm"].mean()
mu22 = versicolor["SepalWidthCm"].mean()
mu32 = virginica["SepalWidthCm"].mean()
mu13 = setosa["PetalLengthCm"].mean()
mu23 = versicolor["PetalLengthCm"].mean()
mu33 = virginica["PetalLengthCm"].mean()
mu14 = setosa["PetalWidthCm"].mean()
mu24 = versicolor["PetalWidthCm"].mean()
mu34 = virginica["PetalWidthCm"].mean()

# %%
mu_1 = np.array([mu11,mu21,mu31]) - df["SepalLengthCm"].mean() #sepalLength
mu_2 = np.array([mu12,mu22,mu32]) - df["SepalWidthCm"].mean()
mu_3 = np.array([mu13,mu23,mu33]) - df["PetalLengthCm"].mean()
mu_4 = np.array([mu14,mu24,mu34]) - df["PetalWidthCm"].mean()

# %%
mu = np.array([mu_1,mu_2,mu_3,mu_4])
mu.shape

# %%
SB = np.dot(mu,mu.T)
SB

# %%
sw_1 = setosa["SepalLengthCm"] - setosa["SepalLengthCm"].mean()

# %%
s1 = np.array([setosa["SepalLengthCm"] - mu11,setosa["SepalWidthCm"] - mu12,setosa["PetalLengthCm"] - mu13,setosa["PetalWidthCm"] - mu14])

s2 = np.array([versicolor["SepalLengthCm"] - mu21,versicolor["SepalWidthCm"] - mu22,versicolor["PetalLengthCm"] - mu23,versicolor["PetalWidthCm"] - mu24])

s3 = np.array([virginica["SepalLengthCm"] - mu31,virginica["SepalWidthCm"] - mu32,virginica["PetalLengthCm"] - mu33,virginica["PetalWidthCm"] - mu34])

# %%
s1

# %%
sw1 = np.dot(s1,s1.T)/50
sw2 = np.dot(s2,s2.T)/50
sw3 = np.dot(s3, s3.T)/50
SW = sw1 + sw2 + sw3

# %%
A = np.dot(np.linalg.pinv(SW), SB)
A

# %%
eigenvalues, eigenvectors = np.linalg.eig(A)
print(eigenvalues,eigenvectors)

# %%
idx = eigenvalues.argsort()[::-1]
values = eigenvalues[idx]
eig = eigenvectors[:,:1]
eig

# %%
k = setosa.iloc[:,1:5]
length_C1  = np.dot(k,eig)
l = versicolor.iloc[:,1:5]
length_C2  = np.dot(l,eig)
m = virginica.iloc[:,1:5]
length_C3  = np.dot(m,eig)

# %%
proj2 = eig.T*length_C2
proj1 = eig.T * length_C1
proj3 = eig.T*length_C3

# %%
proj1

# %%
p2 = pd.concat([pd.DataFrame(proj1),pd.DataFrame(proj2),pd.DataFrame(proj3)])
p2

# %%
import matplotlib.pyplot as plt
plt.scatter(p2[0],p2[1], c=df.iloc[:,4])

# %%
##USING LIBRARIES

# %%
##LDA thriugh sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler, LabelEncoder
X = df.iloc[:,1:5].values
y = df.iloc[:,5].values
#sc = StandardScaler()
#X = sc.fit_transform(X)
#le = LabelEncoder()
#y = le.fit_transform(y)

# %%
lda = LDA(n_components=2)     ## N-1 , AND BY DEFAULT IT WILL BE 1 
k = lda.fit(X,y)
X_lda = lda.transform(X)
predict = lda.predict(X)

# %%
from sklearn.metrics import confusion_matrix  
from sklearn.metrics import accuracy_score

cm = confusion_matrix(y, predict)  
print(cm)  
print('Accuracy' + str(accuracy_score(y, predict))) 

# %%
import matplotlib.pyplot as plt 
plt.scatter(X_lda[51:100,0],X_lda[51:100,1]) 
plt.scatter(X_lda[0:50,0],X_lda[0:50,1]) 
plt.scatter(X_lda[101:150,0],X_lda[101:150,1])

# %%
## for n components = 1
#import matplotlib.pyplot as plt 
#plt.scatter(X_lda[51:100,0],X_lda[51:100,0]) 
#plt.scatter(X_lda[0:50,0],X_lda[0:50,0]) 
#plt.scatter(X_lda[101:150,0],X_lda[101:150,0])

# %% [markdown]
# # Principal Component Analysis (PCA)

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_excel("PCA.xlsx")
df

# %%
M = np.mean(df,axis=0)
c=df-M
c

# %%
plt.scatter(c["X1"],c["X2"])

# %%
Sw = np.cov(c.T)   ## cov goes in neural network therefore go for transform 
Sw


# %%
eigval,eigvec=np.linalg.eig(Sw)
idx=eigval.argsort()[::-1]
val=eigval[idx]
eigvec=eigvec[:,idx]
eig1=eigvec[:,:1]
eig2=eigvec[:,1:]
eig1,eig2

# %%
z1 =np.dot(c,eig1)   # length 
z2 =np.dot(c,eig2)

# %%
p1 = z1*eig1.T
p2 = z2*eig2.T
print(p1)
print(p2)

# %%
plt.scatter(p1[:,0],p1[:,1])
plt.scatter(p2[:,0],p2[:,1])

# %%
##PCA BY LIBRARIES
##Idea - look into the eigen values(pca.explained_variance_) , take 80-90%, now take that many number of features in PcA and perform again 
##This will Reduce the dimension , take the transform(vector projections) of this X and make a dataframe and then do ann and lda for checking accuracy
from sklearn.decomposition import PCA
pca=PCA()   ## write the number of dimnesion we need , or all in default
pca.fit(df)   ## fit the data
print(pca.explained_variance_ratio_)  #(pca.explained_variance_/np.sum(pca.explained_variance_)) eigen values 

# %%
print(pca.components_)  ## EIGEN VECTORS
##now look for the max value vertically and we can infer that which one is more significant 

# %%
#print(pca.explained_variance_) used to see individual variance
B= pca.transform(df)   ##vector projections   ## apply lda and annn on this B
B       

# %%
##Assignment PCA 
df = pd.read_csv("Iris.csv")
df

# %%
C=df.drop(["Species","Id"],axis=1)
C

# %%
M = np.mean(C,axis=0)
c=C-M
c

# %%
Sw = np.cov(c.T)   ## cov goes in neural network therefore go for transform 
Sw

# %%
eigval,eigvec=np.linalg.eig(Sw)
idx=eigval.argsort()[::-1]
val=eigval[idx]
eigvec=eigvec[:,idx]
eig1=eigvec[:,:1]
eig2=eigvec[:,:1]
eig3=eigvec[:,:1]
eig4=eigvec[:,:1]
eig1,eig2,eig3,eig4

# %%
val , eig1

# %%
z1 =pd.DataFrame(np.dot(c,eig1))   # length 
z2 =pd.DataFrame(np.dot(c,eig2))

# %%
z1

# %%
x = np.sum(val)
x

# %%
per1 = val[0]/x*100
per2 = val[1]/x*100


# %%
## Libraries
from sklearn import preprocessing
Y_1 = df.iloc[:,-1]
le = preprocessing.LabelEncoder()
Y_1=le.fit_transform(Y_1).reshape(-1,1)

# %%
x = pd.concat([z1,z2],axis=1)


# %%
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler, LabelEncoder

# %%

lda = LDA(n_components=1)     ## N-1 , AND BY DEFAULT IT WILL BE 1 
k = lda.fit(x,Y_1)
X_lda = lda.transform(x)
predict = lda.predict(x)

# %%
from sklearn.metrics import confusion_matrix  
from sklearn.metrics import accuracy_score

cm = confusion_matrix(Y_1, predict)  
print(cm)  
print('Accuracy' + str(accuracy_score(Y_1, predict))) 

# %%
##PCA BY LIBRARIES
from sklearn.decomposition import PCA
pca=PCA()   ## write the number of dimnesion we need , or all in default
pca.fit(c)   ## fit the data
print(pca.explained_variance_ratio_)  ## eigen values


# %%
## now we see that only 1St eigen value captures 0.92 variance , but we connsider 1 and 2 for mor variance

# %%
pca=PCA(2)   ## write the number of dimnesion we need , or all in default
pca.fit(c)   ## fit the data
print(pca.explained_variance_ratio_) 

# %%
print(pca.components_.T)  ## EIGEN VECTORS
##INFERENCE - petal length has the most variance in z1 , sepal length and sepal width in z2

# %%
B= pca.transform(c)   ## vector projections
B

# %%
## USE THIS b MATRIX FOR LDA AND NN FURTHER 

# %% [markdown]
# # Case Study Bankloan 

# %%
df = pd.read_excel("Bankloan_casestudy.xlsx")
df

# %%
df = df.dropna(axis=0)
df

# %%
## neural network
x = df.iloc[:,0:8]
y = df.iloc[:,-1]

# %%
X = np.asarray(x)
Y= np.asarray(y)

# %%
x.shape

# %%
y.shape

# %%
from tensorflow.keras.layers import Dense 
from tensorflow.keras.models import Sequential 
model = Sequential()
model.add(Dense(128,activation='relu',input_shape=(8,)))
model.add(Dense(64,activation='relu'))
model.add(Dense(1,activation='sigmoid')) 

# %%
model.summary()

# %%
model.compile(loss='binary_crossentropy',optimizer = 'adam',metrics=['accuracy'])

# %%
model.fit(X,Y,epochs =100,batch_size=10)
## stochastic gradient , all together 
## batch gradient , uses output of one as the initialization of the second

# %%

##LDA thriugh sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler, LabelEncoder
lda = LDA(n_components=1)     ## N-1 , AND BY DEFAULT IT WILL BE 1 
k = lda.fit(x,y)
X_lda = lda.transform(x)
predict = lda.predict(x)

# %%
from sklearn.metrics import confusion_matrix  
from sklearn.metrics import accuracy_score

cm = confusion_matrix(y, predict)  
print(cm)  
print('Accuracy' + str(accuracy_score(y, predict))) 

# %%
##PCA 
##PCA BY LIBRARIES

import numpy as np
from sklearn.decomposition import PCA
pca=PCA()   ## write the number of dimnesion we need , or all in default
pca.fit(X)   ## fit t 3.29263674e-02 1.66375415e-02
 1.15684339e-02 1.72533662e-03 1.06062933e-03 4.30841031e-04]
## take first two he data
print(pca.explained_variance_ratio_)


# %%
## take first two 
pca=PCA(2)   ## write the number of dimnesion we need , or all in default
pca.fit(X)   ## fit the data
print(pca.explained_variance_ratio_)



# %%
print(pca.components_.T)
##z1 has emply and income , z2 has sales and many more 

# %%
B= pca.transform(X)   ## vector projections
B

# %%
## Z1 WE HAVE EDUCATION AND INCOME AS HIGHEST   
new_df= pd.DataFrame(B)

# %%
new_df

# %%
new_df = np.asarray(new_df)

# %%
## again neural network
model = Sequential()
model.add(Dense(128,activation='relu',input_shape=(2,)))
model.add(Dense(64,activation='relu'))
model.add(Dense(1,activation='sigmoid'))   ##binary cross entropy ,if linear write linear



# %%
model.summary()

# %%
model.compile(loss='binary_crossentropy',optimizer = 'adam',metrics=['accuracy'])

# %%
model.fit(new_df,Y,epochs =100,batch_size=10)

# %%
##LDA thriugh sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler, LabelEncoder
lda = LDA(n_components=1)     ## N-1 , AND BY DEFAULT IT WILL BE 1 
k = lda.fit(new_df,y)
X_lda = lda.transform(new_df)
predict = lda.predict(new_df)

# %%
from sklearn.metrics import confusion_matrix  
from sklearn.metrics import accuracy_score

cm = confusion_matrix(y, predict)  
print(cm)  
print('Accuracy' + str(accuracy_score(y, predict))) 

# %% [markdown]
# # Case Study PCA

# %%
df = pd.read_excel("PCA_case study.xlsx")
df

# %%
df = df.drop(['Manufacture','Model'],axis = 1)

# %%
df

# %%
df =df.dropna(axis=0)

# %%
y = df['Type']
x = df.drop(['Type'],axis=1)

# %%
X = np.asarray(x)
Y= np.asarray(y)

# %%
x.shape

# %%
model = Sequential()
model.add(Dense(128,activation='relu',input_shape=(12,)))
model.add(Dense(64,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

# %%
model.compile(loss='binary_crossentropy',optimizer = 'adam',metrics=['accuracy'])

# %%
model.fit(X,Y,epochs =1000)


# %%
##LDA thriugh sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler, LabelEncoder
sc = StandardScaler()
x =sc.fit_transform(X)
lda = LDA(n_components=1)     ## N-1 , AND BY DEFAULT IT WILL BE 1 
k = lda.fit(x,Y)
X_lda = lda.transform(x)
predict = lda.predict(x)

# %%
from sklearn.metrics import confusion_matrix  
from sklearn.metrics import accuracy_score

cm = confusion_matrix(y, predict)  
print(cm)  
print('Accuracy' + str(accuracy_score(y, predict))) 

# %%
##PCA 
##PCA BY LIBRARIES

import numpy as np
from sklearn.decomposition import PCA
pca=PCA()   ## write the number of dimnesion we need , or all in default
pca.fit(x)   ## fit the data
print(pca.explained_variance_ratio_)
## take first 4 

# %%
pca=PCA(4)   ## write the number of dimnesion we need , or all in default
pca.fit(x)   ## fit the data
print(pca.explained_variance_ratio_)

# %%
print(pca.components_.T)  ## EIGEN VECTORS    ## Z1 CURB WEIGHT AND PRICE

# %%
B= pca.transform(x)   ## vector projections
B

# %%
new_df = pd.DataFrame(B)

# %%
new_df

# %%


# %%
##LDA thriugh sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler, LabelEncoder
sc = StandardScaler()
x =sc.fit_transform(new_df)
lda = LDA(n_components=1)     ## N-1 , AND BY DEFAULT IT WILL BE 1 
k = lda.fit(x,Y)
X_lda = lda.transform(x)
predict = lda.predict(x)

# %%
from sklearn.metrics import confusion_matrix  
from sklearn.metrics import accuracy_score

cm = confusion_matrix(y, predict)  
print(cm)  
print('Accuracy' + str(accuracy_score(y, predict))) 

# %% [markdown]
# # PCA on Image

# %%
from sklearn import datasets 
faces = datasets.fetch_olivetti_faces()
faces.data.shape   #(number of images , pixel)

# %%
##single image shape  (2nd image )
k=faces.images[1]
k.shape

# %%
##Plot the images
from matplotlib import pyplot as plt 
plt.imshow(k,cmap=plt.cm.bone)

# %%
fig=plt.figure(figsize=(8,6))
for i in range (15):
    ax=fig.add_subplot(3,5,i+1,xticks=[],yticks=[])
    ax.imshow(faces.images[i],cmap=plt.cm.bone)

# %%
##Pca 
from sklearn.decomposition import PCA   ## by default (400,4096) instead of (4096,4096) , we get 400 principal components 
pca = PCA()
pca.fit(faces.data) 


# %%
##average 
plt.imshow(pca.mean_.reshape(faces.images[0].shape),cmap=plt.cm.bone)   ## most common part 

# %%
import numpy as np 
print(pca.explained_variance_)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.show()    
## we infered that only 90% components are important 

# %%
print(pca.components_.shape) ##vector v print(pca.components_.shape) ##vector v 

# %%
##but still we will see first with 400 components 

##plot the first eigen face ## only looking at the first component 
plt.imshow(pca.components_[0].reshape(faces.images[0].shape),cmap=plt.cm.bone)

# %%
##last component
plt.imshow(pca.components_[399].reshape(faces.images[0].shape),cmap=plt.cm.bone)

# %%
##plot first 10 eigen face
fig=plt.figure(figsize=(320,100))
for i in range (10):
    ax=fig.add_subplot(3,100,i+1,xticks=[],yticks=[])
    ax.imshow(pca.components_[i].reshape(faces.images[0].shape),cmap=plt.cm.bone)

# %%
##eigen space ##omega 
face_pca=pca.fit_transform(faces.data)
print(face_pca.shape)

# %%
## projected face considering 400 components   ## mmult(v,x)
faces_proj = pca.inverse_transform(face_pca)
print(faces_proj.shape)


# %%
##Projected face
plt.imshow(faces_proj[0].reshape(faces.images[0].shape),cmap=plt.cm.bone)

# %%
##REal face
plt.imshow(faces.images[0] , cmap=plt.cm.bone)

# %%
## now we know that we have 90% components that will give us the face 
## only looking for PCA(0.9), similarly go on 

# %%
from sklearn.decomposition import PCA   ## by default (400,4096) instead of (4096,4096) , we get 400 principal components 
pca = PCA(0.90)
pca.fit(faces.data) 

# %%
import numpy as np 
print(pca.explained_variance_)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.show()  

# %%
print(pca.components_.shape) ##vector v 

# %%


# %%
##plot the first eigen face ## only looking at the first component 
plt.imshow(pca.components_[0].reshape(faces.images[0].shape),cmap=plt.cm.bone)

# %%
##65th component
plt.imshow(pca.components_[65].reshape(faces.images[0].shape),cmap=plt.cm.bone)

# %%
##plot first 10 eigen face
fig=plt.figure(figsize=(320,100))
for i in range (10):
    ax=fig.add_subplot(3,66,i+1,xticks=[],yticks=[])
    ax.imshow(pca.components_[i].reshape(faces.images[0].shape),cmap=plt.cm.bone)

# %%
##eigen space ##omega 
face_pca=pca.fit_transform(faces.data)
print(face_pca.shape)

# %%
## projected face considering 400 components   ## mmult(v,x)
faces_proj = pca.inverse_transform(face_pca)
print(faces_proj.shape)

# %%
plt.imshow(faces_proj[0].reshape(faces.images[0].shape),cmap=plt.cm.bone)

# %% [markdown]
# # PCA Assignment 

# %%
import cv2
import numpy as np
from matplotlib import pyplot as plt 
from numpy import asarray
from PIL import Image
import os
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense ##dense for ann , con for cnn
import pickle


# %%
img = 'C:/Users/rodea/OneDrive/Desktop/FOML/PCA_IMAGES'
def get_image_array(path):
    image_list=os.listdir(path)
    images=[]
    for img in image_list:
        img=cv2.imread(path+ '/' + img,0)
        images.append(img)
    return np.array(images)

# %%
img=get_image_array(img) 
img.shape

# %%
k = img[0]
from matplotlib import pyplot as plt 
plt.imshow(k,cmap=plt.cm.bone)

# %%


# %%
img1 = img.reshape((400,400*200))
img1 = img1/255

# %%
fig=plt.figure(figsize=(8,6))
for i in range (15):
    ax=fig.add_subplot(3,5,i+1,xticks=[],yticks=[])
    ax.imshow(img[i],cmap=plt.cm.bone)

# %%
from sklearn.decomposition import PCA    
pca = PCA()
pca.fit(img1) 


# %%
##We want 0.95% variance to be captured 
import numpy as np 
print(pca.explained_variance_)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.show()   


# %%
pca = PCA(0.95)
pca.fit(img1) 


# %%
plt.imshow(pca.mean_.reshape(img[0].shape),cmap=plt.cm.bone)   ## most common part 

# %%
print(pca.components_.shape) ##vector v 

# %%
##plot the first eigen face ## only looking at the first component 
plt.imshow(pca.components_[0].reshape(img[0].shape),cmap=plt.cm.bone)

# %%
plt.imshow(pca.components_[11].reshape(img[0].shape),cmap=plt.cm.bone)

# %%
##plot first 10 eigen face
fig=plt.figure(figsize=(320,100))
for i in range (11):
    ax=fig.add_subplot(3,100,i+1,xticks=[],yticks=[])
    ax.imshow(pca.components_[i].reshape(img[0].shape),cmap=plt.cm.bone)

# %%
##eigen space ##omega 
face_pca=pca.fit_transform(img1)
print(face_pca.shape)

# %%
## projected face considering 400 components   ## mmult(v,x)
faces_proj = pca.inverse_transform(face_pca)
print(faces_proj.shape)

# %%
##projected
plt.imshow(faces_proj[0].reshape(img[0].shape))

# %%
##orignal
from matplotlib import pyplot as plt 
plt.imshow(img[0])

# %% [markdown]
# # SVD(Single Value Decomposition)

# %%
A = np.array([
[1,2,3,4,5,6,7,8,9,10],
[11,12,13,14,15,16,17,18,19,20],
[21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
])

# %%
# Perform Singular Value Decomposition
from numpy.linalg import svd
U, S, VT = svd(A)

# %%
# U, S, VT are the matrices such that A = U * np.diag(S) * VT

# U is the left singular vectors matrix
print("U matrix:")
print(U)
print()

# S is the singular values array
print("Singular values:")
print(S)
print()

# VT is the right singular vectors matrix (transposed)
print("VT matrix:")
print(VT)
print()

# %%
##stretch matrix
stretch_matrix = np.diag(S)
print("Stretch Matrix:")
print(stretch_matrix)


# %%
##Rotationn matrix
rotation_matrix_U = U
rotation_matrix_VT = VT.T  # Transpose VT to get the rotation matrix
print("Rotation Matrix U:")
print(rotation_matrix_U)
print()
print("Rotation Matrix VT:")
print(rotation_matrix_VT)

# %% [markdown]
# # SVM(Support Vector Machine)

# %%
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# %%
#data
np.random.seed(1)
X = np.random.randn(200,2)
Y = np.repeat([[1, -1]], 100)
X[Y == -1] = X[Y == -1]*-1

# %%
# SVM training
clf = SVC()
clf.fit(X, Y)

# %%
# Test data generation and manipulation
np.random.seed(1)
X_test = np.random.randn(20,2)
y_test = np.random.choice([-1,1], 20)
X_test[y_test == 1] = X_test[y_test == 1] * -1

# %%
# Testing SVM
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# %%
print(f'Accuracy of the SVM on the test set: {accuracy}')

# %%


# %%
##Question 
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
# Features for each account (Current Ratio, Return on Investment)
X = np.array([
# Good accounts
[1.1, 13], [1.5, 15], [1.2, 17], [0.9, 21],
[1.6, 7], [2.2, 8], [0.9, 16],
# Bad accounts
[0.7, 11], [0.9, 4], [0.8, 6], [1.3, 2],
[1.1, 6], [0.5, 8], [0.3, 8]
])
# Labels (1 for Good Accounts, 0 for Bad Accounts)
y = np.array([1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0])

# %%
# Scale the data
scaler = StandardScaler()
X = scaler.fit_transform(X)


# %%
# Create and train the SVM model
clf = SVC()
clf.fit(X, y)

# %%
# Find out the support vectors
support_vectors = clf.support_vectors_
print(support_vectors)

# %%



""")
 return

def gentlebrute():
    print("""# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
import kagglehub

# %%
import matplotlib.pyplot as plt
import pandas as pd

# Define exam data
exam_data = {
    "Subject": ["ATSA", "AAI", "FOML", "IMAP", "VCC", "RES", "TIM"],
    "Exam Date": ["2024-11-25", "2024-11-27", "2024-11-29", "2024-12-05", "2024-12-09", "2024-12-10", "2024-12-11"],
}

# Convert to DataFrame and calculate days for each subject
exams = pd.DataFrame(exam_data)
exams["Exam Date"] = pd.to_datetime(exams["Exam Date"])
exams["Days to Study"] = (exams["Exam Date"].diff().fillna(pd.Timedelta(days=1))).dt.days

# Prepare for visualization
dates = exams["Exam Date"].dt.strftime('%b %d')
subjects = exams["Subject"]
study_days = exams["Days to Study"]

# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(subjects, study_days, color='skyblue', edgecolor='black')

# Add labels and title
ax.set_title("Days to study each subject", fontsize=14, weight='bold')
ax.set_ylabel("Days to Study", fontsize=12)
ax.set_xlabel("Subjects", fontsize=12)
ax.bar_label(bars, labels=study_days, padding=3, fontsize=10)
ax.set_xticks(range(len(subjects)))
ax.set_xticklabels(subjects, fontsize=10)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# %% [markdown]
# # Numpy

# %% [markdown]
# ### Gradient Descent

# %%
theta0=0.35
theta1=1-theta0-0.2
theta2=0.2
np.random.seed(69)
x1=np.random.randn(100,1)
x2=np.random.randn(100,1)
y=np.random.randn(100,1)

# %%
costs=[]
epochs=10000
m=len(x1)
lr=0.1


for i in range(epochs):
    h=theta0+theta1*x1+theta2*x2
    cost=(1/m)*(np.sum((h-y)**2))
    costs.append(cost)
    
    dtheta0=(1/m)*(h-y)
    dtheta1=(1/m)*(h-y)*x1
    dtheta2=(1/m)*(h-y)*x2
    
    theta0=theta0-lr*dtheta0
    theta1=theta1-lr*dtheta1
    theta2=theta2-lr*dtheta2
plt.plot(costs)

# %%


# %% [markdown]
# ### Activation Functions

# %% [markdown]
# **Sigmoid Activation Function:**
# σ(x) = 1 / (1 + exp(-x))
# 
# **Gradient of Sigmoid:**
# σ'(x) = x * (1 - x)

# %%
def sigmoid(x):
    return 1/1+ np.exp(-x)

def sigmoid_prime(x):
    return x * (1 - x)

# %% [markdown]
# **ReLU Activation Function:**
# ReLU(x) = x if x > 0, else 0
# 
# **Gradient of ReLU:**
# ReLU'(x) = 1 if x > 0, else 0
# 

# %%
def relu(x):
    return np.maximum(x, 0)

def relu_prime(x):
    return np.where(x > 0, 1, 0)

# %% [markdown]
# **Leaky ReLU Activation Function:**
# LReLU(x) = x if x > 0, else α * x
# 
# **Gradient of Leaky ReLU:**
# LReLU'(x) = 1 if x > 0, else α
# 

# %%
def lrelu(x):
    np.maximum(0.01,x)
    
def lrelu_prime(x):
    return np.where(x>0,1,0.01)

# %% [markdown]
# **Tanh Activation Function:**
# tanh(x) = (exp(x) - exp(-x)) / (exp(x) + exp(-x))
# 
# **Gradient of Tanh:**
# tanh'(x) = 1 - x^2
# 

# %%
def tanh(x):
    return (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))

# %% [markdown]
# ### Forward Propagation

# %%
from sklearn.datasets import load_breast_cancer
import pandas as pd

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)  
y = pd.Series(data.target)
X['Target']=y
df=X.copy

# %%
df.head()

# %%
x=X.values.T
y=np.array(df['Target'].values).reshape(1,-1)
x.shape,y.shape

# %%
# 6 layers of a neural network with tanh, sigmoid, relu, relu, leaky relu and sigmoid
layers=[2,4,8,16,32,64]
layers.sort(reverse=True)
layers

# %%
b1=np.random.randn(layers[0],1) * 0.01
b2=np.random.randn(layers[0],1) * 0.01
b3=np.random.randn(layers[0],1) * 0.01
b4=np.random.randn(layers[0],1) * 0.01
b5=np.random.randn(layers[0],1) * 0.01
b5=np.random.randn(layers[0],1) * 0.01

W1=np.random.randn(layers[0],x.shape[0]) * 0.01
W2=np.random.randn(layers[1],layers[1]) * 0.01
W3=np.random.randn(layers[2],layers[2]) * 0.01
W4=np.random.randn(layers[3],layers[3]) * 0.01
W5=np.random.randn(layers[4],layers[4]) * 0.01
W6=np.random.randn(y.shape[0],layers[5]) * 0.01

# %%
Z1= np.dot(W1,x)+b1
A1=tanh(Z1)
print(Z1.shape, A1.shape)
Z2=np.dot(W2,A1)+b2
A2=sigmoid(Z2)

Z1= np.dot(W1,x)+b1
A1=tanh(Z1)

Z2=np.dot(W2,A1)+b2
A2=sigmoid(Z2)

Z1= np.dot(W1,x)+b1
A1=tanh(Z1)

Z2=np.dot(W2,A1)+b2
A2=sigmoid(Z2)
Z1= np.dot(W1,x)+b1
A1=tanh(Z1)

Z2=np.dot(W2,A1)+b2
A2=sigmoid(Z2)


# %% [markdown]
# ### Backward Propagation

# %% [markdown]
# ### PCA

# %% [markdown]
# ### LDA

# %% [markdown]
# ### KNN

# %%
np.random.seed(42)

class_size = 100

class_0_param1 = np.random.normal(5, 1, class_size)  
class_0_param2 = np.random.normal(3, 0.5, class_size)
class_0_y = [0] * class_size

class_1_param1 = np.random.normal(8, 1, class_size)  
class_1_param2 = np.random.normal(6, 0.5, class_size)
class_1_y = [1] * class_size

data = {
    'Parameter1': np.concatenate([class_0_param1, class_1_param1]),
    'Parameter2': np.concatenate([class_0_param2, class_1_param2]),
    'y': np.concatenate([class_0_y, class_1_y])
}

df = pd.DataFrame(data)

df.head()

# %%
plt.scatter(df['Parameter1'],df['Parameter2'],c=df['y'],alpha=1,cmap='PiYG')
plt.scatter(7,4.75, color='red', marker='X', s=100)

# %%
point=(4,3)
lists=[]
for i in range(len(df)):
    distance=np.sqrt((point[0]-df.iloc[i][0])**2+(point[1]-df.iloc[i][1])**2)
    lists.append(distance)
    
df['Distance']=lists

# %%
final=df.sort_values(by='Distance',ascending=True).head(10)
final['y'].value_counts()

# %% [markdown]
# # Sci-Kit Learn

# %%
x=load_wine().data
y=load_wine().target
Xtrain,Xtest, Ytrain,Ytest = train_test_split(x,y,test_size=0.2)
Xtrain.shape,Xtest.shape,Ytrain.shape,Ytest.shape

# %% [markdown]
# ## PCA

# %% [markdown]
# ### PCA 

# %%
pca=PCA(0.9)
Xtrain=pca.fit_transform(Xtrain)
Xtest=pca.transform(Xtest)
Xtrain.shape, Xtest.shape

# %% [markdown]
# ### PCA with NN

# %%
# pca=PCA(0.9)
# Xtrain=pca.fit_transform(Xtrain)
# Xtest=pca.transform(Xtest)
# Xtrain.shape, Xtest.shape

# %%
model=Sequential()
model.add(Dense(64, input_shape=(1,), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(3, activation='softmax'))
model.summary()

# %%
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# %%
model.fit(Xtrain,Ytrain,epochs=100,batch_size=100)

# %%
model.evaluate(Xtest,Ytest)

# %% [markdown]
# ## LDA

# %% [markdown]
# ### LDA

# %%
lda=LDA()
lda.fit(Xtrain,Ytrain)
Ypred=lda.predict(Xtest)
accuracy_score(Ypred,Ytest)

# %% [markdown]
# ### LDA with PCA

# %%
pca=PCA(0.9)
Xtrain=pca.fit_transform(Xtrain)
Xtest=pca.transform(Xtest)

# %%
lda=LDA()
lda.fit(Xtrain,Ytrain)
Ypred=lda.predict(Xtest)
accuracy_score(Ypred,Ytest)

# %% [markdown]
# ## SVM

# %%
svm=SVC()
svm.fit(Xtrain,Ytrain)
accuracy_score(svm.predict(Xtest),Ytest)

# %% [markdown]
# ## Neural Network

# %% [markdown]
# ### With Early Stopping and custom learning rate

# %%
es=EarlyStopping(min_delta=0.0000001, patience=3, monitor='accuracy')
adam=Adam(learning_rate=0.001)

# %%
model=Sequential()
model.add(Dense(64,input_shape=(13,), activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(16,activation='relu'))
model.add(Dense(8,activation='relu'))
model.add(Dense(3,activation='softmax'))
model.summary()

# %%
model.compile(optimizer=adam,loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# %%
model.fit(Xtrain,Ytrain,epochs=100,batch_size=32,callbacks=[es])

# %%
model.evaluate(Xtest,Ytest)

# %% [markdown]
# ### Train Generator

# %%
path = kagglehub.dataset_download("grassknoted/asl-alphabet")

print("Path to dataset files:", path)

# %%
train_dir=path+'/asl_alphabet_train/asl_alphabet_train'
test_dir=path+'/asl_alphabet_test/asl_alphabet_test'

# %%
IMAGE_SIZE = (150, 150)  
BATCH_SIZE = 32

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    width_shift_range=0.2,
    height_shift_range=0.2,  
    shear_range=0.2,  
    zoom_range=0.2,  
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'  
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

print("Class Indices:", train_generator.class_indices)

for images, labels in train_generator:
    print("Image batch shape:", images.shape)
    print("Label batch shape:", labels.shape)
    break

# %%
model=Sequential()
model.add(Dense(8192,input_shape=(150,150,3),activation='relu'))
model.add(Dense(2048,activation='relu'))
model.add(Dense(1024,activation='relu'))
model.add(Dense(512,activation='relu'))
model.add(Dense(256,activation='relu'))
model.add(Dense(128,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(29,activation='softmax'))
model.summary()

# %%
model.compile(optimizer=adam,loss='sparse_categorical_crossentropy',metrics=['accuracy'])

# %%
# Train the model
history = model.fit(
    train_generator,
    epochs=100,
    batch_size=12800,
    validation_data=test_generator
)

# %% [markdown]
# ## KNN

# %%
wine = load_wine()
X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# %%
knn_sklearn = KNeighborsClassifier(n_neighbors=5)
knn_sklearn.fit(X_train, y_train)
y_pred_sklearn = knn_sklearn.predict(X_test)

accuracy_score(y_test, y_pred_sklearn)



""")