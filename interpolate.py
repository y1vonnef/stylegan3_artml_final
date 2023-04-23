# Imports
import torch
import pickle
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import PIL.Image
from tqdm import tqdm
import os

# load Spout library
from Library.Spout import Spout

# Set Device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load Model
import sys
sys.path.append("stylegan3")

path = "stylegan3-t-ffhq-1024x1024.pkl"
with open(path, 'rb') as f:
    G = pickle.load(f)['G_ema'].to(device)

## Helper Functions

# Generate images given a latent code
def generate_image_from_z(z):
  c = None # class labels (not used in this example)
  images = G(z, c) # NCHW, float32, dynamic range [-1, +1], no truncation
  images = (images.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
  return images

# Generate images given a random seed
def generate_image_random(seed):
  z = torch.from_numpy(np.random.RandomState(seed).randn(1, G.z_dim)).to(device)
  
  label = torch.zeros([1, G.c_dim], device=device)

  img = G(z, label)
  img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
  
  return img, z

# Interpolate between latent codes
def linear_interpolate(z1, z2, alpha):
  return z1 * alpha + z2 * (1 - alpha)

# Generate Interpolated Image
def generate_interpolation(z1, z2, alpha):
  z_interpolated = linear_interpolate(z1, z2, alpha) 
  images = generate_image_from_z(z_interpolated)
  PIL.Image.fromarray(images[0].cpu().numpy(), 'RGB').save(f'out/interp.png')
  return images[0].cpu().numpy()

# Spout and TD
def main() :
    # create spout object
    spout = Spout(silent = False)
    # create receiver
    #spout.createReceiver('input')
    # create sender
    spout.createSender('output')

    img1,z1=generate_image_random(1056)
    img2,z2=generate_image_random(2245)
    i = 0
    while True and i<5 :
        img=generate_interpolation(z1,z2,0.5+i*0.5)
        # check on close window
        spout.check()
        # receive data
        #data = spout.receive()
        # send data
        spout.send(img)
        i=i+0.1

if __name__ == "__main__":
  main()
