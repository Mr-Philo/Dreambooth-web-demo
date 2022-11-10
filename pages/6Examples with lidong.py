import streamlit as st
import os
import time

print("Hello")

def lidong_trans_prompt(prompt):
    for str in ["me", "I", "lidong", "Lidong", "lidong zhou", "Lidong Zhou"]:
        prompt = prompt.replace(str, "a #4*js! man")
    return prompt
        
st.set_page_config(layout="wide")
st.title("Some examples from Lidong Zhou")

view_train = st.checkbox('View train images')       
if view_train:
    train_dir_name = "./assets/lidong/train"
    train_dir = sorted(os.listdir(train_dir_name))
    cols = st.columns(5)
    for j, name in enumerate(train_dir):
        cols[j%5].image(os.path.join(train_dir_name, name))
        
st.subheader("You could either search images we have already generated or generate some by your own!")
chose = st.radio('choose', ('pre-generated', 'online generation'), label_visibility='hidden')
st.subheader("")
if chose == 'pre-generated':
    QueryToClass = {
        "Cyberpunk head portrait of lidong": 'cyberpunk',
        "A photo of lidong on the beach": 'beach',
        "A fantasy style portrait painting of a lidong, smiling clean, shaven round face, rpg dnd, oil painting, unreal, rpg portrait, extremely detailed, artgerm, greg rutkowski greg": "fantasy",
        "Low poly art head portrait of lidong": 'low poly',
        "Digital art photo of lidong": 'digital',
        "A photo of lidong surrouded by sunflowers": 'sunflower',
        "Pencil sketch head portrait of lidong": 'pencil sketch',
        "Drawing of lidong with dramatic light, painted by seb mckinnon and greg rutkowski": 'dramatic',
        "Photo of lidong wearing a chef cap": 'chef cap',
        "Impressionist art portrait of lidong": 'impressionist',
        "A photo of lidong holding a bunch of flowers": 'bunch',
        "Photo of lidong in front of Eiffel Tower": 'Eiffel',
    }
    option = st.selectbox('Choose the prompt!', sorted(set(QueryToClass)))
    dir_name = os.path.join("./assets/lidong/result", QueryToClass[option])
    dir = os.listdir(dir_name)
    column = st.columns(4)
    for i,filename in enumerate(dir):    
        column[i%4].image(os.path.join(dir_name, filename))
else:
    username = "lidong"
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
        
    
    user_input = st.text_input('Add some prompts! (use \'I\', \'me\', \'lidong\' to represent lidong)','A photo of me wearing sunglasses')
    user_input = lidong_trans_prompt(user_input)
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