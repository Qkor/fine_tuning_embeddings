from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import InformationRetrievalEvaluator
from datasets import Dataset

test_dataset = Dataset.load_from_disk('datasets/test')

queries = dict(enumerate(test_dataset["anchor"]))
queries = {str(key): value for key, value in queries.items()}
corpus = dict(enumerate(test_dataset["positive"]))
corpus = {str(key): value for key, value in corpus.items()}
relevant = dict()
for q, c in zip(queries, corpus):
    relevant[str(q)] = {str(c)}

evaluator = InformationRetrievalEvaluator(
    queries=queries,
    corpus=corpus,
    relevant_docs=relevant,
)

base_model = SentenceTransformer("sentence-transformers/all-distilroberta-v1")
tuned_model = SentenceTransformer("models/fine_tuned_for_summa")
base_results = evaluator(base_model)
tuned_results = evaluator(tuned_model)

print(evaluator.primary_metric)
print('base model performance: ', base_results[evaluator.primary_metric])
print('tuned model performance: ', tuned_results[evaluator.primary_metric])
