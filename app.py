from flask import Flask, render_template, request, redirect, url_for
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import os

app = Flask(__name__)

# Đường dẫn tuyệt đối mô hình PhoBERT
MODEL_PATH = r"C:\Users\vanng\Downloads\chuyebde2\phobert_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)


# Lưu kết quả vào biến toàn cục
results = []

def predict_phobert(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1).item()
    return prediction

@app.route("/", methods=["GET", "POST"])
def index():
    global results
    if request.method == "POST":
        action = request.form.get("action")
        if action == "predict":
            # Lấy dữ liệu từ form
            input_data = {
                "nghe_cha": request.form.get("nghe_cha"),
                "nghe_me": request.form.get("nghe_me"),
                "gio_hoc": request.form.get("gio_hoc"),
                "gio_choi": request.form.get("gio_choi"),
                "gio_mang": request.form.get("gio_mang"),
                "gpa": request.form.get("gpa"),
                "thich_nghi": request.form.get("thich_nghi"),
                "phuong_phap": request.form.get("phuong_phap"),
                "ho_tro": request.form.get("ho_tro"),
                "co_so": request.form.get("co_so"),
                "chat_luong": request.form.get("chat_luong"),
                "chuong_trinh": request.form.get("chuong_trinh"),
                "tinh_canh_tranh": request.form.get("tinh_canh_tranh"),
                "anh_huong": request.form.get("anh_huong")
            }
            # Tạo chuỗi đầu vào cho PhoBERT
            input_text = " ".join(input_data.values())
            prediction = predict_phobert(input_text)
            input_data["ket_qua"] = f"Kết quả: {prediction}"
            results.append(input_data)
        elif action == "save":
            # Lưu vào CSV
            df = pd.DataFrame(results)
            df.to_csv("ket_qua_du_doan.csv", index=False)
        elif action.startswith("delete_"):
            # Xoá dòng
            index = int(action.split("_")[1])
            if 0 <= index < len(results):
                results.pop(index)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
