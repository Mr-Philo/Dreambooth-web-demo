import streamlit as st
import os

st.set_page_config(layout="wide")
st.header("More examples with DreamBooth")

st.header("with Sumi Chauhan")
st.subheader("Training images")
cols1= st.columns(4)
cols1[0].image("./assets/sumit/train/1.jpg")
cols1[1].image("./assets/sumit/train/2.jpg")
cols1[2].image("./assets/sumit/train/3.jpg")
cols1[3].image("./assets/sumit/train/4.jpg")
st.subheader("Results with different prompts: ")
dir = os.listdir("./assets/sumit/result")
for i,filename in enumerate(dir):
    st.subheader(filename)
    sub_dir = os.listdir(os.path.join("./assets/sumit/result", filename))
    column = st.columns(len(sub_dir))
    for i,img in enumerate(sub_dir):
        column[i].image(os.path.join(os.path.join("./assets/sumit/result", filename, img)))
            
st.header("with more people")
option = st.selectbox(
    "choose the prompt",
    ('beach', 'oil painting', 'chef cap', 'sunflower'))

cols = st.columns([2,1,6])
cols[0].subheader("train")
cols[2].subheader("prompt: \"{}\"".format(option))

for i in range(10):
    dir_name = "./assets/more people/{:0>3}".format(i+1)
    dir = os.listdir(dir_name)
        
    cols = st.columns([2,1,2,2,2])
    with cols[0]:
        st.image(os.path.join(dir_name, "{:0>3}.jpg".format(i+1)))
    sub_dir_name = os.path.join(dir_name, option)
    sub_dir = sorted(os.listdir(sub_dir_name))
    for i, filename in enumerate(sub_dir):
        cols[i+2].image(os.path.join(sub_dir_name, filename))
        
st.header("with car brands")
dir_name = "./assets/cars"
dir = sorted(os.listdir(dir_name))
for i, filename in enumerate(dir):
    
    st.subheader(filename)
    view_train = st.checkbox('View train images', key=i)
        
    if view_train:
        train_dir_name = os.path.join("./assets/cars-train", filename)
        train_dir = sorted(os.listdir(train_dir_name))
        cols = st.columns(5)
        for j, name in enumerate(train_dir):
            cols[j].image(os.path.join(train_dir_name, name))
    
    cols = st.columns(8)
    out_dir_name = os.path.join("./assets/cars", filename)
    out_dir = sorted(os.listdir(out_dir_name))
    for j, name in enumerate(out_dir):
        cols[j].image(os.path.join(out_dir_name, name))
