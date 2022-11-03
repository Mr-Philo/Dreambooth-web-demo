import streamlit as st
import os
import time

def sumit_trans_prompt(prompt):
    for str in ["me", "I", "sumit", "Sumit", "sumit chauhan", "Sumit Chauhan"]:
        prompt = prompt.replace(str, "a #4*js! woman")
    return prompt
        
st.set_page_config(layout="wide")
st.title("Some examples from Sumit Chauhan")
st.subheader("You could either search imags we have already generated or generate some by your own!")
chose = st.radio('choose', ('pre-generated', 'online generation'), label_visibility='hidden')
st.subheader("")
if chose == 'pre-generated':
    QueryToClass = {
        "Cartoon art head portrait of Sumit": 'cartoon',
        "A photo of Sumit wearing a chef cap": 'chef cap',
        "Concept art head portrait of Sumit": 'concept',
        "Cyberpunk head portrait of Sumit": 'cyberpunk',
        "Pencil sketch head portrait of Sumit": 'pencil sketch',
        "A photo of Sumit reading a book": 'reading',
        "A photo of Sumit surrouded by sunflowers": 'sunflower',
        "A photo of Sumit wearing sunglasses": 'sunglasses',
        "Portrait of Sumit with bird wings, high detailed, concept art, genshin impact": 'bird wing',
        "A photo of Sumit holding a bunch of flowers": 'bunch',
        "A photo of Sumit in front of Eiffel Tower": 'Eiffer',
        "A photo of Sumit on the beach": 'beach',
        "Digitial art of Sumit, trending on artstation": 'digital',
        "Impressionist art portrait of Sumit": 'impressionist',
        "Oil painting of Sumit": 'oil painting',
        "Drawing of Sumit with dramatic light, painted by seb mckinnon and greg rutkowski": 'dramatic',
        "Vintage Disney art of Sumit": 'Disney'
    }
    option = st.selectbox('Choose the prompt!', sorted(set(QueryToClass)))
    dir_name = os.path.join("./assets/sumit/result/", QueryToClass[option])
    dir = os.listdir(dir_name)
    column = st.columns(4)
    for i,filename in enumerate(dir):    
        column[i%4].image(os.path.join(dir_name, filename))
else:
    username = "sumit"
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
        
    
    user_input = st.text_input('Add some prompts! (use \'I\', \'me\', \'sumit\' to represent sumit)','A photo of me wearing sunglasses')
    user_input = sumit_trans_prompt(user_input)
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