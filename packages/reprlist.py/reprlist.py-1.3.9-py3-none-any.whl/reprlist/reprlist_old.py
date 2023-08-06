#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Great tool to realize __repr__.
Created on Sat Dec 21 22:06:07 2019
@author: Juntong
e-mail:jessica_ye2015@sina.com
"""
try:
    import reprlist._tools as _tools
except:
    import _tools


class Reprlist:
    """\
  Create and edit multiline text, great tool to realize __repr__.
It keeps all the tandem length same.
When you extend it ,it will align center.
  Method `append(thing, at)` can
add the 'thing' after the appointed line.
  Method 'get_inserted(obj,new_index)' will
return a new Reprlist with `obj` at the `new_index`.
  Slice with `[:]` will get a list with texts each line,
slice with `[:,:]` will get the str blocks in each line,
and `R[<int1>,<int2>]` will get the <int2> str block in line <int1>,
change the list with R[<>,<>]='<shape=original shape>'.
  Use `str` will get '\\n'+'\\n'.join(self[:]).
  Deep-Copy it by using method `copy` or
set up by R[:,:] like `Reprlist(R[:,:])`.
  All mothod's name starts with `get` will return a new obj.
    """

    def __init__(self, extend=None, rule=None):
        r"""Extend value `extend` if it's not None.
        `rule` will load `global_rule` if it's None;
        The default global_rule is {'r':{
                                        'maxstring':  80,
                                        'maxline':    80,
                                        'startswith': '',},
                                    's':{
                                        'maxstring':  80,
                                        'maxline':    80,
                                        'startswith': '\n',
                                        },
                                    'f':{
                                        'maxstring':  None,
                                        'maxline':    None,
                                        'startswith': '',
                                        'linebreaks': '\n',
                                        },
                                    },
        you can give a dict like this, the class will set with yours.
        By the way,you can change global_rule with func `SetGlobalRule`.
        """
        self.main = {}
        #   main likes
        #       {0:[['0'],['1']],
        #        1:[['0'],['1']],
        #        }
        self.size = []
        self.setrule(rule)
        if extend is not None:
            self.extend(extend)

    def __repr__(self):
        r = ''
        ll = len(str(self.length - 1))
        for s, i in self._r_len(self):
            r += str(s).rjust(ll) + ':'
            r += self._r_gen(i) + '\n'
        return self._r_s + r

    def __str__(self):
        return self._s_s + \
               '\n'.join(self._s_gen(i) for _, i in self._s_len(self))

    def __len__(self):
        return len(self.main)

    def __eq__(self, o):
        return isinstance(o, Reprlist) and self.main == o.main

    def __getitem__(self, line):
        try:
            line, file = line
        except TypeError:
            file = None
        else:
            if isinstance(file, int) and file < 0:
                file = len(self.size) + file
        finally:
            if isinstance(line, int) and line < 0:
                line = len(self) + line
        try:
            l = self.main[line]
            if file is None:
                return ''.join(i[0] for i in l)
            else:
                if isinstance(file, int):
                    # To return the self, not a copied one.
                    return l[file]
                return [i[0] for i in l[file]]
        except TypeError:
            r = []
            for i in range(len(self.main))[line]:
                if file is not None:
                    r.append([i[0] for i in self.main[i]][file])
                else:
                    r.append(self[i])
            return r

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            if len(key) > 2:
                raise IndexError(f"Need two subscripts, {len(key)} got.")
            ov = self[key]
            k0, k1 = key
            so = _tools.shape(ov)
            sv = _tools.shape(value)
            if not isinstance(k0, int) or not isinstance(k1, int):
                if so != sv:
                    if len(so) == len(sv) and sum(so[-1]) == sum(sv[-1]):
                        value = _tools.reshape(value, so[-1])
                        self[key] = value
                        return
                    else:
                        raise ValueError("The shape of value is different.")
                rg = range(len(self.main))[k0]
                value = _tools.reshape(value, so[-1])
                if type(rg) is int:
                    self.main[rg][k1] = [[str(i)] for i in value]
                else:
                    st = rg[0]
                    for l in rg:
                        self.main[l][k1] = [[str(i)] for i in value[l - st]]
            elif type(value) is not str:
                if so == sv:
                    ov[0] = value[0]
                else:
                    raise ValueError("The shape of value is different.")
            elif len(ov[0]) != len(value):
                raise ValueError("Need value's length {len(ov[0])}, "
                                 f"got {len(value)}.")
            else:
                ov[0] = value
        else:
            raise IndexError("Need two subscripts, only one got.")

    def __iter__(self):
        return iter(self[:])

    def __add__(self, val):
        'Return self.copy().extend(val).'
        return self.copy().extend(val)

    def __bool__(self):
        return bool(self.main)

    def setrule(self, rule=None):
        rl = _tools.get_global_rule()
        if rule is not None:
            for k in rule:
                rl[k].update(rule[k])
            _tools.check_rule_value(rl)
        self._r_gen, self._r_len, self._s_gen, self._s_len = \
            _tools.comp_rule(rl)
        self._r_s, self._s_s = rl['r']['startswith'], rl['s']['startswith']
        self._f = rl['f']

    def extend(self, o, _chack=True):
        '''\
Extend each line, align center.
       l=6  lo=3
    0  ___        
    1  ___        
    2  ___  ___  0  
mid>3  ___  ___  1<
    4  ___  ___  2  
    5  ___        
    6
       l=3     lo=7
               ___ 0
               ___ 1
    0  ___     ___ 2
mid>1  ___     ___<3
    2  ___     ___ 4
               ___ 5
               ___ 6
                   7
        '''
        if _chack:
            if isinstance(o, Reprlist):
                return self.extend_a_Reprlist(o)
            #            if type(o) is str:
            #                o = o.splitlines()
            elif all(_tools.iterable(i) and not isinstance(i, str) for i in o):
                return self.extend_a_2d_list(o)
            else:
                o = [str(i) for i in o]
        l = len(self.main)
        try:
            lo = len(o)
        except TypeError:
            o = list(o)
            lo = len(o)
        try:
            max_len = max(len(i) for i in o)
        except ValueError:
            raise ValueError('Got a empty obj.')
        if l == lo:
            for i in range(l):
                self.main[i].append([o[i].ljust(max_len)])
        else:
            l2 = l // 2
            lo2 = lo // 2
            if l > lo:
                on_mid = l2 - lo2
                down_mid = l2 + lo - lo2
                #       l=6  lo=3
                #    0  ___        -|-range(on_mid)
                #    1  ___        -\-
                #    2  ___  ___  0  on_mid = 2   -|-
                # mid>3  ___  ___  1<      range(on_mid,down_mid)
                #    4  ___  ___  2  down_mid-1=4 -\-
                #    5  ___        -|-range(down_mid,l)
                #    6
                a = ' ' * max_len
                for i in range(on_mid):
                    self.main[i].append([a])
                for i in range(on_mid, down_mid):
                    self.main[i].append(
                        [o[i - on_mid].ljust(max_len)])
                for i in range(down_mid, l):
                    self.main[i].append([a])
            else:
                #       l=3     lo=7
                #               ___ 0-|-
                #               ___ 1-|-range(out_len)
                #    0  ___     ___ 2   -|-
                # mid>1  ___     ___<3   range(out_len,mid_len)
                #    2  ___     ___ 4   -|-
                #               ___ 5-|-range(mid_len,lo)
                #               ___ 6-\-
                #                   7
                out_len = lo2 - l2
                mid_len = lo2 + l - l2
                cm = self.main.copy()
                for i in range(out_len):
                    self.main[i] = [[' ' * i] for i in self.size] + \
                                   [[o[i].ljust(max_len)]]
                for i in range(out_len, mid_len):
                    self.main[i] = cm[i - out_len]
                    self.main[i].append([o[i].ljust(max_len)])
                for i in range(mid_len, lo):
                    self.main[i] = [[' ' * i] for i in self.size] + \
                                   [[o[i].ljust(max_len)]]
        self.size.append(max_len)
        return self

    def extend_a_2d_list(self, value, ):
        "You needn't use it because `extend` will decide whether to use."
        for i in _tools.itertools.zip_longest(*value, fillvalue=' '):
            self.extend(i)
        return self

    def extend_a_Reprlist(self, value):
        "You needn't use it because `extend` will decide whether to use."
        for i in value.T:
            self.extend(i, False)
        return self

    def smart_extend(self, o, selfmid=None, valmid=None, remove_empty=False):
        """\
