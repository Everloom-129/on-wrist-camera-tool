import os
import time
import numpy as np
import depth_pro
import torch
import matplotlib.pyplot as plt
def get_torch_device():
    device_name = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\033[95mUsing device: {device_name}\033[0m")
    return torch.device(device_name)

def process_image(image_path, output_dir):
    print(f"Processing image: {image_path}")
    # Set device, default is cpu so very slow
    print("Loading Depth-Pro model...")
    model, transform = depth_pro.create_model_and_transforms(
        device=get_torch_device(),
        precision=torch.half,
    )
    model.eval()

    os.makedirs(output_dir, exist_ok=True)
    
    with torch.no_grad():
        # use prediction fpx, this could be replace with actual data
        image, _, f_px = depth_pro.load_rgb(image_path)
        image = transform(image)
        
        prediction = model.infer(image, f_px=f_px)
        depth = prediction["depth"]
        
        depth_cpu = depth.cpu().numpy() * 1000 # convert from m to mm
        
        # Save depth image
        image_name = os.path.basename(image_path)
        date = time.strftime("%m-%d")
        depth_path = os.path.join(output_dir, f'depth_{date}_{image_name}.npy')
        np.save(depth_path, depth_cpu)
        
        
        # Create subplot with original image and depth visualization
        plt.figure(figsize=(16, 6))
        
        # Plot original image
        plt.subplot(1, 2, 1)
        original_img = plt.imread(image_path)
        plt.imshow(original_img)
        plt.title('Original Image')
        plt.axis('off')
        
        # Plot depth visualization
        plt.subplot(1, 2, 2)
        depth_plot = plt.imshow(depth_cpu, cmap='turbo')
        plt.colorbar(depth_plot, label='Depth (mm)')
        plt.title('Depth Map')
        plt.axis('off')
        
        plt.suptitle(f'Depth-Pro Result for {os.path.basename(image_path)}')
        colored_depth_path = os.path.join(output_dir, f'depth_colored_{date}_{image_name}.png')
        plt.savefig(colored_depth_path, bbox_inches='tight', pad_inches=0)
        plt.close()


        # Create log file in output directory
        log_path = os.path.join(output_dir, 'depth_stats.log')
        with open(log_path, 'a') as f:
            f.write(f"Depth statistics for {image_path}:\n")
            f.write(f"Min depth: {depth_cpu.min():.2f}m\n")
            f.write(f"Max depth: {depth_cpu.max():.2f}m\n")
            f.write(f"Mean depth: {depth_cpu.mean():.2f}m\n")
    print(f"\033[95mProcessing completed. Results saved to:")
    print(f"Depth array: {depth_path}")
    print(f"Colored depth: {colored_depth_path}\033[0m")

if __name__ == "__main__":
    # input_path = "/home/tonyw/VLM/pal_video_tool/ml-depth-pro/data/disp/water-2/rgb/image.png"
    # output_dir = "output"
    # process_image(input_path, output_dir)
    input_dir = "data/Koch_images"
    output_dir = f"output/koch_robot/depth"
    for image_path in os.listdir(input_dir):
        process_image(os.path.join(input_dir, image_path), output_dir)
