import streamlit as st

st.title("📝 タスク管理アプリ")

# セッションにタスクリストがなければ初期化
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# タスク入力
new_task = st.text_input("新しいタスクを入力")

# タスク追加
if st.button("追加") and new_task:
    st.session_state.tasks.append({"task": new_task, "done": False})
    st.experimental_rerun()  # ページ再読み込みで表示更新

# タスクリスト表示
st.subheader("📋 タスク一覧")

for i, task in enumerate(st.session_state.tasks):
    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
    with col1:
        st.checkbox(task["task"], value=task["done"], key=f"task_{i}", on_change=lambda i=i: toggle_done(i))
    with col2:
        if st.button("削除", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()

# 完了フラグの切り替え関数
def toggle_done(index):
    st.session_state.tasks[index]["done"] = not st.session_state.tasks[index]["done"]
