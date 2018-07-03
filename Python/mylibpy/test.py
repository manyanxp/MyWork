import numpy as np
import matplotlib.pyplot as plt

def scmatrix(X,Y,Z):#散布図行列
    n=np.shape(X)
    L=np.zeros(n[0])#ラベルの処理　色々
    k,p=0,False
    for i in range(0,n[0]):
        if p==True:
            k=k+1
        p=False
        for j in range(0,n[0]):
            if Y[i]==Y[j] and L[j]==0:
                L[j]=k
                p=True
    plt.figure(figsize=(10,8))#プロット開始
    k=0
    L=(L-L.min())/(L.max()-L.min())#規格化
    for j in range(0,n[1]):
       for i in range(0,n[1]):
           k=k+1
           plt.subplot(n[1],n[1],k)
           plt.scatter(X[:,i],X[:,j],s=5,alpha=0.7,
                            cmap=plt.cm.rainbow,c=L)
           if j==n[1]-1:plt.xlabel(Z[i])
           if i==0 :plt.ylabel(Z[j])
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    return

if __name__ == '__main__':
    dat=np.genfromtxt('iris.csv',delimiter=',',dtype=str)#まずは全部読み出し
    X=np.copy(dat[1:,1:5])#数値データ行列を抜き出し
    X=np.asfarray(X)#型変換str→float64
    Y=np.copy(dat[1:,5])#ラベルの抜き出し
    Z=np.copy(dat[0,1:])

    scmatrix(X,Y,Z)

    plt.show()