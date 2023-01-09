# for finetuning the whole dreambooth model to get better results, you could refer to this training script
export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export INSTANCE_DIR="./instance"        # enter your instance dir here
export CLASS_DIR="./class"              # enter your class dir here
export OUTPUT_DIR="./out"               # enter your output dir here

accelerate launch train_dreambooth.py \
  --pretrained_model_name_or_path=$MODEL_NAME  \
  --train_text_encoder \
  --instance_data_dir=$INSTANCE_DIR \
  --class_data_dir=$CLASS_DIR \
  --output_dir=$OUTPUT_DIR \
  --with_prior_preservation --prior_loss_weight=1.0 \
  --instance_prompt="a photo of #4*js! man" \
  --class_prompt="a photo of man" \
  --resolution=512 \
  --train_batch_size=1 \
  --use_8bit_adam \
  --gradient_checkpointing \
  --learning_rate=1e-6 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --num_class_images=200 \
  --max_train_steps=1200  \

# for human face, set learning_rate to 1e-6 and max_train_steps to 1200 seems good
# for common objects, set learning_rate to 2e-6 or 1e-6 and max_train_steps to 400 seems good (be careful of overfitting)