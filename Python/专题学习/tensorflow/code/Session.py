import tensorflow as tf

# Session执行会话的控制
# 用Session.run这个语句来执行我们图片上面，我们已经创造好的结构上面
# 某一个点的、小图片的功能

# matrix1: tensor:(1,2)
# matrix2: tensor:(2,1)
matrix1 = tf.constant([[3, 3]])
matrix2 = tf.constant([[2],
                      [2]])


# matrix multiple np.dot(m1,m2)
# result: ndarray:(1,1)
product = tf.matmul(matrix1, matrix2)

# ## method 1
# sess=tf.Session()
# # 每run一次，tensorflow才会执行一下结构
# # 返回product的结果
# result=sess.run(product)
# print(result)
# # close有没有都行，有的话结构更整洁完整
# sess.close()

## method 2
#  打开这个session，以sess的名字命名它，就不用管关闭，运行到最后自动关上了
#  跟for循环一样，它是在with之内的语句
with tf.Session() as sess:
    result2 = sess.run(product)
    print(result2)

