import xml.etree.ElementTree as ET

def get_xml_label(path):
    # 读取XML文件
    tree = ET.parse(path)
    root = tree.getroot()
    
    # 获取图像宽度和高度
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    
    content = {}
    # 遍历所有的对象（即目标）
    for obj in root.iter('object'):
        # 获取目标类别和边界框坐标
        cls = obj.find('name').text
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)
        
        w = xmax-xmin
        h = ymax-ymin


        content[cls] = (xmin,ymin,w,h)
    
    return (width,height),content
        # 打印结果
        # print('Class:', cls)
        # print('Bounding Box:', xmin, ymin, xmax, ymax)