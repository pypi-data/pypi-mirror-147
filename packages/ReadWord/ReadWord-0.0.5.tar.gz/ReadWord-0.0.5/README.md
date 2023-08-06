# readword
快速读取docx文档数据

## 安装(install)
```pycon
pip install readword
```

## 使用(use)：
### 1. 实例化RW类并填入docx文档路径
### 2. 创建工作台
### 3. 退出RW工作台，销毁缓存数据

## 使用示例：

```pycon
from ReadWord.readword import RW


# 实例化RW并传入docx文档路径
rw = RW(r'docxpath\file.docx')
# 创建工作台
rw.create_workspace()
# 保存所有png图片
rw.save_all_picture(r'C:\Desktop\test')
# 按照文档结构，获取文档内容和段落类型
rw.get_style_position()
# 退出RW工作台
rw.exit()
```