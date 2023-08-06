import re
import json
from string import Formatter
from string import Template
from pprint import pformat
from datetime import datetime
from collections import OrderedDict

K_tpl_args_fmt = "${{args_{}}}"
K_tpl_field_fmt = "${{{}}}"


def format_tpl_args(i):
    # (2) => "${args_2}"
    return K_tpl_args_fmt.format(i)


def format_tpl_field(key):
    # ("name") => "${name}"
    return K_tpl_field_fmt.format(key)


def format_tpl_kwargs(keys):
    return dict((k, format_tpl_field(k)) for k in keys)


class CoJsonEncoder(json.JSONEncoder):
    """
    default support datetime.datetime and uuid.UUID
    enable convert object by custom `http exception`
    usually:
        "to_json":  Common Class
        "to_dict":  Custom Model
        "as_dict"： SQLAlchemy Rows
        "get_json": json response
        "__html__": jinja templates

    """
    _jsonify_methods = [
        "to_json",
        "to_dict",
        "get_json",  # json response
        "as_dict",  # SQLAlchemy Rows
        "toJson",
        "getJson",  # json response
        "toDict",
        "asDict",  # SQLAlchemy Rows
        "__html__",  # jinja templates
    ]

    _jsonify_strict = False
    _pformat_depth = 2

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            for k in self._jsonify_methods:
                fn = getattr(obj, k, None)
                if callable(fn):
                    return fn()
                elif isinstance(fn, (str, int, float, dict)):
                    return fn
        tp = type(obj)
        return "{}::{}".format(tp, obj)

    @classmethod
    def dumps_v2(cls, data, indent=2, ensure_ascii=False, **kwargs):
        return json.dumps(data, cls=cls, indent=indent, ensure_ascii=ensure_ascii, **kwargs)


class CoTextFormatter():
    tpl_text = "{CoTextFormatter}"

    def __init__(self, tpl_text, tpl_args_offset=0, **default_kwargs):
        self.tpl_text = tpl_text
        self._formatter = Formatter()
        self._cofmt()
        self.tpl_args_offset = tpl_args_offset
        self._render_args = self._get_render_args()
        self.default_kwargs = self._get_render_kwargs(**default_kwargs)

    def _cofmt(self):
        self._tpl_args = []
        self._tpl_kwargs = OrderedDict()
        its = self._formatter.parse(self.tpl_text)
        for literal_text, field_name, format_spec, conversion in its:
            if field_name == "":
                self._tpl_args.append((literal_text, format_spec, conversion))
            elif field_name is not None:
                self._tpl_kwargs[field_name] = (literal_text, format_spec, conversion)
        self.tpl_args_count = len(self._tpl_args)

    def _get_render_kwargs(self, **kwargs):
        kws = {}
        for k, it in self._tpl_kwargs.items():
            v = kwargs.get(k, f"${{{k}}}")
            kws[k] = v
        return kws

    def _get_render_args(self):
        # "${{args_{i}}}".format(2)  # => '${args_2}'
        # [self.tpl_args_fmt.format(i=i + tpl_args_offset) for i in range(self.tpl_args_count)]
        return self.get_render_args(self.tpl_args_count, self.tpl_args_offset)

    @classmethod
    def get_render_args(cls, count, offset=0):
        return [format_tpl_args(i=i + offset) for i in range(count)]

    def render(self, tpl_kwargs=None, tpl_args=None,
               tpl_args_offset=0, **extra_kwargs):
        """
        :param _args_num_offset: -1 不显示; 显示 >=0； 
        """
        kws = dict(self.default_kwargs, **extra_kwargs)
        if isinstance(tpl_kwargs, dict):
            kws.update(tpl_kwargs)

        if tpl_args is None:
            args = []
        elif isinstance(tpl_args, (tuple, list)):
            args = tpl_args
        else:
            args = [tpl_args]
        cnt2 = len(args)
        cnt3 = self.tpl_args_count - cnt2
        if tpl_args_offset < 0:
            ps2 = ["${}" for i in range(cnt3)]
        else:
            # ps2 = [f"${{{i + cnt2 + tpl_args_offset}}}" for i in range(cnt3)]
            ps2 = self.get_render_args(cnt3, offset=tpl_args_offset + cnt2)
        ps = [*args, *ps2]
        return self.tpl_text.format(*ps, **kws)

    def raw_template(self):
        tpl_text2 = self.tpl_text.format(*self._render_args, **self.default_kwargs)
        return tpl_text2

    @classmethod
    def render_string(cls, tpl_text, _args_num_offset=-1, **tpl_kws):
        tpl = cls(tpl_text, **tpl_kws)
        return tpl.render(_args_num_offset=_args_num_offset)

    def to_json(self):
        return self.raw_template()

    def __repr__(self):
        m = dict(vars(self), _type=self.__class__.__name__)
        return pformat(m, indent=2)


