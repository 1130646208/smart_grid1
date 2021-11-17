# -- coding: utf-8 --
# 已知恶意节点，分析分组监督迭代次数
import random

ENC_MOD = 2**32-1


TOTAL_NODE_NUM = 100
BREAK_NODE_NUM = 10
INITIAL_GROUP_NUM = 10
NODES = []
__GROUP_RECORD = {}
__NEW_GROUP_RECORD = []


ITER_COUNT = 0


class Node:
    def __init__(self, id_, usage_value=-1, group_id=-1, mod=ENC_MOD):
        self.id_ = id_
        self.group_id = group_id
        self.usage_value = usage_value
        self.is_abnormal = False
        self.counterparts = []
        self.keys = {}
        self.mod = mod


def init_nodes(n):
    """
    初始化节点
    :param n:
    """
    for i in range(n):
        NODES.append(Node(i))


def initial_partition(k, n):
    """
    节点随机分组
    :param k: minimal group size
    :param n: total node number
    :return: None
    """
    # assert group size >= 2 so that can generate key
    assert k >= 3
    group_num = n // k
    group_ids = [i for i in range(group_num)]
    indexes = [i for i in range(n)]
    # random.shuffle(indexes)
    for i in range(n):
        current_id = group_ids[i % group_num]
        if not __GROUP_RECORD.get(current_id):
            __GROUP_RECORD[current_id] = [NODES[indexes[i]].id_]
        else:
            __GROUP_RECORD.get(current_id).append(NODES[indexes[i]].id_)
        NODES[indexes[i]].group_id = current_id
    # update counterpart
    for i in range(n):
        NODES[i].counterparts.extend(__GROUP_RECORD.get(NODES[i].group_id))


def gen_key():
    def gen_key_for_list(node_ind_list: list):
        """
        为NODES中的节点生成密钥（前提是已经分组完成了）
        :param node_ind_list:节点索引列表
        """
        for a in range(len(node_ind_list)-1):
            for b in range(a+1, len(node_ind_list)):
                rand_key = random.randint(0, ENC_MOD)
                NODES[node_ind_list[a]].keys[node_ind_list[b]] = rand_key
                NODES[node_ind_list[b]].keys[node_ind_list[a]] = -rand_key

    for k, v in __GROUP_RECORD.items():
        gen_key_for_list(v)


def homo_enc(data, key):
    """
    同态加密
    :param data: 明文
    :param key: 密钥
    :return: 密文
    """
    assert data < ENC_MOD
    assert key < ENC_MOD
    return (data + key) % ENC_MOD


def homo_dec(cip, key):
    """
    同态解密
    :param cip: 密文
    :param key: 密钥
    :return: 明文
    """
    assert cip < ENC_MOD
    assert key < ENC_MOD
    return (cip - key) % ENC_MOD


def random_break(break_num):
    """
    随机设置故障节点
    :param break_num: 故障节点个数
    """
    assert break_num <= TOTAL_NODE_NUM
    temp_list = [i for i in range(TOTAL_NODE_NUM)]
    for _ in range(break_num):
        rand_index = temp_list.pop(random.randint(0, len(temp_list)-1))
        NODES[rand_index].is_abnormal = True


def repartition_dfs(node_list):
    global ITER_COUNT
    ITER_COUNT += 1
    # 递归停止条件
    if is_convergence(node_list):
        __NEW_GROUP_RECORD.append(node_list[:])
        return
    # 递归逻辑
    random.shuffle(node_list)
    p = len(node_list) // 2
    repartition_dfs(node_list[:p])
    repartition_dfs(node_list[p:])


def repartition():
    for group_id, node_list in __GROUP_RECORD.items():
        repartition_dfs(node_list)


def is_convergence(node_list):
    if len(node_list) == 0:
        return True
    abnormal_count = 0
    abnormal_node = []
    for node_ind in node_list:
        if NODES[node_ind].is_abnormal:
            abnormal_node.append(node_ind)
            abnormal_count += 1
    # 只有一个异常节点，收敛
    if abnormal_count <= 1:
        # print("收敛，异常节点", abnormal_node)
        return True
    return False


def run(total_node_num, initial_group_num, break_num):
    global TOTAL_NODE_NUM
    global INITIAL_GROUP_NUM
    global BREAK_NODE_NUM
    TOTAL_NODE_NUM = total_node_num
    INITIAL_GROUP_NUM = initial_group_num
    BREAK_NODE_NUM = break_num
    init_nodes(TOTAL_NODE_NUM)
    initial_partition(TOTAL_NODE_NUM // INITIAL_GROUP_NUM, TOTAL_NODE_NUM)
    # gen_key()
    random_break(BREAK_NODE_NUM)
    repartition()
    # print("节点总数:{}\t恶意节点数:{}\t初始分组数:{}\t迭代次数:{}\t最终分组数:{}\t".
    #       format(TOTAL_NODE_NUM, BREAK_NODE_NUM, INITIAL_GROUP_NUM, ITER_COUNT, len(__NEW_GROUP_RECORD)))
    return TOTAL_NODE_NUM, BREAK_NODE_NUM, INITIAL_GROUP_NUM, ITER_COUNT, len(__NEW_GROUP_RECORD)


def reset():
    global NODES, __GROUP_RECORD, __NEW_GROUP_RECORD, ITER_COUNT
    NODES.clear()
    __GROUP_RECORD.clear()
    __NEW_GROUP_RECORD.clear()
    ITER_COUNT = 0


# 恶意节点数量
# if __name__ == '__main__':
#     _iter = 20
#     total_node_num = 200
#     initial_group_num = 5
#     break_num = [i for i in range(0, 100, 5)]
#
#     print("节点总数\t初始分组数\t恶意节点数\t平均迭代次数")
#     for j in break_num:
#         _sum = 0
#         for _ in range(_iter):
#             reset()
#             res = run(total_node_num=total_node_num, initial_group_num=initial_group_num, break_num=j)
#             _sum += res[3]
#         print("{}\t{}\t{}\t{}".format(total_node_num, initial_group_num, j, _sum / _iter))

# 节点总数
if __name__ == '__main__':
    _iter = 40
    total_node_num = [i for i in range(25, 1000, 10)]
    initial_group_num = 5
    break_num = 25

    print("节点总数\t初始分组数\t恶意节点数\t平均迭代次数")
    for j in total_node_num:
        _sum = 0
        for _ in range(_iter):
            reset()
            res = run(total_node_num=j, initial_group_num=initial_group_num, break_num=break_num)
            _sum += res[3]
        print("{}\t{}\t{}\t{}".format(j, initial_group_num, break_num, _sum / _iter))

# 初始分组数
# if __name__ == '__main__':
#     _iter = 40
#     total_node_num = 201
#     initial_group_num = [i for i in range(2, 71, 5)]
#     break_num = 32
#
#     print("节点总数\t初始分组数\t恶意节点数\t平均迭代次数")
#     for j in initial_group_num:
#         _sum = 0
#         for _ in range(_iter):
#             reset()
#             res = run(total_node_num=total_node_num, initial_group_num=j, break_num=break_num)
#             _sum += res[3]
#         print("{}\t{}\t{}\t{}".format(total_node_num, j, break_num, _sum / _iter))
