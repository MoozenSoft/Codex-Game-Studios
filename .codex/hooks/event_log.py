"""跨进程串行追加最少事件记录，避免 Windows 的追加位置竞争。"""
from contextlib import contextmanager
from datetime import datetime,timezone
import hashlib
import json
import os
import time


@contextmanager
def locked(path):
    with path.open('a+b') as handle:
        if os.name=='nt':
            import msvcrt
            if handle.tell()==0:
                handle.write(b'0');handle.flush()
            def acquire():
                handle.seek(0);msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
            def release():
                handle.seek(0);msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)
        else:
            import fcntl
            def acquire():fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
            def release():fcntl.flock(handle.fileno(),fcntl.LOCK_UN)
        deadline=time.monotonic()+2
        while True:
            try:
                acquire();break
            except OSError:
                if time.monotonic()>=deadline:raise
                time.sleep(0.01)
        try:yield
        finally:release()


def append_event(root,event):
    logs=root/'production/session-logs'
    if not logs.resolve().is_relative_to(root):raise OSError('事件日志路径位于项目之外')
    logs.mkdir(parents=True,exist_ok=True)
    name=event['hook_event_name']
    with locked(logs/'.events.lock'):
        marker=None
        if event.get('tool_use_id'):
            seen=logs/'seen';seen.mkdir(exist_ok=True)
            key=':'.join((str(event.get('session_id','')),name,str(event['tool_use_id'])))
            marker=seen/hashlib.sha256(key.encode()).hexdigest()
            if marker.exists():return
        payload=json.dumps({'time':datetime.now(timezone.utc).isoformat(),'event':name,'tool':event.get('tool_name'),'tool_use_id':event.get('tool_use_id')},ensure_ascii=False)+'\n'
        with (logs/'codex-events.jsonl').open('ab') as output:
            output.write(payload.encode('utf-8'))
        # 持锁期间先完成追加，再发布去重标记；失败时仍允许事件重试。
        if marker:marker.touch(exist_ok=False)