# class CoTextTemplate(Template):
class CoTextTemplate():
    pattern_str = '\{(.+?)\}'
    idpattern = r'\{(.+?)\}'

    # pattern = re.compile(pattern_str)
    # pattern = pattern_str
    # idpattern = r'(?a:[_a-z][_a-z0-9]*)'

    def __init__(self, template, **kwargs):
        self.tpl_text = template
        self._cofmt()
        self.default_kwargs = kwargs

    @classmethod
    def render_string(cls, tpl_text, **kwargs):
        tpl = cls(tpl_text)
        return tpl.render(**kwargs)

    def render(self, **kwargs):
        kws = dict(self.default_kwargs)
        kws.update(self._tpl_kwargs)
        kws.update(kwargs)
        txt = self.tpl_text
        for k, v in kws.items():
            txt = txt.replace(f"{{{k}}}", v)
        return txt

    def _cofmt(self):
        # "${}${a}${4}" => [('', '', '', ''), ('', '', 'a', ''), ('', '', '', '')]
        self._tpl_args = []
        self._tpl_kwargs = OrderedDict()
        pattern = re.compile(self.idpattern)
        ps = pattern.findall(self.tpl_text)
        for i, p in enumerate(ps):
            if p:
                self._tpl_kwargs[p] = format_tpl_field(p)
            else:
                self._tpl_args.append(i)
        self.tpl_args_count = len(self._tpl_args)
        return self._tpl_args, self._tpl_kwargs


