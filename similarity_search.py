from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.schema.document import Document

# embeddings = SentenceTransformerEmbeddings(
#     model_name="flax-sentence-embeddings/all_datasets_v3_distilroberta-base",
#     encode_kwargs={'normalize_embeddings': False}
# )

embeddings = SentenceTransformerEmbeddings(
    model_name="models/fine_tuned_for_summa",
    encode_kwargs={'normalize_embeddings': False}
)

objections_file = 'data/objections_I_II.txt'
replies_file = 'data/replies_I_II.txt'


def create_faiss_index():
    docs = []
    with open(replies_file, encoding="utf8") as file:
        for line in file:
            docs.append(Document(page_content=line.strip()))
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_I_II")


def load_faiss_index():
    return FAISS.load_local("faiss_I_II", embeddings, allow_dangerous_deserialization=True)


create_faiss_index()

db = load_faiss_index()
retriever = db.as_retriever()


def search_response(query):
    doc = db.similarity_search(query, k=1)[0]
    return doc.page_content


objections = []
with open(objections_file, encoding="utf8") as file:
    for line in file:
        objections.append(line.strip())

replies = []
with open(replies_file, encoding="utf8") as file:
    for line in file:
        replies.append(line.strip())

score = 0
for objection, reply in zip(objections, replies):
    prediction = search_response(objection)
    if prediction == reply:
        score += 1

print(f"Accuracy: {score}/{len(objections)} = {score / len(objections)}")
