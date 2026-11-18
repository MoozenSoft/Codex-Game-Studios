"""浏览器回归：导入模式应驱动真实循环，而不是把游戏停在手动模式。"""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]

class ImportRunnerBrowserTests(unittest.TestCase):
    def run_game(self,native):
        with tempfile.TemporaryDirectory(prefix='import-browser-') as temp:
            root=Path(temp);game=root/'prototypes/sample';game.mkdir(parents=True)
            code='''<!doctype html><html><body style="margin:0;background:black"><canvas id="c" width="1280" height="720"></canvas>
<script>
const canvas=document.getElementById('c'),ctx=canvas.getContext('2d');let ticks=0;
function resize(){canvas.width=innerWidth;canvas.height=innerHeight;}addEventListener('resize',resize);resize();
function draw(){ctx.fillStyle='#194f83';ctx.fillRect(0,0,1280,720);ctx.fillStyle='#ffd45a';ctx.fillRect(100+ticks%20,100,240,180);}
function frame(){ticks++;draw();requestAnimationFrame(frame);}
NATIVE_HOOK
if(!NATIVE || new URLSearchParams(location.search).get('manual')!=='1')requestAnimationFrame(frame);
else draw();
</script></body></html>'''
            hook="window.game={get scene(){return 'play'},get state(){return {ticks}},press(){},hold(){},step(n=1,paint=true){ticks+=n;if(paint)draw();}};" if native else ''
            code=code.replace('NATIVE_HOOK',hook).replace('NATIVE','true' if native else 'false')
            (game/'index.html').write_text(code,encoding='utf-8')
            env=dict(os.environ);env['CGS_PYTHON']=sys.executable
            browser=env.get('CGS_TEST_BROWSER')
            self.assertTrue(browser,'浏览器回归须显式提供CGS_TEST_BROWSER，不把缺环境算通过')
            env['PAGE_SHOT_BROWSER']=browser
            bash=env.get('CGS_TEST_BASH') or shutil.which('bash')
            result=subprocess.run([bash,str(ROOT/'.agents/scripts/one-shot-run.sh'),'prototypes/sample',str(root/'out.png'),'--hookless','--log','Enter wait:0.2','--stop','30','--root',str(root)],cwd=root,env=env,capture_output=True,text=True,encoding='utf-8',timeout=60)
            self.assertEqual(result.returncode,0,result.stderr+'\n'+result.stdout)
            screens=[line.split('\t') for line in result.stdout.splitlines() if line.startswith('screen\t')]
            self.assertTrue(screens,result.stdout)
            self.assertEqual(screens[-1][4],'drawn',result.stdout)
            self.assertTrue((root/'out.png').is_file())

    def test_import_with_existing_manual_hook_still_draws(self):self.run_game(True)
    def test_import_without_hook_still_draws(self):self.run_game(False)

if __name__=='__main__':unittest.main()
