import pdfplumber
import pandas as pd
import os
from PyPDF2 import PdfReader


def main(args):
    output_table_dir = os.path.join(os.getcwd(), args.outputdir, os.path.splitext(args.filename)[0], 'image')
    output_image_dir = os.path.join(os.getcwd(), args.outputdir, os.path.splitext(args.filename)[0], 'table')
    if not os.path.exists(output_table_dir):
        os.makedirs(output_table_dir)
    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)

    pdf =  pdfplumber.open(args.inputpath + args.filename)
    # 表格提取
    for page_idx, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        if tables is not None:
            for table_idx, table in enumerate(tables):
                table_path = args.outputdir + '/' + os.path.splitext(args.filename)[0] + '/' + 'table' + '/page{}_{}.csv'.format(page_idx + 1, table_idx + 1)
                pd.DataFrame(table[1:],columns=table[0]).to_csv(table_path)
    
    # 图片提取
    reader = PdfReader(args.inputpath + args.filename)
    for page_idx, page in enumerate(reader.pages):
        for image in page.images:
            image_path = args.outputdir + '/' + os.path.splitext(args.filename)[0] + '/' + 'image' + '/page{}_{}'.format(page_idx + 1, image.name)
            with open(image_path, "wb") as fp:
                fp.write(image.data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Extract images and tables from pdf')

    parser.add_argument('--inputpath', default='data/input/', help='input dir')
    parser.add_argument('--filename', default='test1.pdf', help='filename')
    parser.add_argument('--outputdir', default='data/output', help='output dir')

    args = parser.parse_args()
    main(args)

