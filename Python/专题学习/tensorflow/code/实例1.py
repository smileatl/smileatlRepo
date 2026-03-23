import tensorflow as tf
import numpy as np

# create data
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data*0.1 + 0.3

# create tensorflow structure start
# 定义变量参数，用随机数列方式生成参数,维度为1，数值范围在-1~1之间
# weights一般是个矩阵
Weights=tf.Variable(tf.random_uniform([1],-1.0,1.0))
biases=tf.Variable(tf.zeros([1]))

y=Weights*x_data+biases

loss=tf.reduce_mean(tf.square(y-y_data))
# 建立优化器，lr=0.5
optimizer=tf.train.GradientDescentOptimizer(0.5)
# 用优化器减少误差
train=optimizer.minimize(loss)

# 建立了很多变量，但是在神经网络中还没有初始化我们的变量
# 神经网络就是一个大的图
# 可以先把神经网络的结构先做好，再初始化这个结构，让它们真正地活动起来
init=tf.initialize_all_variables()
# create tensorflow structure start

# 接下来要把这个结构激活，初始化
# 初始化之前定义一个session
sess=tf.Session()
# run的时候就像一个指针，指向了我要处理的地方，处理的地方就被激活起来了
# 这里init就被激活了，这个系统、图、神经网络的结构就被激活了
sess.run(init)      # Very important

for step in range(201):
	sess.run(train)
	if step % 20 == 0:
		# run指向我的Weights和biases，告诉我现在的Weights和biases是多少
		print(step,sess.run(Weights),sess.run(Weights))