Extend with given-value,align the text with the assigned line.
        """
        if not isinstance(o, Reprlist):
            o = Reprlist(o)
        if selfmid is not None:
            self.change_mid(selfmid)
        if valmid is not None:
            o = o.change_mid(valmid)

        self.extend_a_Reprlist(o)

        if remove_empty:
            rm = []
            for key, val in self.main.items():
                if not ''.join(i[0] for i in val).strip():
                    rm.append(key)
            if rm:
                for i in rm:
                    self.main.pop(i)
                sub = 1
                dlt = rm[-1]
                for i in range(rm[0] + 1, max(self.main) + 1):
                    try:
                        self.main[i - sub] = self.main[i]
                    except KeyError:
                        sub += 1
                    else:
                        if i > dlt:
                            del self.main[i]
            self._reset_size()
        return self

    def _reset_size(self):
        try:
            self = [len(i[0]) for i in self.main[0]]
        except (KeyError, IndexError):
            self.size = []

    def change_mid(self, mid):
        """\
If mid < given-value, the self[self.mid] will be 
  the thing at line <value> before changed;
if mid > given-value, self.mid will equal the value.
        """
        om = self.mid
        b = [' ' * i for i in self.size]
        if mid > om:
            for i in range(len(self.main), mid * 2 + 1):
                self.main[i] = [[i] for i in b]
        elif mid < om:
            n = len(self.main)
            for i in range(n + om - mid, 0, -1):
                n -= 1
                self.main[i] = self.main[n]
                if n == 0: break
            for j in range(i):
                self.main[j] = [[i] for i in b]
        return self

    def append(self, thing: str, at):
        'Add `thing` after line `at` .'
        l = len(thing)
        a = ' ' * l
        for i in range(at):
            self.main[i].append([a])
        self.main[at].append([thing])
        for i in range(at + 1, len(self.main)):
            self.main[i].append([a])
        self.size.append(l)
        return self

    def insert(self, obj, new_index):
        n = self.get_inserted(obj, new_index)
        self.main = n.main
        self.size = n.size
        return self

    def combine(self):
        "Combine all the str-blocks."
        c = self.get_combined()
        self.main = c.main
        self.size = c.size
        return self

    def separate(self):
        "Separate all the str-blocks to 1-length str."
        a = self.get_abruption()
        self.main = a.main
        self.size = a.size
        return self

    def get_inserted(self, obj, new_index):
        "Value `obj` will at the end of the `new_index` line in result."
        if isinstance(obj, Reprlist):
            obj = obj[:]
        try:
            lo = len(obj)
        except TypeError:
            obj = list(obj)
            lo = len(obj)
        a = ' ' * lo
        e = self[:new_index, :]
        for i in e:
            _tools.Reprlist_inster_use(a, i, lo)
        b = [' ' * i for i in self.size]
        for i in obj:
            e.append(b + [i])
        ea = self[new_index:, :]
        for i in ea:
            _tools.Reprlist_inster_use(a, i, lo)
        return Reprlist(e + ea)

    def get_combined(self):
        "Combine all the str-blocks."
        return Reprlist([i for i in self])

    def get_abruption(self):
        "Separate all the str-blocks to 1-length str."
        r = Reprlist()
        l = len(self.main)
        for i in self.T:
            sep = len(i) // l
            for s in range(sep):
                r.extend(i[s::sep])
        return r

    def get_removed_empty_lines(self, rubbish=None):
        'Remove the line if not [index].strip(rubbish).'
        r = self[:]
        i = 0
        while 1:
            if not r[i].strip(rubbish):
                r.pop(i)
            else:
                i += 1
            if i == len(r):
                try:
                    return Reprlist(r)
                except ValueError:
                    return Reprlist()

    def place_onto(self, bottom, wherejust='l'):
        '''Place R on `bottom`.
        `wherejust` --> 'l' / 'left': storter one in a position of lift.
                    --> 'r' / 'right':storter one in a position of right.
                    --> 'm' / 'middle':storter one in a position of middle.
        '''
        top = self
        if not isinstance(bottom, Reprlist):
            bottom = Reprlist(bottom)
        width = sum(top.size)
        if not width:
            # self is empty.
            return self.extend_a_Reprlist(bottom)
        bwidth = sum(bottom.size)
        if not bwidth:
            return top
        if wherejust in ('l', 'left', '左'):
            def extend(s, width):
                return s.ljust(width)
        elif wherejust in ('r', 'right', '右'):
            def extend(s, width):
                return s.rjust(width)
        elif wherejust in ('m', 'middle', '中'):
            dic = {}

            def extend(s, width):
                try:
                    return s.ljust(dic['l']).rjust(width)
                except KeyError:
                    n = width - len(s)
                    dic['l'] = width - n // 2
                    return extend(s, width)
        else:
            def extend(s, width):
                return s.ljust(wherejust).rjust(width - wherejust)
        if width > bwidth:
            #            bottom.append(' '*(width-bwidth),0)
            for i in bottom.main:
                bottom.main[i][0][0] = extend(bottom.main[i][0][0], width)
            bottom.size = [width]
        elif bwidth > width:
            #            top.append(' '*(bwidth-width),0)
            for i in top.main:
                top.main[i][0][0] = extend(top.main[i][0][0], bwidth)
            top.size = [bwidth]
        length = len(self.main)
        for i in range(len(bottom)):
            top.main[length] = bottom.main[i]
            length += 1
        return top

    def get_place_under(self, top, wherejust='l'):
        'Powered with `get_place_onto`.'
        return Reprlist(top).get_place_onto(self, wherejust)

    def get_place_onto(self, bottom, wherejust='l'):
        'Powered with `get_place_onto`.'
        return self.copy().place_onto(bottom, wherejust='l')

    def place_under(self, top, wherejust='l'):
        'Powered with `get_place_onto`.'
        top = Reprlist(top)
        self.main = top.get_place_onto(self[:], wherejust).main
        return self

    @property
    def T(self):
        "Note:R.T.T == R.get_abruption() ."
        r = Reprlist()
        for i in self:
            r.extend(i, False)
        return r

    @property
    def mid(self):
        return len(self.main) // 2

    @mid.setter
    def mid(self, val):
        self.change_mid(int(val))

    @property
    def length(self):
        return len(self.main)

    @property
    def width(self):
        return sum(self.size)

    @property
    def shape(self):
        return _tools.shape(self[:, :])

    def copy(self):
        return Reprlist(self[:, :])

    def square(self):
        s = max(self.size)
        r = Reprlist()
        for i in self.main:
            r.main[i] = [[j[0].ljust(s)] for j in self.main[i]]
        r.size.extend(s for _ in self.size)
        return r

    def line(self, linenumber):
        '''Return the str at line `linenumber`.
        Can make code more beautifur.
        Like `R.line(1).startswith(...)`.'''
        if linenumber < 0:
            linenumber += len(self)
        return ''.join(i[0] for i in self.main[linenumber])

    def lmove(self, step, fillchar=' '):
        " `!` ---> `!_` by .lmove(1,'_')."
        f = ''.ljust(step, fillchar)
        self.main = \
            Reprlist(f for _ in range(len(self) + 1)).extend_a_Reprlist(self).main
        return self

    def ljust(self, step, fillchar=' '):
        s = self.size
        if s <= step:
            return self.copy()
        else:
            return self.lmove(step - s)

    def rmove(self, step, fillchar=' '):
        " `!` ---> `_!` by .rmove(1,'_')."
        f = ''.ljust(step, fillchar)
        return self.extend([f for _ in range(len(self))], _chack=False)

    def rjust(self, step, fillchar=' '):
        s = self.size
        if s <= step:
            return self.copy()
        else:
            return self.rmove(step - s)

    def put_inbox(self, sides_wnes='####', nw='#', ne='#', sw='#', se='#', ):
        '''
                  #######
                  #some #
        some ---->#thing#
        thing     #######
        '''
        left, up, right, down = sides_wnes
        self.lmove(1, left)
        self.rmove(1, right)
        width = self.width
        self.place_onto([down * width])
        self.place_under([up * width])
        self.separate()
        self[0, 0], self[0, -1], self[-1, 0], self[-1, -1] = (nw, ne, sw, se)
        return self

    def to_tk(self, root=None, **kargstoLabel):
        if root is None:
            root = _tools.tk.Tk()
            root.title('Reprlist.to_tk')
            root.geometry(f'{self.width * 12}x{self.length * 24 + 48}')
        for x, v in enumerate(self, 1):
            la = _tools.tk.Label(root, text=v, font=('Arial', 12),
                                 **kargstoLabel)
            la.place(x=12, y=x * 24)
        return root

    def to_file(self, fileORpath):
        if isinstance(fileORpath, str):
            with open(fileORpath, 'w') as pf:
                pf.write(self._f['startswith'] +
                         self._f['linebreaks'].join(self))
        else:
            with fileORpath as pf:
                pf.write(self._f['startswith'] +
                         self._f['linebreaks'].join(self))
