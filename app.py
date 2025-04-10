import streamlit as st
import random

st.title("🎯 おみくじアプリ")
st.write("ボタンを押して、今日の運勢を占おう！")

if st.button("おみくじを引く"):
    result = random.choice(["大吉", "中吉", "小吉", "凶", "大凶"])
    st.subheader(f"🎉 結果：{result} 🎉")
