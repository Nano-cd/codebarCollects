# 导入所需工具包
import csv
import os
import time
from pyzbar import pyzbar
import argparse
import cv2

start_time = time.time()
data_path = 'p1'
folderlist = os.listdir(data_path)


Z1 = []
Z2 = []
csv_path = 'labels/predicted.csv'
RS = [["名字", "码型", "编码"]]
cnt = 0
for i in folderlist:
    img_path = os.path.join(data_path, i)
    # 加载输入图像
    image = cv2.imread(img_path)
    # 找到图像中的条形码并进行解码
    barcodes = pyzbar.decode(image)
    # 循环检测到的条形码
    for barcode in barcodes:
        # 提取条形码的边界框的位置
        # 画出图像中条形码的边界框
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # 条形码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # 绘出图像上条形码的数据和条形码类型
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

        # 向终端打印条形码数据和条形码类型
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        # 展示输出图像
        RS.append([i, barcodeType, barcodeData])
        # cv2.imshow("Image", image)
        cv2.imwrite('results/'+i,image)
        cnt=cnt+1
        # cv2.waitKey(0)

end_time = time.time()

print((end_time-start_time)/cnt)

# 打开一个新的文件用于写入，如果文件已存在则覆盖
with open(csv_path, 'w', newline='', encoding='utf-8') as file:
    # 创建一个csv.writer对象
    writer = csv.writer(file)

    # 遍历列表并写入每一行
    for row in RS:
        writer.writerow(row)

print("CSV文件已生成。")
