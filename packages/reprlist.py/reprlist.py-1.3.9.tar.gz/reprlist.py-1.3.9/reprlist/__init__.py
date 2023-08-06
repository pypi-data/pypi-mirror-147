# -*- coding: utf-8 -*-
"""
  Create and edit multiline text, great tool to realize __repr__.
It keeps all the tandem length same.
When you extend it ,it will align center.
  Method `append(thing, at)` can
add the 'thing' after the appointed line.
  Method 'get_inserted(obj,new_index)' will 
return a new Reprlist with `obj` at the `new_index`.
  Slice with `[:]` will get a list with texts each line,
slice with `[:,:]` will get the str blocks in each line (the obj in dev will
return self.copy),
and `R[<int1>,<int2>]` will get the <int2> str block in line <int1>,
and in dev.Replist, it returns the char at the index.
change the list with R[<>,<>]='<shape=original shape>'.
  Use `str` will get '\\n'+'\\n'.join(self[:]).
  Deep-Copy it by using method `copy` or
set up by R[:,:] like `Reprlist(R[:,:])`.
  All mothod's name starts with `get` will return a new obj.
@author: Juntong
e-mail:jessica_ye2015@sina.com
"""

from reprlist.reprlist_old import Reprlist
import reprlist.dev as dev
import  reprlist._tools as _tools

class SetGlobalRule:
    r'''
`rule` is a dict with key `s` for `str` and `r` for `repr`.
Each key is based with{'r': {'maxstring': 80,'maxline': 80, 'startswith':''},
                       's': {'maxstring': 80,'maxline': 80, 'startswith':'\n'}}.
`maxstring` decides max length for string at each line,
`maxline` decides max length for all the lines.
    '''
    import json, os
    filename = os.path.dirname(__file__) +os.path.sep + 'globalrule.json'
    def __init__(self, new):
        self.keys = {'maxstring','maxline','startswith'}
        self.old = self.json.load(open(self.filename))
        if set(new) - {'r', 's'}:
            raise ValueError("Unknow key :", set(new) - {'r', 's'})
        if 'r' in new:
            self.set_repr_rule(new['r'])
        if 's' in new:
            self.set_str_rule(new['s'])
        if __name__ == "__main__":
            print("Success set global rule.")
    def set_repr_rule(self, new):
        if set(new) - self.keys:
            raise ValueError("Unknow key :", set(new) - self.keys)
        old = self.old.copy()
        old['r'].update(new)
        _tools.check_rule_value(old['r'])
        self.json.dump(old, open(self.filename, 'w'), )
    def set_str_rule(self, new):
        if set(new) - self.keys:
            raise ValueError("Unknow key :", set(new) - self.keys)
        old = self.old.copy()
        old['s'].update(new)
        _tools.check_rule_value(old['s'])
        self.json.dump(old, open(self.filename, 'w'), )
__all__ = ['Reprlist','dev','ChangeGlobalRule']