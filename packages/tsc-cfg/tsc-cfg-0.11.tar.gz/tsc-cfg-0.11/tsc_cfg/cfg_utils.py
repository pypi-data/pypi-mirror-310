from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent, FileSystemMovedEvent
import importlib
import atexit
import os
import yaml
from typing import Optional, Any, Dict, List, Union, Callable
import threading
import logging
from types import ModuleType
from copy import deepcopy
from .py_static_cfg import Cfg


class ReloadCfgHandler(FileSystemEventHandler):
    def __init__(
        self,
        module: ModuleType,
        delay: float = 3, 
        logger: Optional[logging.Logger] = None,
    ):
        """重新加载模块

        Args:
            module (ModuleType): 重新加载的模块, Cfg 类所在的模块
            delay (float, optional): 防止频繁修改的延迟，可能导致修改后还要再保存一次来触发 on_modified, 单位秒
            logger (Optional[logging.Logger], optional): 日志记录器, 否则使用 print
        """
        self.module = module
        self.delay = delay
        self.logger = logger
        self._timers: Dict[str, threading.Timer] = {}
        self._yaml_handlers: Dict[str, ReloadYamlHandler] = {}
        self._observer = Observer()
        self._observer.schedule(self, path=os.path.dirname(module.__file__), recursive=False)
        self._observer.start()
        atexit.register(self.stop)

    def reset_timer(self, path, opt):
        if path in self._timers:
            self._timers[path].cancel()  # 取消已存在的定时器
        self._timers[path] = threading.Timer(self.delay, self.process_event, [path, opt])
        self._timers[path].start()

    def process_event(self, path: str, opt: str):
        try:
            importlib.reload(self.module)
            if self.logger and opt:
                self.logger.info(f"Cfg {self.module.__name__} reloaded ({opt})")
            else:
                print(f"Cfg {self.module.__name__} reloaded ({opt})")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reloading cfg ({opt}): {e}")
            else:
                print(f"Error reloading cfg ({opt}): {e}")
        finally:
            self._timers.pop(path, None)
        for handler in self._yaml_handlers.values():
            handler.load_all('')

    def on_modified(self, event: FileSystemEvent):
        if event.src_path == self.module.__file__:
            self.reset_timer(event.src_path, 'modified')
    
    def stop(self):
        self._observer.stop()
        for timer in self._timers.values():
            timer.cancel()
        self._timers.clear()
        for handler in self._yaml_handlers.values():
            handler.stop()
        self._yaml_handlers.clear()
    
    def add_yaml(
        self,
        *paths: str,
        delay: Optional[float] = None,
        logger: Optional[logging.Logger] = None,
        load_all_each_time: bool = False,
        **kwargs,
    ) -> 'ReloadCfgHandler':
        """添加监听的yaml文件夹或文件路径

        Args:
            *paths (str): 监听的yaml文件夹或文件路径
                配置文件的文件名必须以 .yaml 结尾，不能以 . 开头
                yaml 的 key 必须符合变量名的命名规范, 不能是任意的字符串, 否则转成普通对象或报错
                重复的 key 后面更新的会覆盖前面
            delay (float, optional): 延迟处理时间, 单位秒
            logger (Optional[logging.Logger], optional): 日志记录器, 否则使用 print
            load_all_each_time (bool): 每次有任何更新都重新加载所有 py/yaml 文件，防止yaml中的删除配置不生效, 但可能更新多次
            **kwargs (Any): 传递给 ReloadYamlHandler 的其他参数

        Returns:
            ReloadCfgHandler: 返回自身
        """
        if load_all_each_time:
            kwargs['cfg_update_func'] = lambda: self.process_event('yaml', 'by_yaml')
        for p in paths:
            p = os.path.normpath(p)
            if p in self._yaml_handlers:
                continue
            self._yaml_handlers[p] = ReloadYamlHandler(
                module=self.module,
                path=p,
                delay=delay or self.delay,
                logger=logger or self.logger,
                **kwargs,
            )
        return self
    
    def del_yaml(self, *paths: str) -> 'ReloadCfgHandler':
        """删除监听的yaml文件夹或文件路径

        Args:
            *paths (str): 监听的yaml文件夹或文件路径

        Returns:
            ReloadCfgHandler: 返回自身
        """
        for p in paths:
            p = os.path.normpath(p)
            handler = self._yaml_handlers.pop(p, None)
            if handler:
                handler.stop()
        self.process_event('self.module.__name__', 'del_yaml')
        return self
    
    @property
    def yaml_paths(self) -> List[str]:
        """返回监听的yaml文件夹或文件路径"""
        return list(self._yaml_handlers)


