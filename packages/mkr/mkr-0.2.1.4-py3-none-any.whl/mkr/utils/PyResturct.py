# -*- coding: utf-8 -*-
import re
import os
import sys  # 打印python解释器位置
from importlib.util import find_spec
from mkr.utils.PackOS import BiasPath


class PyFile:
    def __init__(self, root: str, file_path: str, encoding='utf-8'):
        # 安全性检查
        bp = BiasPath(root, "")
        dp = BiasPath(file_path, "")
        assert bp.isdir(), "target path must be a dir, not : " + str(bp)
        assert bp.isabs(), "target path must be a abspath, not : " + str(bp)
        assert dp.isfile(), "target path must be a file, not : " + str(dp)
        assert dp.isabs(), "target path must be a abspath, not : " + str(dp)
        assert str(dp)[-3:].lower() == '.py', "target path must be a pyfile, not : " + str(dp)

        # 初始化
        self.root = root
        self.rel = []
        self.fname = os.path.basename(file_path)[:-3]
        self._raw_fpath = file_path
        self.encoding = encoding

        path = os.path.dirname(file_path)
        if root != path:
            while 1:
                _dir, _name = os.path.dirname(path), os.path.basename(path)
                self.rel.insert(0, _name)
                if _dir and _name:
                    if _dir == root:
                        break
                else:
                    raise Exception(f"no path union: root: {root}, path: {path}")
                path = _dir

    def read(self):
        try:
            return open(self._raw_fpath, 'r', encoding='UTF-8').read()
        except UnicodeDecodeError as err:
            raise Exception(f"Unicode Error: <file:{self._raw_fpath}>\n{err}")

    def write(self, txt: str):
        try:
            return open(self._raw_fpath, 'w', encoding=self.encoding).write(txt)
        except UnicodeDecodeError as err:
            raise Exception(f"Unicode Error: <file:{self._raw_fpath}>\n{err}")

    def __str__(self):
        rels = "-"
        for rel in self.rel:
            rels += f"{rel}."
        rels = rels[:-1]
        txt = f"PyFile: {self.fname}{rels}"
        return txt


