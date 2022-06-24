import argparse
import os
from PIL import Image, ImageDraw
from tqdm import tqdm

from datasets import load_dataset


def insert_newline(text, cols, rows):
    output = ''
    for i in range(rows):
        start = i * cols
        output += text[start:start + cols] + '\n'
    return output


def main():
    parser = argparse.ArgumentParser(description="Text-to-Image generator")
    parser.add_argument("--output_dir",
                        type=str,
                        required=True,
                        help="Path to the output directory")
    parser.add_argument("--img_size",
                        type=int,
                        default=224,
                        help="Size of the image, assumed squared")
    parser.add_argument("--columns",
                        type=int,
                        default=37,
                        help="Number of columns of char in image")
    parser.add_argument("--rows",
                        type=int,
                        default=15,
                        help="Number of row of chars in image")

    args = parser.parse_args()

    output_folder = os.path.join(args.output_dir)
    os.makedirs(output_folder, exist_ok=True)

    # variables
    backgroud_color = 'white'
    text_color = 'black'
    sequence_length = args.columns * args.rows

    dataset = load_dataset("wikipedia", "20220301.simple")
    for t, (data) in enumerate(tqdm(dataset['train'])):
        text = data['text'].replace('\n', '')
        chunks = [
            insert_newline(text[i:i + sequence_length], args.columns,
                           args.rows)
            for i in range(0, len(text), sequence_length)
        ]
        for i in range(len(chunks)):
            image_name = f"{data['title'].lower()}_{i}.png"
            img = Image.new('RGB', (args.img_size, args.img_size),
                            backgroud_color)
            d = ImageDraw.Draw(img)
            d.text((0, 0), chunks[i], fill=text_color)
            img.save(os.path.join(args.output_dir, image_name))
        break


if __name__ == '__main__':
    main()