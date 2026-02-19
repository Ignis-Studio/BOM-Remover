import os
import chardet


def remove_bom(file_path):
    """
    先检测是否为 UTF-8 编码，再移除 BOM。
    :return: Boolean (True 表示修改了文件，False 表示跳过)
    """
    bom = b'\xef\xbb\xbf'

    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        if not content.startswith(bom):
            return False

        result = chardet.detect(content)
        encoding = result['encoding']
        confidence = result['confidence']

        is_utf8 = encoding and encoding.lower().startswith('utf-8')

        if is_utf8 and confidence > 0.7:
            new_content = content[3:]

            with open(file_path, 'wb') as f:
                f.write(new_content)
            return True
        else:
            print(f"Warning: skipped one file which does have BOM but is likely not a text file{file_path} [detected encoding: {encoding}]")
            return False

    except Exception as e:
        print(f"ERROR: Error while reading file: {file_path}: \n{e}")
        return False


def process_directory(directory):
    if not os.path.exists(directory):
        print(f"FATAL: Cannot find the specified directory: '{directory}'")
        return

    count = 0
    print(f"Scanning directory: {directory} ...\n")

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith(('.jpg', 'png', 'gif', '.webp', 'avif', 'mp4', 'mp3', 'avi', 'mov', 'dll', 'exe')):
               continue

            if remove_bom(file_path):
                print(f"BOM removed: {file_path}")
                count += 1

    print(f"\nDone. {count} files' BOM were removed.")


if __name__ == "__main__":
    target_folder = input("Enter the directory path to remove BOM files: \n>").strip()
    target_folder = target_folder.strip('"').strip("'")

    process_directory(target_folder)