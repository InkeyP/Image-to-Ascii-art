from PIL import Image

# 定义字符集
# ASCII_CHARS = "@%#++=@%%@"
ASCII_CHARS = "█▓▒░"

# 将像素值转换为字符
def pixel_to_char(pixel):
    # 获取亮度，增加红色和绿色通道的权重
    r, g, b = pixel
    brightness = (0.299 * r + 0.587 * g + 0.114 * b)
    # 将亮度映射到字符
    return ASCII_CHARS[int(brightness * len(ASCII_CHARS) // 256)]

# 获取Linux Shell颜色代码
def get_color_code(pixel):
    r, g, b = pixel
    # 计算ANSI颜色代码
    return f"\033[38;2;{r};{g};{b}m"

# 将图像转换为字符画
def image_to_ascii(image_path):
    # 打开并缩放图像
    img = Image.open(image_path)
    img = img.convert("RGB")
    img = img.resize((100, 50))  # 你可以调整大小
    pixels = img.load()
    
    ascii_image = ""
    
    for y in range(img.height):
        for x in range(img.width):
            char = pixel_to_char(pixels[x, y])
            color_code = get_color_code(pixels[x, y])
            ascii_image += f"{color_code}{char}\033[0m"  # 颜色 + 字符 + 重置
        ascii_image += "\n"
    
    return ascii_image

def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def generate_c_code(output_path, ascii_art_lines, max_line_length=80):
    """
    根据字符画内容生成C代码，并输出到指定文件，处理换行符。
    """
    with open(output_path, 'w', encoding='utf-8') as c_file:
        # 写入C文件的头部
        c_file.write('#include <stdio.h>\n\n')
        c_file.write('int main() {\n')

        # 逐行处理字符画内容，切分并生成多个 printf 语句
        for line in ascii_art_lines:
            # 将每行中的特殊字符进行转义，尤其是双引号和百分号
            escaped_line = line.replace('%', '%%').replace('"', '\\"').rstrip()

            # 对每行进行分割，防止太长的行导致编译错误
            for i in range(0, len(escaped_line), max_line_length):
                part = escaped_line[i:i+max_line_length]
                c_file.write(f'    printf("{part}");\n')

            # 每行结束后添加一个换行符 printf("\n");
            c_file.write('    printf("\\n");\n')

        # 结束C文件的main函数
        c_file.write('    return 0;\n')
        c_file.write('}\n')
    print(ascii_art)

if __name__ == "__main__":
    image_path = input("输入图像文件名：")
    ascii_art = image_to_ascii(image_path)
    with open('pic.txt', 'wb') as f:
        f.write(ascii_art.encode())
        print("成功输出字符画到pic.txt")
    
        # 读取字符画所在的txt文件
    input_file = 'pic.txt'  # 确保pic.txt中包含已经生成的字符画
    ascii_art_lines = read_txt_file(input_file)

    # 生成C语言文件
    output_c_file = 'pic.c'
    generate_c_code(output_c_file, ascii_art_lines)

    print(f'C文件已生成：{output_c_file}')


