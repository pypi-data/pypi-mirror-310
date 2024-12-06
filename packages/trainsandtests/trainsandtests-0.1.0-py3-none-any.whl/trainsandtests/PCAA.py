def library():
    print("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from sklearn.neighbors import KNeighborsClassifier""")
    return

def Activation_Functions():
    print("""def sigmoid(z):
    return 1/(1+(np.exp(-z)))

def sigmoid_prime(z):
    return z*(1-z)

def relu(z):
    return np.maximum(z, 0)

def relu_prime(z):
    return np.where(z > 0, 1, 0)

def tanh(z):
    num=np.exp(z)-np.exp(-z)
    den=np.exp(z)+np.exp(-z)
    return num/den

def tanh_prime(z):
    return 1 - z**2

def lrelu(z):
    return np.maximum(z,0.01)

def lrelu_prime(z):
    return np.where(z>0,1,0.01)""")
    return

def ANN():
    print("""def ANN(x,y,nodes):
    nx,m=x.shape
    ny,_=y.shape
    
    #FWD
    w1=np.random.rand(nodes[0],nx)
    b1=np.random.rand(nodes[0],1)
    
    w2= np.random.rand(nodes[1],nodes[0])
    b2=np.random.rand(nodes[1],1)
    
    w3= np.random.rand(ny,nodes[1])
    b3=np.random.rand(ny,1)
    
    epochs=100
    lr=0.01
    cost_hist=[]
    for i in range(epochs):
        z1=np.dot(w1,x)+b1
        a1=relu(z1)
        
        z2=np.dot(w2,a1)+b2
        a2=sigmoid(z2)
        
        z3=np.dot(w3,a2)+b3
        a3=relu(z3)
        
        error=a3-y
        cost=np.sum(np.dot(error,error.T))/(2*m)
        cost_hist.append(cost)
        
        dz3=error
        dw3=np.dot(dz3,a2.T)/m
        db3=np.sum(dw3,axis=1,keepdims=True)/m
        da3=np.dot(w3.T,dz3)
        
        dz2=sigmoid_prime(a2)*da3
        dw2=np.dot(dz2,a1.T)/m
        db2=np.sum(dw2,axis=1,keepdims=True)/m
        da2=np.dot(w2.T,dz2)
        
        dz1=relu_prime(a1)*da2
        dw1=np.dot(dz1,x.T)/m
        db1=np.sum(dw1,axis=1,keepdims=True)/m
        da1=np.dot(w1.T,dz1)
        
        #BWP
        w3-=lr*dw3
        b3-=lr*db3
        w2-=lr*dw2
        b2-=lr*db2
        w1-=lr*dw1
        b1-=lr*db1
        
    plt.plot(cost_hist)
# Don't add the nodes in the output layer
ANN(x, y, nodes=[64,32])""")
    return

def PCA_numpy():
    print("""A = np.random.rand(100,3)
A, A.shape

A_mean=A.mean(axis=0)
A_std=A-A_mean
A_cov=np.cov(A)

eigvals,eigvecs=np.linalg.eig(A_cov)  #eigvals are magnitudes and eigvecs are vectors 
idx = np.argsort(eigvals)[::-1]  # gives the result of the sorted matrix indexes in a decreasing order
eigvals = eigvals[idx] # sort out the vals and vecs on the basis of variability
eigvecs = eigvecs[:, idx]

# First 5 principle components
eig1=eigvecs[:,:1]
eig2=eigvecs[:,1:2]
eig3=eigvecs[:,2:]

z1=np.dot(A_cov,eig1)
z2=np.dot(A_cov,eig2)
z3=np.dot(A_cov,eig3)
# To calculate the explained_var_ratio. Calculate the var of all, sum and each/sum is the ratio 

pca1=np.dot(z1,eig1.T)
pca2=np.dot(z2,eig2.T)
pca3=np.dot(z3,eig3.T)


plt.plot(pca1[:, 0], pca1[:, 1], label='Reconstructed data from 1st PC')
plt.plot(pca2[:, 0], pca2[:, 1], label='Reconstructed data from 2nd PC')
# plt.plot([0, 0], [-1.5, 1.5], color='gray', ls='--')
# plt.plot([-1.5, 1.5], [0, 0], color='gray', ls='--')
plt.legend()
plt.show()""")
    return

