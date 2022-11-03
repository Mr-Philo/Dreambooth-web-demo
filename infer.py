from torch import autocast
from diffusers import StableDiffusionPipeline
import torch
import argparse
import os
import time
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, help="path-to-your-trained-model")
parser.add_argument("--prompt", type=str, default="A photo of sks dog in a bucket")
parser.add_argument("--seed", type=int, default=1024)
parser.add_argument("--rows", type=int, default=1)
parser.add_argument("--cols", type=int, default=1)
parser.add_argument("--save_name", type=str)
parser.add_argument("--save_path", type=str, default="./out_imgs")
parser.add_argument("--skip_grid", action='store_true')
parser.add_argument("--skip_single", action='store_true')
opt = parser.parse_args()
    
def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

# os related preparation
model_id = opt.model
prompt = opt.prompt
if not os.path.exists(opt.save_path):
    os.makedirs(opt.save_path)
if not opt.skip_grid:
    if not os.path.exists(os.path.join(opt.save_path, "grid")):
        os.makedirs(os.path.join(opt.save_path, "grid"))
# uuid_str = time.strftime("%Y-%m-%d %H-%M-%S",time.localtime())
tmpstr = prompt.replace("#4*js!", "V")
save_name = os.path.join(opt.save_path,opt.save_name) if opt.save_name else os.path.join(opt.save_path, "grid", "seed{}_".format(opt.seed)+tmpstr+'.png')
latest_path = os.path.join(opt.save_path, "latest.png")
    
# Diffusion model preparation
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
generator = torch.Generator("cuda").manual_seed(opt.seed)

# Generation
num_images = opt.rows*opt.cols
if num_images == 1:
    with autocast("cuda"):
        image = pipe(prompt, num_inference_steps=100, guidance_scale=7.5, generator=generator).images[0]
    image.save(save_name)
    image.save(latest_path)
else:
    prompt = [prompt] * num_images
    with autocast("cuda"):
        images = pipe(prompt, num_inference_steps=100, guidance_scale=7.5, generator=generator).images
    if not opt.skip_grid:
        grid = image_grid(images, rows=opt.rows, cols=opt.cols)
        grid.save(save_name)
        grid.save(latest_path)
    if not opt.skip_single:
        if not os.path.exists(os.path.join(opt.save_path, tmpstr)):
            os.makedirs(os.path.join(opt.save_path, tmpstr))
        for i, img in enumerate(images):
            img.save(os.path.join(opt.save_path, tmpstr, "seed{}_{:0>3}.png".format(opt.seed, i)))
