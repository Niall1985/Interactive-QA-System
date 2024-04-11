import json
import re
import pyttsx3
import tkinter as tk

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_data(data, file_path):
    # Convert keys to lowercase and remove special characters
    cleaned_data = {re.sub(r'[^\w\s]', '', key.lower()): value.lower() for key, value in data.items()}
    with open(file_path, 'w') as f:
        json.dump(cleaned_data, f, indent=4)

def get_answer(question, data):
    # Remove special characters from the question
    question = re.sub(r'[^\w\s]', '', question)
    return data.get(question.lower(), None)

def ask_question():
    question = question_entry.get().lower()
    answer = get_answer(question, qa_data)
    text_to_speech = pyttsx3.init()
    text_to_speech.say(answer)
    text_to_speech.setProperty('rate', 100)
    text_to_speech.runAndWait()

    if answer:
        answer_label.config(text="Answer: " + answer)
    else:
        answer_label.config(text="I don't know the answer to that question.")
        teach_me_button.pack()

def teach_me():
    new_question = new_question_entry.get()
    new_answer = new_answer_entry.get()
    # Remove special characters and convert to lowercase for both question and answer
    new_question = re.sub(r'[^\w\s]', '', new_question.lower())
    new_answer = new_answer.lower()
    # Append cleaned question and answer to the data
    qa_data[new_question] = new_answer
    save_data(qa_data, data_file)
    print("Thanks for teaching me!")
    teach_me_button.pack_forget()
    new_question_entry.delete(0, tk.END)
    new_answer_entry.delete(0, tk.END)

data_file = "qa_data.json"
qa_data = load_data(data_file)

root = tk.Tk()
root.title("Question Answering System")

question_label = tk.Label(root, text="Ask me a question:")
question_label.pack()

question_entry = tk.Entry(root, width=50)
question_entry.pack()

ask_button = tk.Button(root, text="Ask", command=ask_question)
ask_button.pack()

answer_label = tk.Label(root, text="")
answer_label.pack()

teach_me_button = tk.Button(root, text="Teach Me", command=teach_me)

new_question_label = tk.Label(root, text="What's the question?:")
new_question_label.pack_forget()

new_question_entry = tk.Entry(root, width=50)
new_question_entry.pack_forget()

new_answer_label = tk.Label(root, text="What's the answer?:")
new_answer_label.pack_forget()

new_answer_entry = tk.Entry(root, width=50)
new_answer_entry.pack_forget()

root.mainloop()