def LDA_numpy():
    print("""df_1 = df[df['Group'] == 1]
df_2 = df[df['Group'] == 2]

df_1.shape, df_2.shape

# naming is as per the groups made
# mu{group, df}
mu11 = np.mean(df_1['X1'])
mu21 = np.mean(df_1['X2'])
mu12 = np.mean(df_2['X1'])
mu22 = np.mean(df_2['X2'])

#SB=mu^2
mu = np.array([mu11-mu12, mu21-mu22]).reshape(1, 2)
SB = np.dot(mu.T, mu)
SB

# Standardizing values
df_1['x1'] = df_1['X1'] - mu11
df_1['x2'] = df_1['X2'] - mu21

df_2['x1'] = df_2['X1'] - mu12
df_2['x2'] = df_2['X2'] - mu22

df_1.head(), df_2.head()
x12 = df_1[['x1', 'x2']].values
x22 = df_2[['x1', 'x2']].values
n=len(x12)

# Variance Formula = (x-mu).T * (x-mu) / n, where n is the number of samples
SW = (np.dot(x12.T, x12) + np.dot(x22.T, x22))/n
SW

A = np.dot(np.linalg.inv(SW), SB)
A

eigenvalues, eigenvectors = np.linalg.eig(A)
idx = eigenvalues.argsort()[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

eigenvalues, eigenvectors
eig = eigenvectors[:, :1]

k = df_1.iloc[:, 0:2]
length_c1 = np.dot(k, eig)
l = df_2.iloc[:, 0:2]
length_c2 = np.dot(l, eig)
k.shape

proj_1 = length_c1*eig.T
proj_2 = length_c2*eig.T
ps = np.concatenate([proj_1, proj_2], axis=0)

plt.scatter(ps[:, 0], ps[:, 1], c=df['Group'], cmap=plt.cm.Paired)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data')
plt.show()
x1 = df['X1'].mean()
x2 = df['X2'].mean()

mean_vector = np.array([x1, x2])
mean_vector.shape

# projection of the mean of the data to find the threshold
# multiplying the mean vector with the eigenvector
length_mean = np.dot(mean_vector, eig)
length_mean

proj_mean = np.dot(length_mean, eig.T)
proj_mean

# plotting the data
plt.scatter(ps[:, 0], ps[:, 1], c=df['Group'], cmap=plt.cm.Paired)
plt.scatter(proj_mean[0], proj_mean[1], c='r', marker='x')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data')
plt.show()""")
    return

def PCA_sklearn():
    print("""pca=PCA(0.9)
Xtrain=pca.fit_transform(Xtrain)
Xtest=pca.transform(Xtest)
Xtrain.shape, Xtest.shape""")
    return

def LDA_sklearn():
    print("""lda=LDA()
lda.fit(Xtrain,Ytrain)
Ypred=lda.predict(Xtest)
accuracy_score(Ypred,Ytest)""")
    return

def SVM():
    print("""svm=SVC()
svm.fit(Xtrain,Ytrain)
accuracy_score(svm.predict(Xtest),Ytest)""")    
    return

def NN_sklearn():
    print("""es=EarlyStopping(min_delta=, patience=3, monitor='accuracy')
adam=Adam(learning_rate=0.001)

model=Sequential()
model.add(Dense(64,input_shape=(13,), activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(16,activation='relu'))
model.add(Dense(8,activation='relu'))
model.add(Dense(3,activation='softmax'))
model.summary()

model.compile(optimizer=adam,loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(Xtrain,Ytrain,epochs=100,batch_size=32,callbacks=[es])""")
    return

def KNN_sklearn():
    print("""knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred_sklearn = knn.predict(X_test)

accuracy_score(y_test, y_pred_sklearn)""")
    return