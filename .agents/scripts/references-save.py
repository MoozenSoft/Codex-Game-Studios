"""保存用户明确提供的参考图片文件，不读取任何客户端私有会话目录。"""
import argparse
from pathlib import Path
import sys


def main():
    parser=argparse.ArgumentParser(description='保存 Codex 工具实际提供的本地参考图片路径。')
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--file',type=Path,action='append',default=[])
    parser.add_argument('paste_numbers',nargs='*')
    args=parser.parse_args()
    if not args.file:
        print('not_assessed\t当前工具未提供图片文件路径；请提供可读取的图片文件，不能从粘贴编号推测路径。')
        return 3
    root=args.root.resolve()
    if not root.is_dir():
        print('not_assessed\t项目根目录不存在')
        return 3
    refs=root/'references'
    status=0
    for index,source in enumerate(args.file,1):
        source=source if source.is_absolute() else root/source
        if not source.is_file():
            print(f'missing\t{index}')
            status=4
            continue
        data=source.read_bytes()
        if data.startswith(b'\x89PNG\r\n\x1a\n'): ext='png'
        elif data.startswith(b'\xff\xd8\xff'): ext='jpg'
        elif data.startswith((b'GIF87a',b'GIF89a')): ext='gif'
        elif data.startswith(b'RIFF') and data[8:12]==b'WEBP': ext='webp'
        else:
            print(f'missing\t{index}\t不是支持的参考图片格式')
            status=4
            continue
        refs.mkdir(exist_ok=True)
        same=next((p for p in refs.iterdir() if p.is_file() and p.read_bytes()==data),None)
        if same:
            print(f'kept\t{same.relative_to(root).as_posix()}\t{index}')
            continue
        number=1
        while list(refs.glob(f'pasted-{number}.*')):
            number+=1
        target=refs/f'pasted-{number}.{ext}'
        with target.open('xb') as stream:
            stream.write(data)
        print(f'saved\t{target.relative_to(root).as_posix()}\t{index}')
    return status


if __name__=='__main__':
    sys.exit(main())
