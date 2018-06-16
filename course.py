# import math
# import numpy as np
# from scipy.stats import f
# class MLR(object):
#     def __init__(self,X,Y):
#         self.X=X
#         self.Y=Y
#     def main(self):
#         xt=self.X.T
#         xtx=xt.dot(self.X)
#         xtxinv=np.linalg.inv(xtx)
#         temp=xtxinv.dot(xt)
#         self.A=np.dot(temp,self.Y)
#     def getCoef(self):
#         return self.A
#     def predict(self,X):
#         return X.dot(self.A)
#     def Ftest(self,alpha):
#         n=len(self.X)
#         X=self.X[:,1:]
#         if len(X.shape)==1:
#             k=1
#         else:
#             k=X.shape[1]
#         f_arfa=f.isf(alpha,k,n-k-1)
#         Yaver=self.Y.sum()/n
#         Yhat=self.predict(self.X)
#         U=sum(((self.Y-Yaver)**2))
#         Qe=sum((self.Y-Yhat)**2)
#         F=(U/k)/(Qe/(n-k-1))
#         return [F,f_arfa,F>f_arfa]
#     def rCoef(self):
#         n=len(self.X)
#         Yaver=self.Y.sum()/n
#         Yhat=self.predict(self.X)
#         U = ((self.Y - Yaver) ** 2).sum()
#         Qe = ((self.Y - Yhat) ** 2).sum()
#         r = math.sqrt(U / (U + Qe))
#         return r
#
#
# class PCA:
#     def __init__(self, X):
#         self.X=X
#     def SVDdecompose(self):
#         B = np.linalg.svd(self.X,full_matrices=False)
#         U=B[0]
#         lamda=B[1]
#         self.P = B[2].T
#         i=len(lamda)
#         S=np.zeros ((i,i))
#         S[:i,:i]=np.diag (lamda)
#         self.T = np.dot (U,S)
#         compare = []
#         for i in range(len(lamda) - 1):
#             temp = lamda[i] / lamda[i + 1]
#             compare.append(temp)
#         return np.array(compare)
#
#     def PCAdecompose(self, k):
#         T = self.T[:,:k]
#         P = self.P[:,:k]
#         return T,P
#
#
# class PCR(object):
#     def __init__(self, X, Y):
#         self.X = X
#         self.Y = Y
#
#     def confirmPCs(self):
#         self.pca = PCA(self.X)
#         compare = self.pca.SVDdecompose()
#         return compare
#
#     def model(self, PCs):
#         T, P = self.pca.PCAdecompose(PCs)
#         self.P = P
#         oneCol = np.ones(T.shape[0])
#         T = np.c_[oneCol, T]
#         self.mlr = MLR(T, self.Y)
#         self.mlr.main()
#         self.A = self.mlr.getCoef()
#
#     def predict(self, Xnew):
#         T = np.dot(Xnew, self.P)
#         oneCol = np.ones(T.shape[0])
#         T = np.c_[oneCol, T]
#         ans = self.mlr.predict(T)
#         return ans
#
#     def fTest(self, arfa):
#         return self.mlr.Ftest(arfa)
#
# if __name__=="__main__":
#     S=np.loadtxt("S:\python 数学建模\S-093790.txt")
#     S=S.T
#     C=np.loadtxt("S:\python 数学建模\C-093790.txt")
#     C=C.T
#     pcr=PCR(S,C)
#     Stest=np.loadtxt("S:\python 数学建模\S-093843.txt")
#     Stest=Stest.T
#     print("相邻特征的比值")
#     print(pcr.confirmPCs().round(5))
#     k=int(input("请输入主成分数:"))
#     pcr.model(k)
#     print("回归系数",pcr.A.round(5))
#     ans=pcr.predict(Stest)
#     print("自身预报结果：",ans.round(3))

