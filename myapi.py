import os
import re
from flask import Flask, request, abort, jsonify, send_from_directory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if not os.path.exists("/tmp"):
    os.makedirs("/tmp")


def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


plagiarism_results = set()


def check_plagiarism():
    global s_vectors
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            score = sim_score*100
            plagiarism_results.add(score)
    return plagiarism_results


application = Flask(__name__)
s_vectors = None


@application.route("/", methods=["GET"])
def normal():
    return "Yippie2"


@application.route("/plag/", methods=["POST"])
def post_file():
    """Upload a file."""
    global s_vectors
    file = request.form['myarray']
    tf1, tf2 = open("./tmp/t1.txt", "w"), open("./tmp/t2.txt", "w")
    file = ["./tmp/t1.txt", "./tmp/t2.txt"]
    tf1.write(file[0])
    tf2.write(file[1])
    tf1.close()
    tf2.close()
    student_notes = [open(File).read() for File in file]
    vectors = vectorize(student_notes)
    s_vectors = list(zip(file, vectors))
    ans = list(check_plagiarism())
    return jsonify(ans)


@application.errorhandler(404)
def not_found(e):
    return "error yaar"


if __name__ == "__main__":
    application.run()
    # application.run(host="0.0.0.0", port=80)
