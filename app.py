import streamlit as st
import pandas as pd
import io

# 初期タスクのリストを作成
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# タスクを追加する関数
def add_task(task):
    st.session_state.tasks.append(task)

# タスクを削除する関数
def delete_task(index):
    del st.session_state.tasks[index]

# CSVに変換してダウンロードできるようにする関数
def convert_tasks_to_csv():
    task_df = pd.DataFrame(st.session_state.tasks, columns=["タスク"])
    csv = task_df.to_csv(index=False)
    return csv

# タイトル
st.title('タスク管理アプリ')

# 新しいタスクを追加
task_input = st.text_input('新しいタスクを入力してください')

if st.button('タスクを追加'):
    if task_input:
        add_task(task_input)
        st.success('タスクが追加されました！')
    else:
        st.error('タスクを入力してください。')

# タスクの表示
if st.session_state.tasks:
    st.subheader('タスク一覧')
    task_df = pd.DataFrame(st.session_state.tasks, columns=["タスク"])
    for index, row in task_df.iterrows():
        task_name = row["タスク"]
        if st.button(f'削除 {task_name}', key=index):
            delete_task(index)
            st.success(f'{task_name} が削除されました！')

else:
    st.write('現在、タスクはありません。')

# CSVダウンロードボタン
if st.session_state.tasks:
    csv = convert_tasks_to_csv()
    st.download_button(
        label="タスクをCSVとしてダウンロード",
        data=csv,
        file_name='tasks.csv',
        mime='text/csv'
    )
