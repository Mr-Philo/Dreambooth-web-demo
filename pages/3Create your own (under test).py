import streamlit as st
import os
import time

def sumit_trans_prompt(prompt):
    for str in ["me", "I", "sumit", "Sumit", "sumit chauhan", "Sumit Chauhan"]:
        prompt = prompt.replace(str, "a #4*js! woman")
    return prompt
        
st.set_page_config(layout="wide")
st.title("After your training process finished, you could create your own here!")

st.header("Please input your unique USER NAME, so you could reuse your model next time~")
username = st.text_input('Input your username:', value="sumit")
user_root_dir = os.path.join("./Users",username)
user_model_dir = os.path.join(user_root_dir, "model")
user_out_dir = os.path.join(user_root_dir, "output")
user_log_dir = os.path.join(user_root_dir, "log")
if not os.path.exists(user_out_dir):
    os.makedirs(user_out_dir)
if not os.path.exists(user_log_dir):
    os.makedirs(user_log_dir)

if not os.path.exists(user_model_dir):
    st.write("Model doesn't exist. Please train your model first.")
    
if (username == 'sumit'):
    user_input = st.text_input('Add prompts for your inputed unique person (use \'I\', \'me\', \'sumit\' to represent sumit)','A photo of me wearing sunglasses')
    user_input = sumit_trans_prompt(user_input)
else:
    user_input = st.text_input('Add prompts for your inputed unique person','photo of a #4*js! man')
# TODO: add sonme example prompts for users
# st.text("Here we presented with some examples:")

st.subheader("Choose the num of pics you want to generate:")
columns = st.columns(3)
with columns[1]:
    rows = st.number_input("rows of pics", min_value=1, max_value=4, value=1)
with columns[2]:
    cols = st.number_input("cols of pics", min_value=1, max_value=4, value=1)
with columns[0]:
    st.metric(label="total num of pics", value=rows*cols)
seed = st.slider('Choose a seed (same seed will bring same results):', 0, 1024, 512)
    
if st.button('Generate', key=0):
    uuid_str = time.strftime("%Y-%m-%d %H-%M-%S",time.localtime()) 
    log_file_name ='%s.log' % uuid_str
    log_dir = os.path.join(user_log_dir, log_file_name)
    
    t0 = time.time()
    print("We are ready to generate")
    st.write("We are ready to generate")
    
    os.system('''
            CUDA_VISIBLE_DEVICES=1 python infer.py --model "{}" --prompt "{}" --save_path "{}" --rows {} --cols {} --seed {} --skip_single
            '''.format(user_model_dir, user_input, user_out_dir, rows, cols, seed))
    #python -u infer.py --model "{}" --prompt "{}" --save_path "{}" --rows {} --cols {} > "{}" 2>&1
    #.format(user_model_dir, user_input, user_out_dir, rows, cols, log_dir))
    
    t1 = time.time()
    st.header("You get:")
    st.image(os.path.join(user_out_dir, "latest.png"))
    st.header("Time cost {:.1f}s".format(t1-t0))
    st.header("Enjoy!")
