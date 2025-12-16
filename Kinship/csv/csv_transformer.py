import csv
import os


def load_entity_mapping(entity_file):
    """加载实体名称到ID的映射"""
    entity2id = {}
    id2entity = {}
    with open(entity_file, 'r', encoding='utf-8') as f:
        for line in f:
            entity_name, entity_id = line.strip().split('\t')
            entity2id[entity_name] = entity_id
            id2entity[entity_id] = entity_name
    return entity2id, id2entity


def process_triples(triple_files, entity2id, output_file):
    """处理三元组文件并写入CSV"""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['head_id', 'relation_name', 'tail_id'])  # 写入表头

        for file in triple_files:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    head, rel, tail = line.strip().split('\t')
                    writer.writerow([entity2id[head], rel, entity2id[tail]])


def main():

    root_pth = '../basic/'
    # 输入文件路径
    entity_file = root_pth + 'entity2id.txt'
    train_file = root_pth + 'train.txt'
    valid_file = root_pth + 'valid.txt'
    test_file = root_pth + 'test.txt'

    # 输出文件路径
    id2ents_csv = './id2ents.csv'
    train_graph_csv = './train_graph.csv'
    full_graph_csv = './full_graph.csv'

    # 1. 加载实体映射
    entity2id, id2entity = load_entity_mapping(entity_file)

    # 2. 生成id2ents.csv
    with open(id2ents_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['entity_id', 'entity_name'])  # 写入表头
        for entity_id, entity_name in id2entity.items():
            writer.writerow([entity_id, entity_name])

    # 3. 生成train_graph.csv (仅使用train.txt)
    process_triples([train_file], entity2id, train_graph_csv)

    # 4. 生成full_graph.csv (使用train+valid+test.txt)
    process_triples([train_file, valid_file, test_file], entity2id, full_graph_csv)

    print("转换完成！")
    print(f"生成文件: {id2ents_csv}, {train_graph_csv}, {full_graph_csv}")


if __name__ == '__main__':
    main()
