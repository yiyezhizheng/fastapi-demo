import math
from collections import Counter

data = [
    {"Outlook": "Sunny", "Temperature": "Hot", "Humidity": 85, "Wind": "false", "PlayTennis": "No"},
    {"Outlook": "Sunny", "Temperature": "Hot", "Humidity": 90, "Wind": "true", "PlayTennis": "No"},
    {"Outlook": "Overcast", "Temperature": "Hot", "Humidity": 78, "Wind": "false", "PlayTennis": "Yes"},
    {"Outlook": "Rain", "Temperature": "Mild", "Humidity": 96, "Wind": "false", "PlayTennis": "Yes"},
    {"Outlook": "Rain", "Temperature": "Cool", "Humidity": 80, "Wind": "false", "PlayTennis": "Yes"},
    {"Outlook": "Rain", "Temperature": "Cool", "Humidity": 70, "Wind": "true", "PlayTennis": "No"},
    {"Outlook": "Overcast", "Temperature": "Cool", "Humidity": 65, "Wind": "true", "PlayTennis": "Yes"},
    {"Outlook": "Sunny", "Temperature": "Mild", "Humidity": 95, "Wind": "false", "PlayTennis": "No"},
    {"Outlook": "Sunny", "Temperature": "Cool", "Humidity": 70, "Wind": "false", "PlayTennis": "Yes"},
    {"Outlook": "Rain", "Temperature": "Mild", "Humidity": 80, "Wind": "false", "PlayTennis": "Yes"},
    {"Outlook": "Sunny", "Temperature": "Mild", "Humidity": 70, "Wind": "true", "PlayTennis": "Yes"},
    {"Outlook": "Overcast", "Temperature": "Mild", "Humidity": 90, "Wind": "true", "PlayTennis": "Yes"},
    {"Outlook": "Overcast", "Temperature": "Hot", "Humidity": 75, "Wind": "false", "PlayTennis": "Yes"},
    {"Outlook": "Rain", "Temperature": "Mild", "Humidity": 80, "Wind": "true", "PlayTennis": "No"},
]

attr_info = {
    "Outlook": False,
    "Temperature": False,
    "Humidity": True,
    "Wind": False
}
label_name = "PlayTennis"


def entropy(labels):
    cnt = Counter(labels)
    total = len(labels)
    ent = 0.0
    for count in cnt.values():
        p = count / total
        if p > 0:
            ent -= p * math.log2(p)
    return ent

def split_info(groups):
    total = sum(len(g) for g in groups.values())
    si = 0.0
    for g in groups.values():
        p = len(g) / total
        if p > 0:
            si -= p * math.log2(p)
    return si

def calc_discrete(dataset, attr):
    groups = {}
    for row in dataset:
        val = row[attr]
        if val not in groups:
            groups[val] = []
        groups[val].append(row[label_name])
    all_labels = [row[label_name] for row in dataset]
    original_I = entropy(all_labels)
    cond_ent = 0.0
    total = len(dataset)
    for lab_list in groups.values():
        weight = len(lab_list) / total
        cond_ent += weight * entropy(lab_list)
    gain = original_I - cond_ent
    si = split_info(groups)
    ratio = gain / si if si > 1e-9 else 0.0
    return gain, si, ratio, groups


def calc_continuous(dataset, attr):
    values = sorted({row[attr] for row in dataset})
    candidates = []
    for i in range(len(values) - 1):
        mid = (values[i] + values[i + 1]) / 2
        candidates.append(mid)

    best_ratio = -1.0
    best_gain = 0.0
    best_si = 0.0
    best_th = 0.0
    best_groups = {}
    all_labels = [row[label_name] for row in dataset]
    original_I = entropy(all_labels)

    for th in candidates:
        g_le = [r[label_name] for r in dataset if r[attr] <= th]
        g_gt = [r[label_name] for r in dataset if r[attr] > th]
        groups = {"<=" + str(th): g_le, ">" + str(th): g_gt}
        cond_ent = 0.0
        total = len(dataset)
        cond_ent += (len(g_le) / total) * entropy(g_le)
        cond_ent += (len(g_gt) / total) * entropy(g_gt)
        gain = original_I - cond_ent
        si = split_info(groups)
        ratio = gain / si if si > 1e-9 else 0.0

        if ratio >= best_ratio:
            best_ratio = ratio
            best_gain = gain
            best_si = si
            best_th = th
            best_groups = groups

    return best_gain, best_si, best_ratio, best_groups, best_th

def c45(dataset, attrs):
    labels = [row[label_name] for row in dataset]
    if len(set(labels)) == 1:
        return labels[0]
    if len(attrs) == 0:
        return Counter(labels).most_common(1)[0][0]

    best_ratio = -1.0
    best_attr = ""
    best_groups = {}
    best_th = 0.0
    is_best_cont = False

    for a in attrs:
        is_cont = attr_info[a]
        if is_cont:
            gain, si, ratio, grp, th = calc_continuous(dataset, a)
        else:
            gain, si, ratio, grp = calc_discrete(dataset, a)
            th = 0.0
        print(f"{a}：Gain={gain:.4f}  SplitInfo={si:.4f}  GainRatio={ratio:.4f}")
        if ratio > best_ratio:
            best_ratio = ratio
            best_attr = a
            best_groups = grp
            best_th = th
            is_best_cont = is_cont

    if is_best_cont:
        print(f"\n选中分裂属性：{best_attr}  最优增益比={best_ratio:.4f}  分割阈值={best_th}\n")
    else:
        print(f"\n选中分裂属性：{best_attr}  最优增益比={best_ratio:.4f}\n")

    tree = {best_attr: {}}
    remain_attrs = [x for x in attrs if x != best_attr]

    if is_best_cont:
        key_le = "<=" + str(best_th)
        key_gt = ">" + str(best_th)
        sub_le = [r for r in dataset if r[best_attr] <= best_th]
        sub_gt = [r for r in dataset if r[best_attr] > best_th]
        tree[best_attr][key_le] = c45(sub_le, remain_attrs)
        tree[best_attr][key_gt] = c45(sub_gt, remain_attrs)
    else:
        for val in best_groups:
            sub_data = [r for r in dataset if r[best_attr] == val]
            tree[best_attr][val] = c45(sub_data, remain_attrs)
    return tree


if __name__ == "__main__":
    attr_list = ["Outlook", "Temperature", "Humidity", "Wind"]
    decision_tree = c45(data, attr_list)
    print("最终决策树结构：")
    print(decision_tree)