class CoJsonTemplate():
    _max_depth_ = 5
    _CoFormatter = CoTextFormatter
    tpl_text = "${CoJsonTemplate}"
    pformat_json = CoJsonEncoder.dumps_v2

    def __init__(self, tpl_text: str, tpl_kwargs=None,
                 tpl_args_count=0, tpl_args_offset=0,
                 **extra_kwargs):
        self.tpl_text = tpl_text
        self._cofmt()
        kws = {}
        if isinstance(tpl_kwargs, dict):
            kws.update(tpl_kwargs)
        kws.update(**extra_kwargs)
        self.default_kwargs = kws
        self.tpl_args_count = tpl_args_count
        self.tpl_args_offset = tpl_args_offset
        self._rendered_kws = None

    def _get_render_args(self):
        cnt = self.tpl_args_count
        offset = self.tpl_args_offset
        return self._CoFormatter.get_render_args(cnt, offset)

    def _cofmt(self):
        # "${}${a}${4}" => [('', '', '', ''), ('', '', 'a', ''), ('', '', '', '')]
        self._tpl = Template(self.tpl_text)
        self._tpl_args = []
        self._tpl_kwargs = OrderedDict()
        ps4 = re.findall(self._tpl.pattern, self.tpl_text)
        for i, ps in enumerate(ps4):
            if ps[2]:
                self._tpl_kwargs[ps[2]] = ps
            else:
                self._tpl_args.append(ps)
        self.tpl_args_count = len(self._tpl_args)
        return self._tpl_args, self._tpl_kwargs

    @classmethod
    def create(cls, data, _used_delimit=True, **kws):
        if isinstance(data, str):
            return cls.create_from_str(data, _used_delimit=_used_delimit, **kws)
        elif isinstance(data, (list, tuple)):
            return cls.create_from_iter(data, _used_delimit=_used_delimit, **kws)
        elif isinstance(data, dict):
            return cls.create_from_dict(data, _used_delimit=_used_delimit, **kws)
        else:
            return cls.create_from_str(str(data), _used_delimit=_used_delimit, _raw_type_=type(data))

    @classmethod
    def create_from_str(cls, text, tpl_args_offset=0, **kwargs):
        _used_delimit = kwargs.get("_used_delimit", True)
        if _used_delimit:
            return cls(text, tpl_args_offset=tpl_args_offset, **kwargs)

        cofmt = cls._CoFormatter(text, **kwargs, tpl_args_offset=tpl_args_offset)
        tpl_text = cofmt.raw_template()
        return cls(tpl_text, **cofmt.default_kwargs,
                   tpl_args_count=cofmt.tpl_args_count,
                   tpl_args_offset=tpl_args_offset, **kwargs)

    @classmethod
    def create_from_iter(cls, iter_data, tpl_args_offset=0, _cur_depth=0, **kwargs):
        if _cur_depth > cls._max_depth_:
            return cls(f"[TooComplexTpl:{_cur_depth}]")
        else:
            _cur_depth += 1

        res = []
        tpl_kwargs = {}
        tpl_args_cnt = tpl_args_offset
        for m in iter_data:
            m2 = cls.create(m, tpl_args_offset=tpl_args_cnt, _cur_depth=_cur_depth, **kwargs)
            res.append(m2.tpl_text)
            tpl_kwargs.update(m2.default_kwargs)
            tpl_args_cnt += m2.tpl_args_count
        tpl_text = cls.pformat_json(res, indent=2)
        return cls(tpl_text, tpl_args_count=tpl_args_cnt,
                   tpl_args_offset=tpl_args_offset,
                   tpl_kwargs=tpl_kwargs, **kwargs)

    @classmethod
    def create_from_dict(cls, tpl_dict, tpl_args_offset=0, _cur_depth=0, **tpl_kws):
        if _cur_depth > cls._max_depth_:
            return cls(f"[TooComplexTpl:{_cur_depth}]")
        else:
            _cur_depth += 1

        tpl_kwargs = {}
        tpl_args_cnt = tpl_args_offset
        res = OrderedDict()
        for k, v in tpl_dict.items():
            cofmt_k = cls.create(k, **tpl_kws, tpl_args_offset=tpl_args_cnt, _cur_depth=_cur_depth)
            tpl_kwargs.update(cofmt_k.default_kwargs)
            tpl_args_cnt += cofmt_k.tpl_args_count
            k2 = cofmt_k.tpl_text

            cofmt_v = cls.create(v, **tpl_kws, tpl_args_offset=tpl_args_cnt, _cur_depth=_cur_depth)
            tpl_kwargs.update(cofmt_v.default_kwargs)
            tpl_args_cnt += cofmt_v.tpl_args_count
            v2 = cofmt_v.tpl_text

            # print(cofmt_k, cofmt_v, tpl_kwargs)
            res[k2] = v2

        tpl_text = cls.pformat_json(res)
        tpl_m = cls(tpl_text, tpl_kwargs=tpl_kwargs, tpl_args_count=tpl_args_cnt, **tpl_kws)
        return tpl_m

    @classmethod
    def decode(cls, data):
        if isinstance(data, str):
            try:
                m = json.loads(data)
                return cls.decode(m)
            except Exception as e:
                return data
        elif isinstance(data, list):
            ms = []
            for t in data:
                ms.append(cls.decode(t))
            return ms
        elif isinstance(data, dict):
            ms = {}
            for k, v in data.items():
                ms[k] = cls.decode(v)
            return ms
        return data

    def render_data(self, tpl_kwargs=None, tpl_args=None, **extra_kwargs):
        kws = dict(self.default_kwargs, **extra_kwargs)
        if isinstance(tpl_kwargs, dict):
            kws.update(tpl_kwargs)

        if isinstance(tpl_args, (tuple, list)):
            cnt = min(self.tpl_args_count, len(tpl_args))
            _render_args = self._get_render_args()
            kws2 = dict((_render_args[i], tpl_args[i]) for i in range(cnt))
            kws.update(kws2)
        self._rendered_kws = kws
        text = self._tpl.safe_substitute(kws)
        return self.decode(text)

    def render(self, **kwargs):
        data = self.render_data(**kwargs)
        return self.pformat_json(data)

    def to_json(self, **kwargs):
        return self.render(**kwargs)

    def save_file(self, fout, **kwargs):
        with open(fout, "w") as fw:
            fw.write(self.render(**kwargs))
        return fout

    @classmethod
    def load_file(cls, fout, **kwargs):
        with open(fout, "r") as fr:
            txt = fr.read()
            return cls(txt, **kwargs)

    def __repr__(self):
        m = dict(vars(self), _type=self.__class__.__name__)
        return pformat(m, indent=2)
