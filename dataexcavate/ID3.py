import math
from collections import Counter

data = [
    {"性别": 1, "学生": 1, "民族": 0, "电脑": 1},
    {"性别": 0, "学生": 0, "民族": 0, "电脑": 1},
    {"性别": 1, "学生": 1, "民族": 0, "电脑": 1},
    {"性别": 1, "学生": 1, "民族": 0, "电脑": 1},
    {"性别": 1, "学生": 0, "民族": 0, "电脑": 0},
    {"性别": 1, "学生": 0, "民族": 1, "电脑": 0},
]
feature_names = ["性别", "学生", "民族"]
label_name = "电脑"

def entropy(pos_count, neg_count):
    total = pos_count + neg_count
    if total == 0:
        return 0.0
    p1 = pos_count / total
    p2 = neg_count / total
    ent = 0.0
    if p1 > 0:
        ent -= p1 * math.log2(p1)
    if p2 > 0:
        ent -= p2 * math.log2(p2)
    return ent

def calc_gain(dataset, attr):
    groups = {}
    for row in dataset:
        val = row[attr]
        if val not in groups:
            groups[val] = []
        groups[val].append(row[label_name])

    all_labels = [row[label_name] for row in dataset]
    pos_total = all_labels.count(1)
    neg_total = all_labels.count(0)
    original_I = entropy(pos_total, neg_total)

    E = 0.0
    total_num = len(dataset)
    for label_list in groups.values():
        p = label_list.count(1)
        n = label_list.count(0)
        weight = len(label_list) / total_num
        E += weight * entropy(p, n)

    gain = original_I - E
    return original_I, E, gain, groups

def id3(dataset, attrs):
    labels = [row[label_name] for row in dataset]
    if len(set(labels)) == 1:
        return labels[0]
    if len(attrs) == 0:
        return Counter(labels).most_common(1)[0][0]

    best_gain = -1.0
    best_attr = None
    best_groups = {}

    for a in attrs:
        I, E, gain, grp = calc_gain(dataset, a)
        print(f"{a}：总熵I={I:.3f}，条件熵E={E:.3f}，信息增益Gain={gain:.3f}")
        if gain > best_gain:
            best_gain = gain
            best_attr = a
            best_groups = grp

    print(f"\n选中分裂属性：{best_attr}，最大增益={best_gain:.3f}\n")
    tree = {best_attr: {}}
    remain_attrs = [x for x in attrs if x != best_attr]

    for val in best_groups:
        sub_data = [r for r in dataset if r[best_attr] == val]
        subtree = id3(sub_data, remain_attrs)
        tree[best_attr][val] = subtree

    return tree


if __name__ == "__main__":
    decision_tree = id3(data, feature_names)
    print("最终决策树结构:")
    print(decision_tree)
