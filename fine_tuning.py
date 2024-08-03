from sentence_transformers import SentenceTransformerTrainer, SentenceTransformerTrainingArguments
from sentence_transformers.losses import MultipleNegativesRankingLoss
from sentence_transformers import SentenceTransformer
from datasets import Dataset

dataset = Dataset.load_from_disk('datasets/test')

train_dataset = Dataset.load_from_disk('datasets/train')
eval_dataset = Dataset.load_from_disk('datasets/eval')

model = SentenceTransformer("sentence-transformers/all-distilroberta-v1")
loss = MultipleNegativesRankingLoss(model)

args = SentenceTransformerTrainingArguments(
    output_dir="models/fine_tuned_for_summa",
    num_train_epochs=2,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_ratio=0.1,
    eval_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=2,
    logging_steps=100
)

trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    loss=loss
)

trainer.train()

model.save_pretrained("models/fine_tuned_for_summa")