class ReloadYamlHandler(FileSystemEventHandler):
    def __init__(
        self,
        module: ModuleType,
        path: str,
        delay: float = 3, 
        logger: Optional[logging.Logger] = None,
        create_path: bool = True,
        limit_value_type: bool = True,
        allow_new_key: bool = True,
        cfg_update_func: Optional[Callable[..., None]] = None,
    ):
        """延迟处理文件变化事件，使用多线程实现延迟，不适合大量文件变化

        Args:
            module (ModuleType): 重新加载的模块, Cfg 类所在的模块
            path (str): 监听的yaml文件夹或文件路径
                配置文件的文件名必须以 .yaml 结尾，不能以 . 开头
                yaml 的 key 必须符合变量名的命名规范, 不能是任意的字符串, 否则转成普通对象或报错
                重复的 key 后面更新的会覆盖前面
            delay (float, optional): 延迟处理时间, 单位秒
            logger (Optional[logging.Logger], optional): 日志记录器, 否则使用 print
            create_path (bool, optional): 是否创建不存在的路径, 防止文件不存在报错
                后缀名为 .yaml 则创建文件，否则创建文件夹
            limit_value_type (bool, optional): 限制值的类型, 除 None 以外不允许 yaml 的 value 类型和配置类不同
            allow_new_key (bool, optional): 允许新的 key, 不在配置类中的 key 也会加入配置类
        """
        if create_path and not os.path.exists(path):
            if path.endswith('.yaml'):
                if os.path.sep in path:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write('')
            else:
                os.makedirs(path, exist_ok=True)
        self.module = module
        self.logger = logger
        self.path = path
        self.delay = delay
        self.limit_value_type = limit_value_type
        self.allow_new_key = allow_new_key
        self.cfg_update_func = cfg_update_func
        self._timers: Dict[str, threading.Timer] = {}  # 用字典存储文件和对应的定时器
        self.load_all()
        self._observer = Observer()
        self._observer.schedule(self, path=self.path, recursive=True)
        self._observer.start()
        atexit.register(self.stop)

    def reset_timer(self, path, opt):
        if path in self._timers:
            self._timers[path].cancel()  # 取消已存在的定时器
        self._timers[path] = threading.Timer(self.delay, self.warp_process_event, [path, opt])
        self._timers[path].start()
    
    def warp_process_event(self, path: str, opt: str):
        if self.cfg_update_func is None:
            self.process_event(path, opt)
        else:
            self.cfg_update_func()
            if opt:
                if self.logger:
                    self.logger.info(f"Reloaded by cfg yaml ({opt}) {path}")
                else:
                    print(f"Reloaded by cfg yaml ({opt}) {path}")
    
    @staticmethod
    def old_define(old: Any, new: Any) -> bool:
        if (  # 要求 old 和 new 都是 None 或者类型相同, 不然可能改变类型
            old is None or
            new is None or
            type(old) == type(new) or
            isinstance(old, (set, tuple)) and isinstance(new, list)
        ):
            return True
        raise TypeError(f"Cfg type mismatch: {type(old)} != {type(new)}, old={str(old)}, new={str(new)}")
    
    @staticmethod
    def direct_assign_func(key: Union[str, int], old: Any, new: Any) -> Any:
        if isinstance(old, (set, tuple)) and isinstance(new, list):
            return type(old)(new)
        return deepcopy(new)
    
    def load_all(self, opt: str = 'init'):
        if os.path.isdir(self.path):
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    if not self.yaml_check(file):
                        continue
                    path = os.path.join(root, file)
                    self.process_event(path, opt)
        else:
            assert self.yaml_check(self.path), f"Path must be a yaml file, but got {self.path}"
            self.process_event(self.path, opt)

    def process_event(self, path: str, opt: str):
        try:
            with open(path, 'r',encoding='utf-8') as f:
                config = yaml.safe_load(f.read())
                if config is None:
                    config = {}
                assert isinstance(config, dict), f"Config must be a dict, but got {type(config)}"
            update_flag = False
            for k, v in config.items():
                if not hasattr(self.module, k):
                    continue
                vv = getattr(self.module, k)
                if hasattr(vv, '_set_'):
                    vv: Cfg
                    vv._set_(
                        key=None,
                        value=v,
                        cover_old=self.limit_value_type,
                        old_define=self.old_define,
                        create_new=self.allow_new_key,
                        direct_assign_func=self.direct_assign_func,
                    )
                setattr(self.module, k, vv)
                update_flag = True
            if update_flag and opt:
                if self.logger:
                    self.logger.info(f"Reloaded cfg yaml ({opt}) {path}")
                else:
                    print(f"Reloaded cfg yaml ({opt}) {path}")
        except BaseException as e:
            if self.logger:
                self.logger.error(f"ReloadYamlHandler error {opt} ({path}): {e}")
            else:
                print(f"ReloadYamlHandler error {opt} ({path}): {e}")
        finally:
            self._timers.pop(path, None)

    def on_modified(self, event: FileSystemEvent):
        if event.is_directory or not self.yaml_check(event.src_path):
            return
        self.reset_timer(event.src_path, 'modified')

    def on_created(self, event: FileSystemEvent):
        if event.is_directory or not self.yaml_check(event.src_path):
            return
        self.reset_timer(event.src_path, 'created')

    def on_moved(self, event: FileSystemMovedEvent):
        if event.is_directory or not self.yaml_check(event.dest_path):
            return
        self.reset_timer(event.dest_path, 'created')
    
    @staticmethod
    def yaml_check(path: str) -> bool:
        if not path.endswith('.yaml') or path[0] == '.':
            return False
        return True
    
    def stop(self):
        self._observer.stop()
        for timer in self._timers.values():
            timer.cancel()
        self._timers.clear()


