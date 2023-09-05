import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
nltk.download('punkt')  # Download the NLTK data for sentence and word tokenization

def check_plagiarism():
    text1 = original_text.get("1.0", "end-1c")
    text2 = user_text.get("1.0", "end-1c")

    if not text1.strip() or not text2.strip():
        messagebox.showinfo("Plagiarism Checker", "Both fields must be filled.")
        return

    # Preprocess the paragraphs
    def preprocess(text):
        text = text.lower()
        text = ' '.join(word_tokenize(text))
        return text

    text1 = preprocess(text1)
    text2 = preprocess(text2)

    # Tokenize the paragraphs into sentences
    sentences1 = sent_tokenize(text1)
    sentences2 = sent_tokenize(text2)

    # Create TF-IDF vectors for the sentences
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([text1, text2])

    # Calculate cosine similarity between the paragraphs
    cosine_similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Define a similarity threshold
    threshold = 0.8

    # Check for plagiarism
    if cosine_similarity_matrix[0][0] >= threshold:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Plagiarism detected!")
        result_text.config(state=tk.DISABLED)
    else:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "No plagiarism detected.")
        result_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Plagiarism Checker")

# Create input widgets
original_label = tk.Label(root, text="Original Text:")
original_label.pack()

original_text = scrolledtext.ScrolledText(root, width=40, height=5)
original_text.pack()

user_label = tk.Label(root, text="User Text:")
user_label.pack()

user_text = scrolledtext.ScrolledText(root, width=40, height=5)
user_text.pack()

check_button = tk.Button(root, text="Check Plagiarism", command=check_plagiarism)
check_button.pack()

result_text = scrolledtext.ScrolledText(root, width=40, height=2, state=tk.DISABLED)
result_text.pack()

root.mainloop()
