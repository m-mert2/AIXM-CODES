"""
Uygulamayı bu script ile başlat: python run.py
Bu script önce eski .pyc cache'leri temizler, sonra Flask'ı başlatır.
"""
import shutil, os, sys

# __pycache__ temizle
cache = os.path.join(os.path.dirname(__file__), '__pycache__')
if os.path.exists(cache):
    shutil.rmtree(cache)
    print("✅ __pycache__ temizlendi")

# app'i başlat
from app import app
app.run(debug=True, port=5000)
