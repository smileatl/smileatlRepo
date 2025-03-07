import tensorflow as tf

# placeholder
# palceholder开始的时候先hold住一个类似变量的东西
# 但是到之后，sess.run的时候，要从外界传入进来
# 把它的placeholder填进去

# tensorflow大部分情况只能处理float32的数据
# placeholder指定它的类型,还能指定结构[2,2]
input1=tf.placeholder(tf.float32,)
input2=tf.placeholder(tf.float32)

output=tf.multiply(input1,input2)

with tf.Session() as sess:
    # 因为有placeholder需要每次传进去一个值
    # 传进去的时候，就是在我sess.run的时候
    # 以feed_dict的形式传进去，dict就是python当中的一个字典
    # 都是字典的形式input1:[7.],input2:[2.]
    print(sess.run(output,feed_dict={input1:[7.],input2:[2.]}))

# 总结：
# 用placeholder就意味着你想要在sess.run运行的时候再给它输入的值
# 用了placeholder跟feed_dict是绑定的