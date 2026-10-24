"""
AtCoder用テンプレート
Repository:
https://github.com/tanukineiri31514/My_AtCoder_Templates

各種ライブラリ:
MainTemplates:
https://github.com/tanukineiri31514/My_AtCoder_Templates/blob/main/temp.py

SegmentTree, LazySegmentTree:
https://github.com/tanukineiri31514/My_AtCoder_Templates/blob/main/SEG.py

UnionFind:
https://github.com/tanukineiri31514/My_AtCoder_Templates/blob/main/UF.py

Gitの更新を忘れて少し異なる場合があります

"""

import sys
import heapq # 優先度付きキュー
from bisect import bisect_left, bisect_right
from collections import deque
from itertools import combinations
from itertools import permutations
from math import*
def input():return sys.stdin.readline().strip()
heap = heapq.heapify
push = heapq.heappush
pop = heapq.heappop
mod9 = 10**9 + 7
mod998 = 998244353
INF = 10**36
move8 = [(-1,-1),(-1,0),(-1, 1),(0 ,-1),( 0, 1),(1 ,-1),( 1, 0),(1, 1)]
move4 = [(0,-1),(0,1),(-1,0),(1,0)]
move4c = [(-1,-1),(-1,1),(1,-1),(1,1)]
dirc = {"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)}
Yes = 'Yes'
No = "No"

def lint():return list(map(int,input().split()))
def lstr():return list(map(str,input().split()))
def mint():return map(int,input().split())
def mstr():return map(str,input().split())
def bsl(l,n):return bisect_left(l,n)# n以上の要素数
def bsr(l,n):return bisect_right(l,n) # n以下の要素数
def bs(l,n):return (bisect_left(l,n),bisect_right(l,n)) # 二分探索
def manhat(T1,T2):return sum(abs(a-b) for a,b in zip(T1,T2))
def ugread(T1,T2):return dist(T1,T2)
def sort(l):return list(sorted(l))
def ps(a:list): #累積和
    s = [0]
    for x in a:s.append(s[-1] + x)
    return s #list
def ps_2d(g): # 二次元累積和
    h = len(g)
    w = len(g[0])
    m = [[0]*(w+1) for _ in range(h+1)]
    for i in range(1,h+1):
        for j in range(1,w+1):m[i][j] = (m[i-1][j]+m[i][j-1]-m[i-1][j-1]+g[i-1][j-1])
    return m
def ps_2dm(g:list,pos:tuple,add=1):
    a,b,c,d = pos
    g[a][b] += add
    g[c+1][d+1] += add
    g[a][d+1] -= add
    g[c+1][b] -= add
    return g
def alpha_id(c):
    if'a'<=c<='z':return ord(c)-96
    if'A'<=c<='Z':return ord(c)-38
    raise ValueError("alphabet only")
def rle(s): # ランレングス圧縮
    res = []
    cur = s[0]
    cnt = 1
    for i in range(1, len(s)):
        if s[i] == cur:cnt += 1
        else:
            res.append((cur, cnt))
            cur = s[i]
            cnt = 1
    res.append((cur, cnt))
    return res
def rotate(l,c=1): # 90度回転
    for i in range(c%4):l = [list(row) for row in zip(*l[::-1])]
    return l
def ncr(n, r):return comb(n, r)
def get_kv(d:dict):return d.items()
def get_k(d:dict):return d.keys()
def get_v(d:dict):return d.values()
def contdic(l):
  d = {}
  for i in l:
    if i not in d:
      d[i] = 1
    else:
      d[i] += 1
  return d
enu = enumerate
combi = combinations
permi = permutations
def dic_sort_v(l) :return sorted(l.items(), key = lambda A : A[1])\]}\]_}}
def _deque():
    """ this fanc in deque template"""
    # from collections import deque
    x = None
    _ = deque()
    _.append(x) # xを右に追加
    _.appendleft(x) # xを左に追加
    _.pop() # 右側を削除し返り値として持つ
    _.popleft() # 左側を削除し返り値として持つ
    _.clear() # 初期化
    _.copy() # コピー
def cc(l,mapping=True): # 座圧
  L = sorted(set(l))
  n = {x:i for i,x in enumerate(L)}
  ls = [n[i] for i in l]
  
  if mapping:
    return n
  else:
    return ls

def _heap():
    _ = []
    X = int()
    heap(_)
    push(_,X)
    num = pop(_)

"""
bit temp

for bit in range(1<<n):
    for i in range(n):
        if bit >> i & 1:
        # check

"""

"""
memo

"""
