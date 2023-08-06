#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 17:15:59 2020

@author: Juntong
"""

from array import array
from collections.abc import Iterable
from itertools import zip_longest, count
import tkinter as tk
try:
    import reprlist._tools as _tools
except:
    import _tools

class Reprlist:
    
    def __init__(self,extend=None, rule = None):
        self.main = {}
        self.setrule(rule)
        if extend is not None:
            self.extend(extend)
    def extend(self, iterable, fillside='l', fillchar=' ',
               cheaktype=True):
        if cheaktype:
            if isinstance(iterable, Reprlist):
                self.extend(iterable[:], fillside, fillchar, False)
                return self
            elif isinstance(iterable, array):
                iterable = iterable.tounicode().splitlines()
            elif all(not isinstance(i, str) and isinstance(i, Iterable)
                    for i in iterable):
                for et in zip_longest(*iterable,fillvalue=''):
                    self.extend(et)
                else:
                    return self
        try:
            lv = len(iterable)
        except TypeError:
            iterable = list(iterable)
            lv = len(iterable)
        mv = lv // 2       #The middle subscript of iterable.
        ls = len(self.main)#The length of self.
        ms = ls // 2       #The middle subscript of self.
        maxlen = max(len(i) for i in iterable)
        if fillside in ('l','left','左'):
            fill = lambda x:x.ljust(maxlen,fillchar)
        elif fillside in ('r','right','右'):
            fill = lambda x:x.rjust(maxlen,fillchar)
        else:
            raise ValueError('Unknow fillside,must be (%s).'%
                             "'l','left' or '左','r','right','右'")
        if ls > lv:
            # 0  __       
            # 1  __  __ 0 
            #>2  __  __ 1<
            # 3  __       
            # 4  __       
            on = ms - mv
            down = lv + ms - mv
            f0 = fill('')
            for i in range(on):
                self.main[i].extend(f0)
            for i in range(on, down):
                self.main[i].extend(fill(iterable[i-on]))
            for i in range(down, ls):
                self.main[i].extend(f0)
        elif ls < lv:
            on = mv - ms
            down = ls + mv - ms
            f1 = array('u',fillchar*self.width)
            newmain = {}
            for i in range(on):
                newmain[i] = f1 + array('u',fill(iterable[i]))
            for i in range(on, down):
                newmain[i] = self.main[i-on] + array('u',fill(iterable[i]))
            for i in range(down, lv):
                newmain[i] = f1 + array('u',fill(iterable[i]))
            self.main = newmain
        else:
            for i in range(len(self.main)):
                self.main[i] += array('u',fill(iterable[i]))
        return self
    def __repr__(self):
        r = self._r['startswith']
        ll = len(str(self.length)) + 1
        if self._r['maxline'] is None or self.width <= self._r['maxline']:
            it = enumerate(self)
        else:
            it = _tools._set_maxline(self._r['maxline'])(self)
        func = _tools._set_maxstring(self._r['maxstring'])
        for s, i in it:
            r += f'{ s }:'.rjust(ll) + func(i) + '\n'
        return r[:-1]
    def __str__(self):
        r = self._s['startswith']
        if self._s['maxline'] is None or self.width <= self._s['maxline']:
            it = enumerate(self)
        else:
            it = _tools._set_maxline(self._s['maxline'])(self)
        func = _tools._set_maxstring(self._s['maxstring'])
        for _, i in it:
            r += func(i) + '\n'
        return r[:-1]
    def __len__(self):
        return len(self.main)
    def __iter__(self):
        for i in range(self.length):
            yield self.main[i].tounicode()
    def __getitem__(self, item):
        if isinstance(item, tuple):
            return Reprlist([i[item[1]] for i in self[item[0]]])
        else:
            if isinstance(item, int) and item < 0:
                item = len(self.main) + item
            rg = tuple(range(len(self.main)))[item]
            if isinstance(rg,int):
                return [self.main[rg].tounicode()]
            else:
                return [self.main[i].tounicode() for i in rg]
    def __setitem__(self, item, val):
        if isinstance(item, int):
            if item < 0:
                item = len(self.main) + item
            old = self.main[item]
            if len(old) != len(val):
                raise ValueError("Need length %s, got %s."
                                 %(len(old),len(val)))
            self.main[item] = array('u', val)
        if isinstance(item, tuple):
            if len({len(i) for i in val})!=1:
                raise ValueError("The shape of value is different.") 
            item, file = item
            rg = range(self.length)[item]
            if isinstance(rg, int):
                a = val if isinstance(val,str) else val[0]
                if len(a) != len(self.main[rg][file]):
                    raise ValueError(f"Need len {len(self.main[rg][file])}.")
                self.main[rg][file] = a
            else:
                for ix, key in enumerate(rg):
                    a = val[ix]
                    if len(a) != len(self.main[key][file]):
                        l = len(self.main[rg][file])
                        raise ValueError(f"Need len {l},raise at val[{ix}].")
                    self.main[key][file] = a
        else:
            rg = range(self.length)[item]
            if isinstance(rg, int):self[rg] = val
            if len(rg) != len(val):
                raise ValueError("Need val length %s."%len(rg))
            ix = 0
            for key in rg:
                self[key] = str(val[ix])
                ix += 1
    def __add__(self, val):
        return self.copy().extend(val)
    def __eq__(self,o):
        return isinstance(o,Reprlist) and self.main==o.main
    def __bool__(self):return bool(self.main)
    def setrule(self, rule=None):
        rl = _tools.get_global_rule()
        if rule is not None:
            for k in rule:
                rl[k].update(rule[k])
            _tools.check_rule_value(rl)
        self._s = rl['s']
        self._r = rl['r']
        self._f = rl['f']
    @property
    def width(self):
        try:
            return len(self.main[0])
        except KeyError:
            return 0
    @property
    def length(self):
        return len(self.main)
    @property
    def mid(self):
        return len(self) // 2
    @mid.setter
    def mid(self, val):
        self.change_mid(val)
    def change_mid(self, newmid, fillchar=' '):
        if len(fillchar) != 1:
            TypeError(
            'The fill character must be exactly one character long.')
        l = self.length
        sd = l // 2
        f = fillchar*l
        if newmid > sd:
            for i in range(l,newmid*2):
                self.main[i] = array('u',f)
        elif newmid < sd:
            n = {}
            first = sd - newmid + 1
            for i in range(first):
                n[i] = array('u',f)
            for i in range(first, first+l):
                n[i] = self.main[i-first]
            self.main = n
        return self
    def copy(self):
        'deep copy.'
        r = Reprlist()
        r.main = {i:array('u',self.main[i].tounicode())
                    for i in range(self.length)}
        return r
    @property
    def T(self):
        r = Reprlist()
        for i in self:
            r.extend(i,cheaktype=False)
        return r
    def smart_extend(self, val, selfmid=None, valmid=None,
                     fillside='l', fillchar=' ',
                     remove_empty=False):
        if not isinstance(val, Reprlist):
            val = Reprlist().extend(val, fillside, fillchar)
        if selfmid is not None:
            self.change_mid(selfmid, fillchar)
        if valmid is not None:
            val.change_mid(valmid, fillchar)
        self.extend(val[:], fillside, fillchar, False)
        if remove_empty:
            rm = []
            for key, val in self.main.items():
                if not val.tounicode().strip():
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
        return self
    def append(self,thing:str,at, fillchar=' '):
        'Add `thing` after line `at` .'
        if at < 0 :at += len(self.main)
        thing = str(thing)
        a = ''.ljust(len(thing), fillchar)
        for i in range(at):
            self.main[i].extend(a)
        self.main[at].extend(thing)
        for i in range(at+1,len(self.main)):
            self.main[i].extend(a)
        return self
    def insert(self, obj, at, fillchar=' '):
        nm = {}
        val = list(obj)
        lv = len(val)
        sf = ''.ljust(self.length, fillchar)
        fill = array('u', sf)
        if at < 0 :at += len(self.main)
        elif at == self.length + 1:
            try:
                self.append(sf,0,fillchar)
            except KeyError:
                return self.extend(val)
            else:
                return self.place_onto([f'{sf}{i}' for i in val])
        for i in range(at):
            nm[i] = self.main[i] + fill
        for index, nv in zip(count(at, 1), val):
            nm[index] = array('u', sf + nv)
        for i in range(index + 1, self.length + lv):
            nm[i] = self.main[i-lv] + fill
        self.main = nm
        return self
    def get_inserted(self, val, at, fillchar=' '):
        return self.copy().insert(val, at, fillchar=' ')
    def get_removed_empty_lines(self,rubbish=None):
        'Remove the line if not [index].strip(rubbish).'
        r = self[:]
        i = 0
        while 1 :
            if not r[i].strip(rubbish):
                r.pop(i)
            else:i += 1
            if i == len(r):return Reprlist(r)
    def place_onto(self, bottom, wherejust = 'l'):
        if not self:
            self.main = bottom.main
            return bottom
        if not bottom:
            return self
        bottom = Reprlist(bottom)
        bl = bottom.length
        sl = self.length
        bw = bottom.width
        sw = self.width
        if wherejust in ('l', 'left'):
            if sw > bw:
                bottom.append(' '*(sw-bw), 0)
            elif sw < bw:
                self.append(' '*(bw-sw), 0)
        elif wherejust in ('r', 'right',):
            if sw > bw:
                bottom = bottom.rmove(sw - bw,)
            elif sw < bw:
                self.main = self.rmove(bw - sw).main
        elif wherejust in ('m', 'middle'):
            if sw > bw:
                n = sw-bw
                l = n // 2
                n = n - l
                bottom.append(' '*(l), 0)
                bottom = bottom.rmove(n)
            elif sw < bw:
                n = bw-sw
                l = n // 2
                n = n - l
                self.append(' '*(l), 0)
                self.main = self.rmove(n).main
        for i in range(bl):
            self.main[sl] = bottom.main[i]
            sl += 1
        return self
    def place_under(self, top, wherejust = 'l'):
        top = Reprlist(top)
        self.main = top.place_onto(self, wherejust).main
        return self
    def line(self, line_number):
        if line_number < 0:line_number += len(self.main)
#        return self.main[line_number].tounicode()
        return ''.join(self.main[line_number])
    def rmove(self, step, fillchar=' '):
        f = array('u', ''.ljust(step, fillchar))
        for i in range(self.length):
            self.main[i] = f + self.main[i]
        return self
    def lmove(self, step, fillchar=' '):
        f = ''.ljust(step, fillchar)
        for i in range(self.length):
            self.main[i].extend(f)
        return self
    def put_inbox(self, sides_wnes='####', nw='#', ne='#', sw='#', se='#',):
        '''
                  #######
                  #some #
        some ---->#thing#
        thing     #######
        '''
        if not self.main:raise ValueError("List is empty!")
        left, up, right, down = sides_wnes
        self.lmove(1,left)
        self.rmove(1,right)
        width = self.width
        self.place_onto([down*(width)])
        self.place_under([up*width])
        self[0,0],self[0,-1],self[-1,0],self[-1,-1] = (nw, ne, sw, se)
        return self
    def to_tk(self, root=None, **kargstoLabel):
        if root is None:
            root = tk.Tk()
            root.title('Reprlist.to_tk')
            root.geometry(f'{self.width * 12}x{self.length * 24 + 48}')
        for x, v in enumerate(self, 1):
            la = tk.Label(root, text = v, font=('Arial', 12), **kargstoLabel)
            la.place(x= 12, y= x * 24)
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