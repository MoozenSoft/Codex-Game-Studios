// 用 Node 的原生模块解释器执行生成代码，不依赖 Vite 或外部测试包。
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

const context=vm.createContext({console});
context.window=context;
// 用同一全局上下文模拟浏览器执行经典script，模块绑定仍由原生解释器处理。
context.document={
  createElement(tag){
    if(tag!=='script') throw new Error(`unsupported test element: ${tag}`);
    return {textContent:'',remove(){}};
  },
  head:{appendChild(script){vm.runInContext(script.textContent,context);return script;}},
};
const modules=new Map();
async function load(file) {
  file=resolve(file);
  if(modules.has(file)) return modules.get(file);
  let module;
  if(file.endsWith('.json')) {
    const data=JSON.parse(readFileSync(file,'utf8'));
    module=new vm.SyntheticModule(['default'],function(){this.setExport('default',data);},{context,identifier:file});
  } else {
    module=new vm.SourceTextModule(readFileSync(file,'utf8'),{
      context,identifier:file,initializeImportMeta(meta){meta.env={DEV:false};},
    });
  }
  modules.set(file,module);
  await module.link((specifier,referrer)=>load(resolve(dirname(referrer.identifier),specifier)));
  return module;
}
await(await load(process.argv[2])).evaluate();
console.log(JSON.stringify(context.growObservation));
