# Test model for Koch Robot's on-wrist Camera

12/07/2024

Tony Wang

> Here is 9 typical images from @Edward's litte robot.
> 
> I tested 2 foundation models: Depth-Pro and DINO-X.
> 
> I also tested iPhone SE 2022 camera.
> 
> Please check the folder for more details.

## Depth-Pro: 

- **Minimum Depth:** The smallest recorded depth across all cameras ranges from approximately \(209.21 \, \text{m}\) to \(259.53 \, \text{m}\).
- **Maximum Depth:** The largest recorded depth across all cameras varies significantly, from \(593.51 \, \text{m}\) to \(851.93 \, \text{m}\).
- **Mean Depth:** The average depth values for all images are fairly consistent, ranging from \(331.82 \, \text{m}\) to \(433.94 \, \text{m}\).

![depth](./depth/DA-1.png)

can not validate as their is no GT

![depth](./depth/DA-2.png)

---

## DINO-X
- prompt-free mode 

https://deepdataspace.com/playground/dino-x

### example and my idea
1. many objects
![1](./depth/depth_colored_12-07_1.jpg.png)
![1](./DINOX/1.jpg)

2. reflective pc surface
![1](./depth/depth_colored_12-07_3.jpg.png)
![1](./DINOX/3.jpg)

3. keyboard (clear)
![1](./depth/depth_colored_12-07_4.jpg.png)
![1](./DINOX/4.jpg)

3. keyboard (unclear)
![1](./depth/depth_colored_12-07_6.jpg.png)
![1](./DINOX/4.jpg)

4. white paper
![1](./depth/depth_colored_12-07_8.jpg.png)
![1](./DINOX/7.jpg)


## iPhone SE 2022 Result

Summary of Depth Statistics:
- Minimum Depth Range: 264.03m to 570.01m
- Maximum Depth Range: 1099.27m to 2549.09m
- Mean Depth Range: 532.19m to 1109.28m


1. 10cm level from koch robot
![1](./phone_depth/depth_colored_12-07_1.png)
![1](./phone_DINOX/1.jpg)

2. 30cm level from objects
![2](./phone_depth/depth_colored_12-07_2.png)
![2](./phone_DINOX/2.jpg)

3. Looking at objects at eye level
![3](./phone_depth/depth_colored_12-07_3.png)
![3](./phone_DINOX/3.jpg)

4. 50cm level from objects
![4](./phone_depth/depth_colored_12-07_4.png)
![4](./phone_DINOX/4.jpg)

5. very close to objects
![5](./phone_depth/depth_colored_12-07_5.png)
![5](./phone_DINOX/5.jpg)

max depth is incorrect

## Conclusion

Currently, the depth image by Koch Robot's on-wrist camera is not as good as phone or realsense's. 

Relative depth is very good, but metric depth is yet to be tested.

But I think it is still useful for very close manipulation task.

Hope this can help research in our lab, I am glad to further test on it.