ALL_CFG_HANDLERS: Dict[str, ReloadCfgHandler] = {}


def get_cfg_handler(module: ModuleType, **kwargs) -> ReloadCfgHandler:
    if module.__file__ in ALL_CFG_HANDLERS:
        return ALL_CFG_HANDLERS[module.__file__]
    else:
        handler = ReloadCfgHandler(module, **kwargs)
        ALL_CFG_HANDLERS[module.__file__] = handler
        return handler


def module_model_dump(module: ModuleType, **kwargs) -> dict:
    """将模块的配置类整体转成字典

    Args:
        module (ModuleType): 模块
        **kwargs: 传递给 Cfg.model_dump 的参数

    Returns:
        dict: 返回结果
    """
    dump = {}
    for k, v in module.__dict__.items():
        if Cfg._is_config_class_(v):
            v: Cfg
            dump[k] = v.model_dump(**kwargs)
    return dump


def module_model_dump_code(module: ModuleType, **kwargs) -> Union[str, list]:
    """将模块的配置类整体转成字典的代码

    Args:
        module (ModuleType): 模块
        **kwargs: 传递给 Cfg.model_dump 的参数

    Returns:
        str: 返回结果
    """
    dump = []
    for k, v in module.__dict__.items():
        if Cfg._is_config_class_(v):
            v: Cfg
            dump.append(v.model_dump_code(**kwargs))
    if dump and isinstance(dump[0], list):
        return sum(dump, [])
    else:
        return '\n\n'.join(dump)
