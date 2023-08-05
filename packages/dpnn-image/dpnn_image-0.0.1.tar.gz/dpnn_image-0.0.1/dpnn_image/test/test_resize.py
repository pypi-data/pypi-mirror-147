import shutil
import sys
sys.path.append('/mnt/ys/project/pybind11-cuda/build')

import dpnn_image
import numpy as np
import cv2
import os
from time import time
from glob import glob
from tqdm import tqdm


def test(img_path):
    basename = os.path.basename(img_path).split('.')[0]
    img_origin = cv2.imread(img_path)
    dst_h = 736
    dst_w = 1280
    runs = 1
    
    t_cuda = 0
    t_cpu = 0
    # for i in tqdm(range(runs)):
    for i in range(runs):
        # cuda resize
        t = cv2.getTickCount()
        img_resized_cuda = dpnn_image.bilinear_resize(
            img_origin, 
            img_origin.shape[0], img_origin.shape[1], dst_h, dst_w, img_origin.shape[2]).reshape((dst_h, dst_w, 3))
        t_cuda += (cv2.getTickCount() - t ) / cv2.getTickFrequency() * 1000
        
        # cpu resize
        t = cv2.getTickCount()
        img_resized_cpu = cv2.resize(img_origin, (dst_w, dst_h), 0, 0, cv2.INTER_LINEAR)
        t_cpu += (cv2.getTickCount() - t ) / cv2.getTickFrequency() * 1000
        
    print(f'TIME(ms): cuda={t_cuda}, cpu={t_cpu}')
    
    # check three channel
    save_dir_cuda = './resize_result/cuda'
    os.makedirs(save_dir_cuda, exist_ok=True)
    save_dir_cpu = './resize_result/cpu'
    os.makedirs(save_dir_cpu, exist_ok=True)
    cv2.imwrite(os.path.join(save_dir_cuda, f'{basename}_{img_origin.shape[1]}x{img_origin.shape[0]}_{dst_w}x{dst_h}_cuda.png'), img_resized_cuda)
    cv2.imwrite(os.path.join(save_dir_cpu, f'{basename}_{img_origin.shape[1]}x{img_origin.shape[0]}_{dst_w}x{dst_h}_cpu.png'), img_resized_cpu)
    
    max_error_b = np.max(np.abs(img_resized_cuda[:,:,0].astype(np.int64) - img_resized_cpu[:,:,0].astype(np.int64)))
    max_error_g = np.max(np.abs(img_resized_cuda[:,:,1].astype(np.int64) - img_resized_cpu[:,:,1].astype(np.int64)))
    max_error_r = np.max(np.abs(img_resized_cuda[:,:,2].astype(np.int64) - img_resized_cpu[:,:,2].astype(np.int64)))
    print(f'max_error_b={max_error_b}, max_error_g={max_error_g}, max_error_r={max_error_r}')
    assert(max_error_b<2 and max_error_g<2 and max_error_r <2)


if __name__ == '__main__':
    print(f'{help(dpnn_image)}')
    
    # img_path = sys.argv[1]
    # test(img_path)
    
    img_dir = sys.argv[1]
    for img_path in glob(os.path.join(img_dir, '*')):
        test(img_path)
    