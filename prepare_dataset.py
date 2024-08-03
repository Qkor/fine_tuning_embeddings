from datasets import load_dataset, Dataset
from sklearn.model_selection import train_test_split

objections = []
with open('data/objections_no_I_II.txt', encoding="utf8") as file:
    for line in file:
        objections.append(line.strip())

replies = []
with open('data/replies_no_I_II.txt', encoding="utf8") as file:
    for line in file:
        replies.append(line.strip())

objections_test = []
with open('data/objections_I_II.txt', encoding="utf8") as file:
    for line in file:
        objections_test.append(line.strip())

replies_test = []
with open('data/replies_I_II.txt', encoding="utf8") as file:
    for line in file:
        replies_test.append(line.strip())


test_dataset = Dataset.from_dict({'anchor': objections_test, 'positive': replies_test})
train_objections, eval_objections, train_replies, eval_replies = train_test_split(objections, replies, test_size=0.2)
train_dataset = Dataset.from_dict({'anchor': train_objections, 'positive': train_replies})
eval_dataset = Dataset.from_dict({'anchor': eval_objections, 'positive': eval_replies})

train_dataset.save_to_disk('datasets/train')
test_dataset.save_to_disk('datasets/test')
eval_dataset.save_to_disk('datasets/eval')
