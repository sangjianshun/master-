import torch
import torch.nn.functional as F

from AI.GCN.GCN_model import GCN
from AI.dataset.gen_dataset import GenCoreDataset

epoch = 200

genCoreDataset = GenCoreDataset()
all_feature,all_label,adj_matrix,idx_train,idx_val,idx_test = genCoreDataset.main_process()

model = GCN(all_feature.shape[1], hidden_dim = 16, label_dim = len(genCoreDataset.label2num))
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)


def accuracy(output, labels):
    preds = output.max(1)[1].type_as(labels)
    correct = preds.eq(labels).double()
    correct = correct.sum()
    return correct / len(labels)

model.train()
for i in range(epoch):
    optimizer.zero_grad()  # 梯度初始化为0
    output = model(all_feature, adj_matrix)  # 计算模型的输出
    loss_train = F.nll_loss(output[idx_train], all_label[idx_train])
    loss_train.backward()   # 计算梯度
    optimizer.step()
    print(loss_train)


model.eval()
output = model(all_feature, adj_matrix)
loss_test = F.nll_loss(output[idx_test], all_label[idx_test])
acc_test = accuracy(output[idx_test], all_label[idx_test])
print("Test set results:",
      "loss= {:.4f}".format(loss_test.item()),
      "accuracy= {:.4f}".format(acc_test.item()))
