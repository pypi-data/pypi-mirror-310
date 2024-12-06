#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

# モジュールの参照ルールに注意
#   パッケージとモジュールの名前
#     モジュールの名前は、全て小文字の短い名前にすべきです。読みやすくなるなら、アンダースコアをモジュール名に使っても構いません
#   拡張子は無視される
#     shachecksum.py -> shachecksum
#   パッケージ参照
#      この明示的な相対 import では、先頭のドットで現在および親パッケージを指定します.
#      .shachecksum   -> ./shachecksum.py
#      ..shachecksum  -> ../shachecksum.py
from .printdv import print_err, print_mes;
from .mk1pass import main_mk1pass, Main_mk1pass;


### Variables ###                                                                                                                                   
__version__     = Main_mk1pass.version;
__versiondate__ = Main_mk1pass.date; 

