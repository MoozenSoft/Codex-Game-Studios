"""从 Codex 的可选模型目录解析指定家族的最高正式版本。"""
import argparse
import json
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time


MODEL_ID = re.compile(r'gpt-(\d+(?:\.\d+)*)-(astra|sol)')
REFRESH_FAILURE = re.compile(
    r'failed to (?:refresh available models|initialize model catalog|refresh model catalog)',
    re.IGNORECASE,
)


class CatalogError(RuntimeError):
    """模型目录不可用于确认最新版本。"""


def select_model(rows, family):
    candidates = []
    for row in rows:
        if not isinstance(row, dict) or row.get('hidden') is not False:
            continue
        model = row.get('model')
        match = MODEL_ID.fullmatch(model) if isinstance(model, str) else None
        if match and match[2] == family:
            version = tuple(map(int, match[1].split('.')))
            candidates.append((version, model))
    if not candidates:
        raise CatalogError(f'目录没有可见的 GPT {family} 正式版本')
    return max(candidates)[1]


def catalog_page(result):
    if not isinstance(result, dict) or not isinstance(result.get('data'), list):
        raise CatalogError('Codex 模型目录响应格式无效')
    cursor = result.get('nextCursor')
    if cursor is not None and (not isinstance(cursor, str) or not cursor):
        raise CatalogError('Codex 模型目录分页游标无效')
    return result['data'], cursor


def read_catalog(command, provider=None, timeout=25):
    """仅查询 App Server 模型列表，使用同一截止时间读取所有页。"""
    deadline = time.monotonic() + timeout
    messages = queue.Queue()
    with tempfile.TemporaryFile(mode='w+t', encoding='utf-8', errors='replace') as stderr:
        process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
            text=True, encoding='utf-8', errors='replace',
        )

        def read_stdout():
            try:
                for line in process.stdout:
                    messages.put(line)
            finally:
                messages.put(None)

        reader = threading.Thread(target=read_stdout, daemon=True)
        reader.start()

        def send(message):
            process.stdin.write(json.dumps(message) + '\n')
            process.stdin.flush()

        def request(request_id, method, params):
            send({'id': request_id, 'method': method, 'params': params})
            while time.monotonic() < deadline:
                try:
                    line = messages.get(timeout=max(0, deadline - time.monotonic()))
                except queue.Empty:
                    break
                if line is None:
                    raise CatalogError(f'Codex 在返回 {method} 前已退出')
                reply = json.loads(line)
                if isinstance(reply, dict) and reply.get('id') == request_id:
                    if 'error' in reply or 'result' not in reply:
                        raise CatalogError(f'Codex 未能完成 {method} 查询')
                    return reply['result']
            raise CatalogError(f'Codex {method} 查询超时')

        try:
            request(0, 'initialize', {'clientInfo': {'name': 'cgs_model_routing', 'version': '1.0'}})
            send({'method': 'initialized'})
            params = {'includeHidden': False, 'limit': 100}
            if provider:
                params['modelProvider'] = provider
            entries = []
            seen_cursors = set()
            request_id = 1
            while True:
                page, cursor = catalog_page(request(request_id, 'model/list', params))
                entries.extend(page)
                if cursor is None:
                    break
                if cursor in seen_cursors:
                    raise CatalogError('Codex 模型目录分页游标重复')
                seen_cursors.add(cursor)
                params['cursor'] = cursor
                request_id += 1
        finally:
            process.stdin.close()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            reader.join(timeout=1)
            if not reader.is_alive():
                process.stdout.close()

        stderr.seek(0)
        if REFRESH_FAILURE.search(stderr.read()):
            raise CatalogError('Codex 模型目录刷新失败，无法确认回退目录中的最高版本')
        if process.returncode != 0:
            raise CatalogError('Codex 模型目录查询进程异常退出')
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('family', choices=('astra', 'sol'))
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--provider', help='查询 Codex 中已配置的特定模型提供方')
    source.add_argument('--catalog-stdin', action='store_true',
                        help='从标准输入读取当前客户端已经取得的完整 model/list 结果')
    source.add_argument('--available-stdin', action='store_true',
                        help='从标准输入读取当前客户端公开的可选模型 ID 的 JSON 数组')
    args = parser.parse_args()
    try:
        if args.catalog_stdin:
            rows, cursor = catalog_page(json.load(sys.stdin))
            if cursor is not None:
                raise CatalogError('输入的模型目录仍有未读取的页面')
            origin = 'client model/list snapshot'
        elif args.available_stdin:
            ids = json.load(sys.stdin)
            if not isinstance(ids, list) or not all(isinstance(value, str) for value in ids):
                raise CatalogError('输入必须为客户端可选模型 ID 的 JSON 数组')
            rows = [{'model': model, 'hidden': False} for model in ids]
            origin = 'active client advertised model IDs'
        else:
            executable = shutil.which('codex.cmd') or shutil.which('codex')
            if executable is None:
                raise CatalogError('找不到可执行的 Codex CLI')
            rows = read_catalog([executable, 'app-server', '--stdio'], args.provider)
            origin = 'codex app-server model/list'
        result = {'status': 'resolved', 'family': args.family,
                  'model': select_model(rows, args.family), 'source': origin}
    except (CatalogError, OSError, ValueError) as error:
        reason = str(error) if isinstance(error, CatalogError) else '无法读取 Codex 模型目录'
        print(json.dumps({'status': 'not_assessed', 'family': args.family, 'reason': reason}))
        return 2
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
