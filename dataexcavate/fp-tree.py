from collections import defaultdict


class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None

    def increment(self, cnt=1):
        self.count += cnt

class FPTree:
    def __init__(self):
        self.root = FPNode(None, 1, None)
        self.header = defaultdict(list)

    def insert_tree(self, items, node):
        if not items:
            return
        first = items[0]
        if first in node.children:
            node.children[first].increment()
        else:
            new_node = FPNode(first, 1, node)
            node.children[first] = new_node
            self.header[first].append(new_node)
        self.insert_tree(items[1:], node.children[first])

def get_prefix_paths(tree, target_item):
    paths = []
    for node in tree.header[target_item]:
        path = []
        cur = node.parent
        while cur.item is not None:
            path.append(cur.item)
            cur = cur.parent
        if path:
            paths.append(("".join(reversed(path)), node.count))
    return paths

def build_tree_silent(transactions, min_sup, rank):
    item_count = defaultdict(int)
    for tran in transactions:
        for item in tran:
            item_count[item] += 1
    freq_items = {k: v for k, v in item_count.items() if v >= min_sup}
    if not freq_items:
        return FPTree(), freq_items
    
    tree = FPTree()
    for tran in transactions:
        filtered = [x for x in tran if x in freq_items]
        filtered.sort(key=lambda x: rank[x])
        if filtered:
            tree.insert_tree(filtered, tree.root)
    return tree, freq_items

def mine_sub_patterns(cond_tree, beta, min_sup, rank):
    patterns = []
    for item in list(cond_tree.header.keys()):
        new_beta = beta + [item]
        paths = get_prefix_paths(cond_tree, item)
        cond_trans = []
        for p, c in paths:
            for _ in range(c):
                cond_trans.append(list(p))
        sub_tree, _ = build_tree_silent(cond_trans, min_sup, rank)
        sup = sum(n.count for n in cond_tree.header[item])
        patterns.append(f"{''.join(new_beta)}:{sup}")
        if sub_tree.root.children:
            patterns.extend(mine_sub_patterns(sub_tree, new_beta, min_sup, rank))
    return patterns

if __name__ == "__main__":
    raw_db = [
        ("100", ['f','a','c','d','g','i','m','p']),
        ("200", ['a','b','c','f','l','o']),
        ("300", ['b','f','h','j','m','p']),
        ("400", ['b','c','k','m','o','s']),
        ("500", ['a','f','c','e','l','n','o','p'])
    ]
    min_sup = 3
    priority = ['f', 'c', 'a', 'b', 'm', 'o', 'p']
    rank = {item: i for i, item in enumerate(priority)}

    print("-"*70)
    print(f"{'TID数据库':<12}{'原始项目集':<28}{'整理后的项目集':<28}")
    print("-"*70)
    cleaned_trans = []
    for tid, tran in raw_db:
        filtered = [x for x in tran if x in rank]
        filtered.sort(key=lambda x: rank[x])
        cleaned_trans.append(filtered)
        print(f"{tid:<14}{','.join(tran):<30}{','.join(filtered):<28}")
    print("-"*70)
    print()

    fp_tree = FPTree()
    for tran in cleaned_trans:
        fp_tree.insert_tree(tran, fp_tree.root)

    mine_order = ['p', 'o', 'm', 'b', 'a', 'c', 'f'] 
    table39 = []

    for item in mine_order:
        paths = get_prefix_paths(fp_tree, item)
        if not paths:
            cp_base = "∅"
        else:
            cp_base = ",".join([f"({p}:{c})" for p, c in paths])

        cond_trans = []
        for p, c in paths:
            for _ in range(c):
                cond_trans.append(list(p))
        cond_tree, cond_freq = build_tree_silent(cond_trans, min_sup, rank)
        
        if not cond_freq:
            cond_tree_str = "∅"
        else:
            sorted_freq = sorted(cond_freq.items(), key=lambda x: rank[x[0]])
            cond_tree_str = "(" + ",".join([f"{k}:{v}" for k, v in sorted_freq]) + ")"

        if cond_tree.root.children:
            sub_patterns = mine_sub_patterns(cond_tree, [item], min_sup, rank)
            pattern_str = ",".join(sub_patterns)
        else:
            pattern_str = "∅"

        table39.append([item, cp_base, cond_tree_str, pattern_str])

    print("-"*85)
    print(f"{'项':<6}{'条件模式基':<36}{'条件FP-tree':<18}{'产生的频繁模式':<24}")
    print("-"*85)
    for row in table39:
        print(f"{row[0]:<8}{row[1]:<38}{row[2]:<20}{row[3]:<24}")
    print("-"*85)
