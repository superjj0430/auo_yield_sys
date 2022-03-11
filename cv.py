import numpy as np
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
file_name = 'X3'
in_file = r'C:/Users/BarryShih/Desktop/Jupyter/cv/data/{}.jpg'.format(file_name)

in_image_a = Image.open(in_file)

# 橫向統計
img_g = np.array(in_image_a.convert("L"))[10:-10, 10:-10]
img_sum = np.sum(img_g, axis=1)
plt.plot(img_sum)

# 平滑曲線
x = np.arange(0,1180,1)
y = img_sum.tolist()

plt.plot(x,y,color="red",linewidth = '1')

# x_smooth = savgol_filter(y, 101, 3)
smooth_y = savgol_filter(y,229, 3)
    
plt.plot(x,y,color="red",linewidth = '1')
plt.plot(x,smooth_y,color="green",linewidth = '1')
plt.show()

# 找差異區域
up_threshold = np.mean(smooth_y - y) + 1.5*np.std(smooth_y - y)
down_threshold = np.mean(smooth_y - y) - 1.5*np.std(smooth_y - y)
print(np.mean(smooth_y - y))
print(np.std(smooth_y - y))
print(up_threshold)
print(down_threshold)

diff_list = y - smooth_y
diff_point = []
for i in range(len(diff_list)):
    if diff_list[i]>up_threshold or diff_list[i]<down_threshold:
#     if abs(diff_list[i]) < np.mean(smooth_y - y):
        diff_point.append(i)
print(len(diff_point))

x = np.arange(0,1180,1)
y = img_sum.tolist()

plt.plot(x,y,color="red",linewidth = '1')

# # x_smooth = savgol_filter(y, 101, 3)
# smooth_y = savgol_filter(y, 199, 0)

tmp_x = diff_point
tmp_y = []
for i in tmp_x:
    tmp_y.append(y[i]) 
    
plt.plot(x,y,color="red",linewidth = '1')
plt.plot(tmp_x,tmp_y,'.',color="green", linewidth = '0.5')
plt.show()

# 切割出差異區域
tmp = tmp_x[0]
tmp_point = []
for i in range(len(tmp_x)):
    if tmp_x[i] - tmp > 40:
        tmp= tmp_x[i]
        tmp_point.append(tmp_x[i])
print(tmp_point)    
y1 = tmp_point[0]
y2 = tmp_point[-1]
in_image_a.crop((0,y1,1600,y2))
in_image_a.crop((0,y1,1600,y2)).save(file[:-4]+'_cutting.jpg')
