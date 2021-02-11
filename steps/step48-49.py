import math
import numpy as np
import dezero
from dezero import optimizers
import dezero.functions as F
from dezero.models import MLP

#
# x, t = dezero.datasets.get_spiral(train=True)
# print(x.shape)
# print(t.shape)
#
# print(x[10], t[10])
# print(x[110], t[110])


max_epoch = 300
batch_size = 30
hidden_size = 10
lr = 1.0

# transform function for pre process
# sample 1
def trans_f(x):
    y = x / 2.0
    return y

# sample 2
from dezero import transforms
f = transforms.Normalize(mean=0.0, std=2.0)

# sample 3
f = transforms.Compose([transforms.Normalize(mean=0.0, std=2.0),
                        transforms.AsType(np.float64),
                        trans_f])

# with pre process
# train_set = dezero.datasets.Spiral(transform=f)
train_set = dezero.datasets.Spiral()
model = MLP((hidden_size, 3))
optimizer = optimizers.SGD(lr).setup(model)

data_size = len(train_set)
max_iter = math.ceil(data_size / batch_size)

for epoch in range(max_epoch):
    index = np.random.permutation(data_size)
    sum_loss = 0

    for i in range(max_iter):
        batch_index = index[i * batch_size:(i + 1) * batch_size]
        batch = [train_set[i] for i in batch_index]
        batch_x = np.array([example[0] for example in batch])
        batch_t = np.array([example[1] for example in batch])

        y = model(batch_x)
        loss = F.softmax_cross_entropy(y, batch_t)
        model.cleargrads()
        loss.backward()
        optimizer.update()

        sum_loss += float(loss.data) * len(batch_t)

    avg_loss = sum_loss / data_size
    print('epoch %d, loss %.2f' % (epoch + 1, avg_loss))