class ImportSegment:
    ORDa = ord('a')
    ORDz = ord('z')
    ORDA = ord('A')
    ORDZ = ord('Z')
    FROMPATTERN = '[^\n\s:]*from[\s\w.]*import.+\n'  # --*--
    IMPPATTERN = '[^\n\s:]*import.+\n'  # --*--
    FKEYNAME = "$<restruct>:"
    FKEYPATTERN = rf'\{FKEYNAME}\d+'  # --*--

    # --*--
    _from_replaces, _from_id = {}, 0

    @staticmethod
    def release():
        ImportSegment._from_replaces, ImportSegment._from_id = {}, 0

    @property
    def _id(self):
        ImportSegment._from_id += 1
        return ImportSegment._from_id - 1

    @property
    def _frep(self):
        return ImportSegment._from_replaces

    # --*-- /

    def __init__(self, segment: str, preix: str):
        self.seg = segment
        self.pre = preix

    @staticmethod
    def replace(match, preix):
        """
        负责对:
            from ... import xxx
            import xxx
        进行响应的函数
        返回对应的替换值
        :param match:
        :param preix:
        :return:
        """
        if isinstance(match, str):
            seg = match
        else:
            seg = match.group()[:-1]  # 去掉\n

        ret = ""
        if '\n' in seg:
            for s in seg.split('\n'):
                if s:
                    ret += '\n' + ImportSegment.replace(s, preix)
            return ret

        imp_seg = ImportSegment(seg, preix)

        if imp_seg.isfrom:
            _id = str(imp_seg._id)
            key, value = imp_seg.FKEYNAME + _id, imp_seg.solution()
            imp_seg._frep[_id] = value
            ret = key + '\n'
        else:
            ret = imp_seg.solution()

        # print('>>seg: ', seg, "; -- isfrom: ", imp_seg.isfrom, ":: answer is: ", ret)
        return ret

    @staticmethod
    def secReplace(match):
        """
        负责对:
            $<restruct>:xxx
        进行响应的函数
        返回对应的替换值
        :param match:
        :return:
        """
        # print("dict:", ImportSegment._from_replaces)
        seg = match.group()
        index = seg.find(':')
        _id = seg[index + 1:]
        if _id.isdigit():
            value = ImportSegment._from_replaces.get(_id)
            if value:
                return value
        print(f"failed to import with {seg}")
        return f"raise ImportError('Failed to import from raw key: {seg}')"

    @property
    def prestr(self):
        if hasattr(self, '_prestr'): return self._prestr
        ret, i = '', 0
        while 1:
            if 127 == ord(self.seg[i]) <= 31: break
            ret += self.seg[i]
            i += 1
        self._prestr = ret
        return ret

    @property
    def isfrom(self):
        if hasattr(self, '_isfrom'): return self._isfrom
        index = self.seg.find('from')
        if index != -1:  # 仍有可能为 import fromlib这样的可能
            for i in range(0, index):
                if self.ORDA < ord(self.seg[i]) < self.ORDz:
                    self._isfrom = False
                    return
            self._isfrom = True
        else:
            self._isfrom = False
        return self._isfrom

    @property
    def afterimport(self):
        if hasattr(self, '_afterimport'): return self._afterimport
        if self.isfrom:
            self._afterimport = None  # from xxx import 后面的东西已经不重要了
        else:
            self._afterimport = self.seg[self.importpos + 6:] if self.importpos else None
        return self._afterimport

    @property
    def importpos(self):
        if hasattr(self, '_importpos'): return self._importpos
        if self.isfrom:
            match = re.search('\simport\s', self.seg)
            self._importpos = match.span()[0] if match else None
        else:
            index = self.seg.find('import')
            self._importpos = index if index != -1 else None
        return self._importpos

    @property
    def frompos(self):
        if hasattr(self, '_frompos'): return self._frompos
        index = self.seg.find('from')
        self._frompos = index if self.isfrom and index != -1 else None
        return self._frompos

    def newName(self, module: str, pre: str) -> str:
        """
        获取一个module的新名称
        :param module: 模块名称
        :param pre: 模块新前缀(不能有空白字符)
        :return: str
        """
        try:
            __import__(module)
            return module
        except ImportError:
            pre = pre if pre[-1] == '.' else pre + '.'
            return pre + module

    def solution(self):
        """
        为这个导入片段制定解决方案
        执行解决方案时需要暂时在sys.path中移除当前目录
        :return:
        """
        if self.isfrom:  # from 模式
            module = re.sub('\s', '', self.seg[self.frompos + 4: self.importpos])
            return f"{self.seg[:self.frompos + 4]} {self.newName(module, self.pre)} {self.seg[self.importpos:]}\n"
        else:  # import 模式
            left, right = self.seg[:self.importpos + 6], ''
            for piece in self.seg[self.importpos + 6:].split(','):
                if not piece: continue
                if piece.find('*') != -1:
                    right += f"{piece}, "
                    continue
                match = re.search('\sas\s', piece)
                index = match.span()[0] if match else len(piece) + 1
                module = re.sub('\s', '', piece[:index])
                _new_ = self.newName(module, self.pre)
                right += f"{_new_} {piece[index:]}, "
                # import 本地库 没有as是非常危险的
                if _new_ != module and match is None:
                    print(f"Warning: Dangerous import: '{self.seg}'. Using 'from xxx import ...' or 'import xxx as ...' is a better choice.")

            if right: right = right[:-2]
            return f"{left} {right}\n"


class ResourceSegment:
    """
    假设mod只能使用相对路径来引用资源

    """
    RESPATTERN = 'rf?[\"\'].+[\"\']'

    def __init__(self, segment: str, preix: str):
        self.seg = segment
        self.pre = preix

    @staticmethod
    def replace(match, preix):
        """

        :param match:
        :param preix:
        :return:
        """
        seg = match.group()
        # print('seg is ', seg)
        res_seg = ResourceSegment(seg, preix)
        return res_seg.solution()

    def solution(self):
        """
        为这个导入片段制定解决方案
        :return:
        """
        if self.seg[1] == 'f':
            index = 3
        else:
            index = 2

        if self.seg[index] == '\\':
            if self.pre[-1] == '\\': self.pre = self.pre[:-1]
        else:
            if self.pre[-1] != '\\': self.pre = self.pre + '\\'

        ret = f"{self.seg[:index]}{self.pre}{self.seg[index:]}"
        return ret


