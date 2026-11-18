"""真实 Chrome 验证 grow 配置在经典 script 与模块之间保留绑定。"""
import functools
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.result = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'pre' and dict(attrs).get('id') == 'result':
            self.active = True

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.active = False

    def handle_data(self, data):
        if self.active:
            self.result += data


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class GrowConfigBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = os.environ.get('CGS_TEST_BROWSER')
        cls.bash = os.environ.get('CGS_TEST_BASH')
        if not cls.browser or not cls.bash:
            raise unittest.SkipTest('未评估：需显式指定已安装的 CGS_TEST_BROWSER 和 CGS_TEST_BASH')

    def test_generated_config_keeps_classic_bindings_in_chrome(self):
        (ROOT / '.scratch').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='grow-scope-', dir=ROOT / '.scratch') as temporary:
            project = Path(temporary)
            game = project / 'prototypes/fish'
            game.mkdir(parents=True)
            (game / 'config.js').write_text(
                'window.CONFIG={duration:{value:30,min:10,max:90,step:5}};\n'
                'var ART={color:"purple"}; let BONUS=2; const OFFSET=3;\n'
                'function nextDuration(){return CONFIG.duration.value+BONUS+OFFSET;}\n', encoding='utf-8')
            (game / 'index.html').write_text(
                '<!doctype html>\n<title>fish</title>\n<script src="config.js"></script>\n'
                '<script>\nwindow.growObservation={color:ART.color};\n</script>\n', encoding='utf-8')
            copied = subprocess.run(
                [self.bash, str(ROOT / '.agents/scripts/one-shot-grow.sh'), 'copy', 'fish', '--root', str(project)],
                cwd=project, capture_output=True, text=True, encoding='utf-8', timeout=40)
            self.assertEqual(copied.returncode, 0, copied.stderr)
            (project / 'scope-probe.html').write_text('''<!doctype html><pre id="result">PENDING</pre>
<script>window.addEventListener('error', e => {
 document.getElementById('result').textContent=JSON.stringify({error:e.message});
});</script>
<script type="module">
import './src/config-source.js';
document.getElementById('result').textContent=JSON.stringify({
 color:ART.color,bonus:BONUS,offset:OFFSET,extra:nextDuration()
});
</script>''', encoding='utf-8')
            handler = functools.partial(QuietHandler, directory=str(project))
            with ThreadingHTTPServer(('127.0.0.1', 0), handler) as server:
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    browser = subprocess.run([
                        self.browser, '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
                        f'--user-data-dir={project / "browser-profile"}', '--virtual-time-budget=1000', '--dump-dom',
                        f'http://127.0.0.1:{server.server_port}/scope-probe.html',
                    ], capture_output=True, text=True, encoding='utf-8', timeout=35)
                finally:
                    server.shutdown()
                    thread.join(timeout=5)
            self.assertEqual(browser.returncode, 0, browser.stderr)
            parser = ResultParser()
            parser.feed(browser.stdout)
            self.assertEqual(json.loads(parser.result), {'color':'purple', 'bonus':2, 'offset':3, 'extra':35})


if __name__ == '__main__':
    unittest.main()
