#-*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)    # 解决windows环境下画图汉字乱码问题


def linearRegression(alpha=0.01,num_iters=400):
    print(u"加载数据...\n")
    # global data
    # global X
    # global y
    # global theta
    data = loadtxtAndcsv_data("data.txt",",",np.float64)  #读取数据 data : ndarray(47,3)
    X = data[:,0:-1]      # X对应0到倒数第2列  (前两列)  (47,2)
    y = data[:,-1]        # y对应最后一列         (47)
    m = len(y)            # 总的数据条数 47
    col = data.shape[1]      # data的列数 3
    X,mu,sigma = featureNormaliza(X)    # 对每列均值归一化
    plot_X1_X2(X)         # 画图看一下归一化效果
    
    X = np.hstack((np.ones((m,1)),X))    # 在X前加一列1 X:(47,3)
    
    print(u"\n执行梯度下降算法....\n")
    
    theta = np.zeros((col,1))    #theta:(3,1)
    y = y.reshape(-1,1)   #将行向量转化为列   y:(47,1)
    # 传递原始数据
    theta,J_history = gradientDescent(X, y, theta, alpha, num_iters)
    
    plotJ(J_history, num_iters)
    
    return mu,sigma,theta   #返回均值mu,标准差sigma,和学习的结果theta
    
   
# 加载txt和csv文件
def loadtxtAndcsv_data(fileName,split,dataType):
    # 读取数据
    return np.loadtxt(fileName,delimiter=split,dtype=dataType) # 'data.txt'  split=, datatype=np.float64

# 加载npy文件
def loadnpy_data(fileName):
    return np.load(fileName)

# 均值归一化feature
def featureNormaliza(X):
    # X_norm = np.array(X)            #将X转化为numpy数组对象，才可以进行矩阵的运算
    X_norm = X
    #定义所需变量
    mu = np.zeros((1,X.shape[1]))      # (1,2) 所有行x1 、x2的均值
    sigma = np.zeros((1,X.shape[1]))   # (1,2) 所有行x1 、x2的标准差
    # 统计均值、标准差
    mu = np.mean(X_norm,0)          # 求每一列的平均值（0指定为列，1代表行）
    sigma = np.std(X_norm,0)        # 求每一列的标准差
    # 批量归一化
    for i in range(X.shape[1]):     # 遍历2列
        X_norm[:,i] = (X_norm[:,i]-mu[i])/sigma[i]  # 归一化
    
    return X_norm,mu,sigma

# 画二维图
def plot_X1_X2(X):
    plt.scatter(X[:,0],X[:,1])
    plt.show()


# 梯度下降算法
def gradientDescent(X,y,theta,alpha,num_iters):
    '''
    X (47,3)
    Y (47,1)
    theta (3,1)
    alpha 0.01
    num_iters 400
    '''

    m = len(y)      # len返回多维数组第一个维度的大小 47
    n = len(theta)  # 3

    # ndarray转matrix
    temp = np.matrix(np.zeros((n,num_iters)))   # 暂存每次迭代计算的theta，转化为矩阵形式 temp:matrix(3,47)
    
    J_history = np.zeros((num_iters,1)) #记录每次迭代计算的代价值  J_history: ndarray (400,1)
    
    for i in range(num_iters):  # 遍历迭代次数    
        h = np.dot(X,theta)     # 计算内积，matrix可以直接乘
        temp[:,i] = theta - ((alpha/m)*(np.dot(np.transpose(X),h-y)))   #梯度的计算
        theta = temp[:,i]                           # 梯度下降后的theta
        J_history[i] = computerCost(X,y,theta)      #调用计算代价函数
        print('.', end=' ')      
    return theta,J_history  

# 计算代价函数
def computerCost(X,y,theta):
    '''
    X,y,theta均为列向量
    '''
    m = len(y)
    J = 0
    # MSE/2 计算均方误差
    # X:(47,3) theta:(3,1) y:(47,1)
    # 应该是@进行矩阵乘法，*进行逐个元素相乘
    # (1，47)*(47,1)同时实现了平方和加和
    J = (np.transpose(X@theta-y))@(X@theta-y)/(2*m) #计算代价J (-2,47)*(47,1)同时实现了平方加和
    return J

# 画每次迭代代价的变化图
def plotJ(J_history,num_iters):
    x = np.arange(1,num_iters+1)
    plt.plot(x,J_history)
    plt.xlabel(u"迭代次数",fontproperties=font) # 注意指定字体，要不然出现乱码问题
    plt.ylabel(u"代价值",fontproperties=font)
    plt.title(u"代价随迭代次数的变化",fontproperties=font)
    plt.show()

# 测试linearRegression函数

def testLinearRegression():
    mu,sigma,theta = linearRegression(0.01,400)
    print (u"\n计算的theta值为：\n",theta)
    print (u"\n预测结果为：%f"%predict(mu, sigma, theta))
    
# 测试学习效果（预测）
def predict(mu,sigma,theta):
    result = 0
    # 注意归一化
    predict = np.array([2104,3])
    norm_predict = (predict-mu)/sigma
    final_predict = np.hstack((np.ones((1)),norm_predict))
    
    result = np.dot(final_predict,theta)    # 预测结果
    return result
    
    
if __name__ == "__main__":
    testLinearRegression()