def removeLongInterpret(pycode):
    pycode = '\n' + pycode
    pycode = re.sub('\n\s*[\"\'][\"\'][\"\']', '\n\"\"\"', pycode)
    # 去除"""
    index = pycode.find('"""')
    while index != -1 and not (index != 0 and pycode[index - 1] != '\n'):  # 对于a = ”“”“”“这种不做处理
        next = pycode[index + 3:].find('"""')
        if next == -1:
            raise Exception('""" does not closed. at:\n\n' + pycode[index - 100:index + 100] + "...")
        pycode = pycode[:index] + '\n' + pycode[index + next + 6:]
        index = pycode.find('"""')

    # 去除'''
    index = pycode.find("'''")
    while index != -1 and not (index != 0 and pycode[index - 1] != '\n'):
        next = pycode[index + 3:].find("'''")
        if next == -1:
            raise Exception("''' does not closed. at:\n\n" + pycode[index - 100:index + 100] + "...")
        pycode = pycode[:index] + '\n' + pycode[index + next + 6:]
        index = pycode.find("'''")
    return pycode


def PyRestruct(mod_path: str, new_path: str, run_path: str = None, encoding: str = 'utf-8', debug=False):
    """
    python代码(关于import路径和资源路径)的重构
    将目标mod移动到当前目录下的
    :param mod_path: abs path. 目标mod根目录
    :param new_path: abs path. 目标mod的新目录
    :param run_path: abs path. 执行处的目录。该目录必须是new_path的一部分
                _: None  will use os.getcwd()
    :param encoding: 解析文件时使用的编码
                _: utf-8d
    NOTE: these three path must under same disk segment.
    :return:
    """
    run_path = os.getcwd() if run_path is None else run_path

    # 检索目录是否正常
    assert os.path.exists(run_path), "run_path must be a exist path. Path: " + run_path
    assert os.path.isabs(run_path), "run_path must be a abspath. not " + run_path
    assert os.path.isdir(run_path), "run_path must be a dirpath. not " + run_path
    assert os.path.exists(mod_path), "mod_path must be a exist path. Path: " + mod_path
    assert os.path.isabs(mod_path), "mod_path must be a abspath. not " + mod_path
    assert os.path.isdir(mod_path), "mod_path must be a dirpath. not " + mod_path
    assert os.path.exists(new_path), "new mod_path must be a exist path. Path: " + new_path
    assert os.path.isabs(new_path), "new mod_path must be a abspath. not " + new_path
    assert os.path.isdir(new_path), "new mod_path must be a dirpath. not " + new_path

    # 预处理
    rel = os.path.relpath(new_path, run_path)  # 新目录相对运行目录的路径
    imp_pre = ''  # 一个以.作为分隔符的pypath
    for piece in rel.split('\\'):
        if piece:
            imp_pre += piece + '.'
    res_pre = os.path.relpath(mod_path, run_path)  # 旧目录相对运行目录的路径

    # find py files:
    pyfiles = []  # PyFile
    for root, dirs, files in os.walk(new_path):
        for file in files:
            if file[-3:].lower() == '.py':
                path = os.path.join(root, file)
                pyfiles += [PyFile(new_path, path, encoding)]

    # restruct body
    sys.path.remove(os.getcwd())
    ImportSegment.release()
    for py in pyfiles:
        pycode = py.read()
        pycode = pycode.replace('\n', '\n\n')  # 稀疏化
        pycode = re.sub('#.*\n', '\n', pycode)  # 去注释#
        pycode = removeLongInterpret(pycode)  # 去注释""" """
        pycode = re.sub(ImportSegment.FROMPATTERN, lambda match: ImportSegment.replace(match, imp_pre), pycode)     # from import segment
        pycode = re.sub(ImportSegment.FROMPATTERN, lambda match: ImportSegment.replace(match, imp_pre), pycode)     # from import segment
        pycode = re.sub(ImportSegment.IMPPATTERN, lambda match: ImportSegment.replace(match, imp_pre), pycode)      # import segment
        pycode = re.sub(ImportSegment.FKEYPATTERN, ImportSegment.secReplace, pycode)                                # $<restruct> segment
        pycode = re.sub(ResourceSegment.RESPATTERN, lambda match: ResourceSegment.replace(match, res_pre), pycode)  # resource segment
        pycode = pycode.replace('\n\n', '\n')  # 反稀疏化
        if debug:
            print(pycode)
        else:
            py.write(pycode)
    sys.path.append(os.getcwd())


if __name__ == '__main__':
    mkpath = os.path.join(os.getcwd(), 'mktemp/test')
    PyRestruct(r'E:\Python\Python310\Lib\site-packages\mkr\test\test', mkpath, debug=True)
