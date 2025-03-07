import tensorflow as tf

# tensorflow里指定它是个变量，它才是个变量
# 可以给定值，名字
state = tf.Variable(0,name='counter')
print(state.name)
# 变量加常量还是等于变量
one=tf.constant(1)

new_value=tf.add(state,one)
# 让当前状态state等于new_value
update=tf.assign(state,new_value)

init=tf.initialize_all_variables()   # must have if define variable
with tf.Session() as sess:
    # 真正意义上的初始化所有变量
    sess.run(init)

    for _ in range(3):
        sess.run(update)
        # 直接print(state)是没有用的，一定把session的指针
        # 放到state上面去run一下，才会出现state的结果
        print(sess.run(state))
