import streamlit as st
import pandas as pd
from io import BytesIO

# 初期タスクのリストを作成
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []

# タスクを追加する関数
def add_task(task):
    st.session_state.tasks.append({'task': task, 'completed': False})

# タスクを削除する関数
def delete_task(index, completed=False):
    if completed:
        del st.session_state.completed_tasks[index]
    else:
        del st.session_state.tasks[index]

# タスクを完了としてマークする関数
def mark_completed(index):
    task = st.session_state.tasks.pop(index)
    task['completed'] = True
    st.session_state.completed_tasks.append(task)

# タスクを未完了に戻す関数
def mark_incomplete(index):
    task = st.session_state.completed_tasks.pop(index)
    task['completed'] = False
    st.session_state.tasks.append(task)

# CSVに変換してダウンロードできるようにする関数
def convert_tasks_to_csv():
    task_df = pd.DataFrame(st.session_state.tasks, columns=["タスク", "完了"])
    completed_df = pd.DataFrame(st.session_state.completed_tasks, columns=["タスク", "完了"])
    
    # バイナリストリームを使用
    csv_buffer = BytesIO()
    task_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    completed_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    csv_buffer.seek(0)
    return csv_buffer

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

# 未完了タスクの表示
if st.session_state.tasks:
    st.subheader('未完了タスク一覧')
    for index, task in enumerate(st.session_state.tasks):
        task_name = task['task']
        completed_checkbox = st.checkbox(f'{task_name}', key=f'checkbox_{index}')
        if completed_checkbox:
            mark_completed(index)
            st.success(f'{task_name} が完了しました！')
        elif st.button(f'削除 {task_name}', key=f'delete_{index}'):
            delete_task(index)
            st.success(f'{task_name} が削除されました！')

else:
    st.write('現在、未完了のタスクはありません。')

# 完了したタスクの表示
if st.session_state.completed_tasks:
    st.subheader('完了したタスク一覧')
    for index, task in enumerate(st.session_state.completed_tasks):
        task_name = task['task']
        # 完了したタスクにチェックボックスを追加して、未完了に戻すことができるようにする
        incomplete_checkbox = st.checkbox(f'{task_name} (完了)', key=f'incomplete_{index}')
        if incomplete_checkbox:
            mark_incomplete(index)
            st.success(f'{task_name} が未完了に戻されました！')

# CSVダウンロードボタン
if st.session_state.tasks or st.session_state.completed_tasks:
    csv_buffer = convert_tasks_to_csv()
    st.download_button(
        label="タスクをCSVとしてダウンロード",
        data=csv_buffer,
        file_name='tasks.csv',
        mime='text/csv'
    )

