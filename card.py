#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
身份证扫描件水印添加工具
为身份证图片添加安全水印
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

def add_watermark(input_path, output_path=None, watermark_text="仅供xxx使用，他用无效", rotate_ccw=True):
    """
    为图片添加水印
    
    参数:
        input_path: 输入图片路径
        output_path: 输出图片路径（如果为None，则在原文件名后加_watermark）
        watermark_text: 水印文字
        rotate_ccw: 是否逆时针旋转90度
    """
    try:
        # 打开原始图片
        img = Image.open(input_path)
        
        # 逆时针旋转90度（如果需要）
        if rotate_ccw:
            img = img.rotate(90, expand=True)
        
        # 转换为RGBA模式以支持透明度
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 创建一个透明图层用于绘制水印
        watermark_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)
        
        # 设置字体大小（更小的字体）
        font_size = int(min(img.size) / 25)
        
        # 尝试使用系统字体
        try:
            # Windows/Linux/Mac 常见中文字体路径
            font_paths = [
                '/System/Library/Fonts/PingFang.ttc',  # Mac
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',  # Linux
                'C:\\Windows\\Fonts\\msyh.ttc',  # Windows 微软雅黑
                'C:\\Windows\\Fonts\\simhei.ttf',  # Windows 黑体
            ]
            
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    break
            
            if font is None:
                font = ImageFont.load_default()
                print("警告: 未找到中文字体，使用默认字体")
        except:
            font = ImageFont.load_default()
            print("警告: 字体加载失败，使用默认字体")
        
        # 计算文字大小
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 设置水印样式
        opacity = 128  # 透明度 (0-255)，提高清晰度
        angle = -30  # 旋转角度
        spacing_x = text_width + 80  # 水平间距（稍微密集一些）
        spacing_y = text_height + 120  # 垂直间距
        
        # 在整个图片上重复绘制水印
        for y in range(-text_height, img.height + text_height, spacing_y):
            for x in range(-text_width, img.width + text_width, spacing_x):
                # 创建单个水印文字
                txt_img = Image.new('RGBA', (text_width + 20, text_height + 20), (0, 0, 0, 0))
                txt_draw = ImageDraw.Draw(txt_img)
                txt_draw.text((10, 10), watermark_text, fill=(255, 0, 0, opacity), font=font)
                
                # 旋转水印
                txt_img = txt_img.rotate(angle, expand=True)
                
                # 粘贴到水印层
                watermark_layer.paste(txt_img, (x, y), txt_img)
        
        # 合并原图和水印层
        watermarked = Image.alpha_composite(img, watermark_layer)
        
        # 转换回RGB模式以便保存为JPEG
        watermarked = watermarked.convert('RGB')
        
        # 确定输出路径
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_watermark{ext}"
        
        # 保存图片（高质量）
        watermarked.save(output_path, quality=98, dpi=(300, 300))
        print(f"✓ 水印添加成功！")
        print(f"  输入文件: {input_path}")
        print(f"  输出文件: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        return None

def main():
    """主函数"""
    print("=" * 50)
    print("身份证扫描件水印添加工具")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("\n使用方法:")
        print(f"  python {sys.argv[0]} <图片路径>")
        print(f"  python {sys.argv[0]} <图片路径> <输出路径>")
        print("\n示例:")
        print(f"  python {sys.argv[0]} id_card.jpg")
        print(f"  python {sys.argv[0]} id_card.jpg id_card_with_watermark.jpg")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_path):
        print(f"✗ 错误: 文件不存在 '{input_path}'")
        return
    
    # 添加水印
    result = add_watermark(
        input_path, 
        output_path,
        watermark_text="仅供xxx使用，他用无效"
    )
    
    if result:
        print("\n✓ 处理完成！")

if __name__ == "__main__":
    main()