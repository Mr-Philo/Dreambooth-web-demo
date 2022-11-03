import streamlit as st
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import os

st.set_page_config(layout="wide")
st.title("Now it's your time! First you need to train a model of your own:")

# Create user's own file
st.header("Please input your unique USER NAME, so you could reuse your model next time~")
username = st.text_input('Input your username:', value="default")
user_root_dir = os.path.join("./Users",username)
if not os.path.exists(user_root_dir):
    os.makedirs(user_root_dir)

# Receive user's uploaded images for training
st.header("Please upload 3-5 photos of a certain person:")
uploaded_files = st.file_uploader(
    "Choose some pictures",
    type=['png','jpg'],
    accept_multiple_files=True)
user_train_dir = os.path.join(user_root_dir, "train")
if not os.path.exists(user_train_dir):
    os.makedirs(user_train_dir)
for i,uploaded_file in enumerate(uploaded_files):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    # st.image(opencv_image, channels="BGR")
    cv2.imwrite(os.path.join(user_train_dir, username+"_{:0>3}.png".format(i+1)), opencv_image)
    
# Show all the training images
st.header("Your traning images are listed here:")
train_dir = os.listdir(user_train_dir)
column = st.columns(len(train_dir) if len(train_dir)<=5 and len(train_dir)>0 else 5)
for i,pth in enumerate(train_dir):
    column[i%5].image(os.path.join(user_train_dir, pth))
    
# Indicate the specific class    
st.header("Please choose the type of this person:")
option = st.selectbox(
    "Note: You could only upload human photos at present",
    ('boy', 'girl', 'young man', 'young woman', 'man', 'woman', 'old man', 'old woman'))

user_train_prompt = "a photo of #4*js! {}".format(option)      #! [V] here
user_class_prompt = "a photo of {}".format(option)
user_class_dir = os.path.join("./class-images", option)
print("Slected class name: {}".format(option))

# When the button is clicked, start training
st.header("When all prepared, click here to train. It'll take a little time ~")
if st.button('Train', key=0):
    user_model_dir = os.path.join(user_root_dir, "model")
    if os.path.exists(user_model_dir):
        # TODO
        st.write("Model dir already exists, Retraining...")
        # st.write("Note: Model has already exists. Do you want to retrain it?")
        # st.write("If you don't, go straight forward to 'Create your own'!")
        # if st.button('Retrain', key=1):
        #     1
    else:
        os.makedirs(user_model_dir)
    st.write("Now we are going to train")
    
    os.system('''
            accelerate launch train_dreambooth.py \
            --pretrained_model_name_or_path="{}"  \
            --train_text_encoder \
            --instance_data_dir="{}" \
            --class_data_dir="{}" \
            --output_dir="{}" \
            --with_prior_preservation --prior_loss_weight=1.0 \
            --instance_prompt="{}" \
            --class_prompt="{}" \
            --resolution=512 \
            --train_batch_size=1 \
            --gradient_checkpointing \
            --learning_rate=2e-6 \
            --lr_scheduler="constant" \
            --lr_warmup_steps=0 \
            --num_class_images=200 \
            --max_train_steps=1200  \
              '''.format(
                    "CompVis/stable-diffusion-v1-4",
                    user_train_dir,
                    user_class_dir, 
                    user_model_dir, 
                    user_train_prompt,
                    user_class_prompt))
    
    st.write("Finished!")
