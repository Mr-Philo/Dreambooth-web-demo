import enum
from fileinput import filename
import streamlit as st
import os

st.set_page_config(layout="wide")
st.title("Welcome to DreamBooth")

st.subheader("With Dreambooth, you could UPLOAD your photos and GET stylized head portrait !!!")
st.header("Step 1: Choose the training images:")
option = st.selectbox("Choose the example person",('Bill gates','Sumit Chauhan', 'ruizhe(author)'))

if option == 'Bill gates':
    cols1= st.columns(5)
    cols1[0].image("./assets/gates/train/gates1.jpg")
    cols1[1].image("./assets/gates/train/gates2.jpg")
    cols1[2].image("./assets/gates/train/gates3.jpg")
    cols1[3].image("./assets/gates/train/gates4.jpg")
    cols1[4].image("./assets/gates/train/gates5.jpg")

    st.header("Step 2: Waiting for model traning")
    st.header("Step 3: Create your stylized head portrait")
    
    dir = os.listdir("./assets/gates/result")
    for i,filename in enumerate(dir):
        st.subheader(filename)
        sub_dir = os.listdir(os.path.join("./assets/gates/result", filename))
        column = st.columns(len(sub_dir))
        for i,img in enumerate(sub_dir):
            column[i].image(os.path.join(os.path.join("./assets/gates/result", filename, img)))
            
elif option == 'Sumit Chauhan':
    cols1= st.columns(5)
    cols1[0].image("./assets/sumit/train/1.jpg")
    cols1[1].image("./assets/sumit/train/2.png")
    cols1[2].image("./assets/sumit/train/3.jpg")
    cols1[3].image("./assets/sumit/train/4.jpg")
    cols1[4].image("./assets/sumit/train/5.png")
    cols1[0].image("./assets/sumit/train/6.png")
    cols1[1].image("./assets/sumit/train/7.png")
    cols1[2].image("./assets/sumit/train/8.png")
    cols1[3].image("./assets/sumit/train/9.png")
    cols1[4].image("./assets/sumit/train/10.png")

    st.header("Step 2: Waiting for model traning")
    st.header("Step 3: Create your stylized head portrait")
    
    dir = os.listdir("./assets/sumit/result")
    for i,filename in enumerate(dir):
        st.subheader(filename)
        sub_dir = os.listdir(os.path.join("./assets/sumit/result", filename))
        column = st.columns(len(sub_dir))
        for i,img in enumerate(sub_dir):
            column[i].image(os.path.join(os.path.join("./assets/sumit/result", filename, img)))
            
elif option == 'ruizhe(author)':
    cols1= st.columns(5)
    cols1[0].image("./assets/ruizhe/train/ruizhe1.jpg")
    cols1[1].image("./assets/ruizhe/train/ruizhe2.jpg")
    cols1[2].image("./assets/ruizhe/train/ruizhe3.jpg")
    cols1[3].image("./assets/ruizhe/train/ruizhe4.jpg")
    cols1[4].image("./assets/ruizhe/train/ruizhe5.jpg")

    st.header("Step 2: Waiting for model traning")
    st.header("Step 3: Create your stylized head portrait")
    
    dir = os.listdir("./assets/ruizhe/result")
    for i,filename in enumerate(dir):
        st.subheader(filename)
        sub_dir = os.listdir(os.path.join("./assets/ruizhe/result", filename))
        column = st.columns(len(sub_dir))
        for i,img in enumerate(sub_dir):
            column[i].image(os.path.join(os.path.join("./assets/ruizhe/result", filename, img)))
