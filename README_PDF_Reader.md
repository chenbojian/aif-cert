# PDF文本提取工具

这是一个用Python编写的PDF文本提取工具，可以从PDF文件中读取文字内容。

## 功能特点

- 支持多页PDF文件
- 自动检测文件格式
- 逐页提取文本内容
- 可选择将提取的文本保存到文件
- 支持中文路径和内容

## 安装依赖

在运行脚本之前，需要先安装PyPDF2库：

```bash
pip install PyPDF2
```

或者使用requirements.txt文件：

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法1：命令行参数

```bash
python pdf_reader.py your_pdf_file.pdf
```

### 方法2：交互式输入

```bash
python pdf_reader.py
```

然后按提示输入PDF文件路径。

## 使用示例

```bash
# 安装依赖
pip install PyPDF2

# 运行脚本
python pdf_reader.py document.pdf
```

## 输出说明

- 脚本会显示PDF的总页数
- 逐页提取文本内容
- 如果某页没有可提取的文本，会提示该页没有内容
- 可以选择将提取的文本保存到同名的.txt文件中

## 注意事项

1. 确保PDF文件存在且可访问
2. 某些PDF文件可能包含扫描图像，这种情况下无法提取文本
3. 提取的文本质量取决于PDF文件的格式和内容类型
4. 支持中文PDF文件

## 故障排除

如果遇到问题：

1. 确保已正确安装PyPDF2库
2. 检查PDF文件路径是否正确
3. 确认PDF文件没有损坏
4. 对于扫描版PDF，可能需要使用OCR工具

## 扩展功能

如果需要处理扫描版PDF，可以考虑使用以下库：
- `pytesseract` - OCR文字识别
- `pdf2image` - 将PDF转换为图像
- `Pillow` - 图像处理 