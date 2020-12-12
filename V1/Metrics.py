import torch
import math


# Num locations for each class. ndcg for the first n locations to be found.
def ndcg_at_n(real_score, predict_score, n, num):
    each_real_score = \
        [real_score[i: i + num] for i in range(0, len(real_score), num)]
    each_predict_score = \
        [predict_score[i: i + num] for i in range(0, len(predict_score), num)]

    total_ndcg = 0
    total_num = len(each_predict_score)
    for i in range(len(each_predict_score)):
        now_real_score = each_real_score[i]
        now_predict_score = each_predict_score[i]

        _, real_rank = torch.sort(now_real_score, descending=True)
        _, pre_rank = torch.sort(now_predict_score, descending=True)

        target = real_rank[0]
        now_ndcg = 0
        for j in range(n):
            if target == pre_rank[j]:
                now_ndcg = 1 / math.log2(j + 2)
                break
        total_ndcg += now_ndcg

    return total_ndcg / total_num


# Num locations for each class. hr for the first n locations to be found.
def hr_at_n(real_score, predict_score, n, num):
    each_real_score = \
        [real_score[i: i + num] for i in range(0, len(real_score), num)]
    each_predict_score = \
        [predict_score[i: i + num] for i in range(0, len(predict_score), num)]

    hit_num = 0
    total_num = len(each_predict_score)
    for i in range(len(each_predict_score)):
        now_real_score = each_real_score[i]
        now_predict_score = each_predict_score[i]

        _, real_rank = torch.sort(now_real_score, descending=True)
        _, pre_rank = torch.sort(now_predict_score, descending=True)

        if real_rank[0] in pre_rank[:n]:
            hit_num += 1

    return hit_num / total_num


def train_ndcg_at_n(train_real_score, train_predict_score, n, num):
    each_train_real_score = \
        [train_real_score[i: i + num] for i in range(0, len(train_real_score), num)]
    each_train_predict_score = \
        [train_predict_score[i: i + num] for i in range(0, len(train_predict_score), num)]

    total_ndcg = 0
    total_num = len(each_train_predict_score)

    for i in range(len(each_train_predict_score)):

        now_real_score = each_train_real_score[i]
        now_predict_score = each_train_predict_score[i]

        rel_val, real_rank = torch.sort(now_real_score, descending=True)
        _, pre_rank = torch.sort(now_predict_score, descending=True)
        one_set = []
        now_dcg = 0
        now_idcg = 0
        for j in range(len(rel_val)):
            if rel_val[j] == torch.tensor(0):
                break
            one_set.append(real_rank[j])
        one_set = torch.tensor(one_set)

        for j in range(n):
            if pre_rank[j] in one_set:
                now_dcg += 1 / math.log2(j + 2)

        num = min(n, len(one_set))
        for j in range(num):
            now_idcg += 1 / math.log2(j + 2)

        total_ndcg += now_dcg / now_idcg

    return total_ndcg / total_num


def train_hr_at_n(train_real_score, train_predict_score, n, num):
    each_train_real_score = \
        [train_real_score[i: i + num] for i in range(0, len(train_real_score), num)]
    each_train_predict_score = \
        [train_predict_score[i: i + num] for i in range(0, len(train_predict_score), num)]

    total_hit = 0
    total_num = len(each_train_predict_score)
    for i in range(len(each_train_predict_score)):
        now_real_score = each_train_real_score[i]
        now_predict_score = each_train_predict_score[i]

        rel_val, real_rank = torch.sort(now_real_score, descending=True)
        _, pre_rank = torch.sort(now_predict_score, descending=True)

        one_set = []
        for j in range(len(rel_val)):
            if rel_val[j] == torch.tensor(0):
                break
            one_set.append(real_rank[j])

        one_set = torch.tensor(one_set)
        for j in range(n):
            if pre_rank[j] in one_set:
                total_hit += 1
                break

    return total_hit / total_num


if __name__ == '__main__':
    # real_score = torch.tensor([0, 0, 0, 1, 0, 1, 0, 0])
    # pre_score = torch.tensor([0.8, 0.2, 0.1, 0.3, 0.9, 0.4, 0.5, 0.6])
    # print("ndcg: ", ndcg_at_n(real_score, pre_score, 3, 4))
    # print("hr: ", hr_at_n(real_score, pre_score, 3, 4))

    real_score = torch.tensor([0, 1, 0, 1, 0, 1, 0, 1])
    pre_score = torch.tensor([0.8, 0.2, 0.1, 0.3, 0.9, 1.1, 0.5, 0.6])
    print("train_ndcg: ", train_ndcg_at_n(real_score, pre_score, 2, 4))
    print("train_hr: ", train_hr_at_n(real_score, pre_score, 2, 4))
