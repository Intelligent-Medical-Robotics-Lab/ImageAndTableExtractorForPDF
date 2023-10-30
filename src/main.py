import fitz, os, io
from PIL import Image


def main(args):
    print(os.getcwd())
    filename = os.path.join(os.getcwd(), args.inputpath, args.filename)
    print(filename)
    # open file
    with fitz.Document(filename) as my_pdf_file:
        # 遍历所有页面
        for page_number in range(1, len(my_pdf_file) + 1):

            # 查看独立页面
            page = my_pdf_file[page_number - 1]

            # 查看当前页所有图片
            images = page.get_images()

            # 查看是否有图片
            if images:
                print(f"There are {len(images)} image/s on page number {page_number}[+]")
            else:
                print(f"There are No image/s on page number {page_number}[!]")

            # 遍历当前页面所有图片
            for image_number, image in enumerate(page.get_images(), start=1):
                # 访问图片xref
                xref_value = image[0]

                # 提取图片信息
                base_image = my_pdf_file.extract_image(xref_value)

                # 访问图片
                image_bytes = base_image["image"]

                # 获取图片扩展名
                ext = base_image["ext"]

                # 加载图片
                image = Image.open(io.BytesIO(image_bytes))

                # 保存图片
                image_name = f"Page{page_number}Image{image_number}.{ext}"
                output_dir = os.path.join(args.outputdir, args.filename[:-4])
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)

                im_path = os.path.join(args.outputdir, args.filename[:-4], image_name)
                image.save(open(im_path, "wb"))
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Extract images from pdf')

    parser.add_argument('--inputpath', default='data/input/', help='input dir')
    parser.add_argument('--filename', default='test2.pdf', help='filename')
    parser.add_argument('--outputdir', default='data/output', help='output dir')

    args = parser.parse_args()
    main(args)

