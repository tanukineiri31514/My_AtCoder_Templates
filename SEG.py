class F:
    # 基本演算
    Add = staticmethod(lambda a,b: a+b)
    Mul = staticmethod(lambda a,b: a*b)
    Xor = staticmethod(lambda a,b: a^b)
    And = staticmethod(lambda a,b: a&b)
    Or = staticmethod(lambda a,b: a|b)

    # 文字列    # 文字列連結（左から順番に連結）
    # e = ""
    Concat = staticmethod(lambda a,b: a+b)

    # 集合
    # Union: 2つの集合の和集合（どちらかに含まれる要素）
    # e = set()
    Union = staticmethod(lambda a,b: a|b)

    # Inter: 2つの集合の積集合（両方に含まれる要素）
    # e = 全要素を含む集合
    Inter = staticmethod(lambda a,b: a&b)

    # 辞書のマージ（同じキーがあれば右側の値を優先）
    # e = {}
    Merge = staticmethod(lambda a,b: a|b)

    # 最大値とその出現回数を管理
    # a,b = (最大値, 個数)
    # e = (-INF, 0)
    @staticmethod
    def MaxCount(a, b):
        if a[0] > b[0]: return a
        if a[0] < b[0]: return b
        return (a[0], a[1]+b[1])

    # 最小値とその出現回数を管理
    # a,b = (最小値, 個数)
    # e = (INF, 0)
    @staticmethod
    def MinCount(a, b):
        if a[0] < b[0]: return a
        if a[0] > b[0]: return b
        return (a[0], a[1]+b[1])

    # 合計と要素数を同時に管理
    # a,b = (合計, 要素数)
    # e = (0, 0)
    @staticmethod
    def SumCount(a, b):
        return (a[0]+b[0], a[1]+b[1])

    # 区間の最小値と最大値を同時に管理
    # a,b = (最小値, 最大値)
    # e = (INF, -INF)
    @staticmethod
    def MinMax(a, b):
        return (min(a[0],b[0]), max(a[1],b[1]))

class Seg:
    def __init__(self, A, func, e):
        self.N = len(A)
        self.func = func
        self.e = e
        self.size = 1 << (self.N - 1).bit_length()
        self.tree = [e] * (2 * self.size)

        for i in range(self.N):
            self.tree[self.size + i] = A[i]

        # 木を作る
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.func(
                self.tree[2 * i],
                self.tree[2 * i + 1]
            )

    # A[k] = x
    # 要素の変更
    def update(self, i, x):
        i += self.size
        self.tree[i] = x

        while i > 1:
            i >>= 1
            self.tree[i] = self.func(
                self.tree[2 * i],
                self.tree[2 * i + 1]
            )

    # A[k] += x
    # ※普通の数値用
    def add(self, i, x):
        self.update(i, self.tree[self.size + i] + x)

    # A[k] を取得
    def get(self, i):
        return self.tree[self.size + i]
        
    # [l, r) の結果
    def query(self, l, r):
        left = self.e
        right = self.e
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                left = self.func(left, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                right = self.func(self.tree[r], right)

            l >>= 1
            r >>= 1

        return self.func(left, right)

    # 全体の結果
    def all(self):
        return self.tree[1]

    # 表示
    def print(self):
        print([self.get(i) for i in range(self.N)])
    
    def list_seg(self):
        return[self.get(i) for i in range(self.N)]

    # 木の中身を見る
    def print_tree(self):
        print(self.tree)
    
    def list_seg_tree(self):
        return(self.tree)
"""

Seg(list,式,初期値) -> 初期化
(min,max,lambda a,b:a+b)
seg.update(ind,X) -> 数値の変更
seg.add(i,X) -> 数値の加算
seg.get(i) -> l[i]の値の取得
seg.query(l,r) l以上r未満の範囲の結果
seg.all() -> 全体の結果
seg.print() -> リストの中の表示
seg.print_tree() -> 木の構造の表示
"""


class LSeg:
    """
    init(init_val, ide_ele): 配列init_valで初期化 O(N)
    add(l, r, x): 区間[l, r)にxを加算 O(logN)
    query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
    """
    def __init__(self, init_val, segfunc, ide_ele):
        """
        init_val: 配列の初期値
        segfunc: 区間にしたい操作
        ide_ele: 単位元
        num: n以上の最小の2のべき乗
        data: 値配列(1-index)
        lazy: 遅延配列(1-index)
        """
        n = len(init_val)
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1 << (n - 1).bit_length()
        self.data = [ide_ele] * 2 * self.num
        self.lazy = [0] * 2 * self.num
        # 配列の値を葉にセット
        for i in range(n):
            self.data[self.num + i] = init_val[i]
        # 構築していく
        for i in range(self.num - 1, 0, -1):
            self.data[i] = self.segfunc(self.data[2 * i], self.data[2 * i + 1])

    def prop(self, *ids):
        """
        遅延伝搬処理
        ids: 伝搬する対象の区間 
        """
        for i in reversed(ids):
            v = self.lazy[i]
            if not v:
                continue
            self.lazy[2 * i] += v
            self.lazy[2 * i + 1] += v
            self.data[2 * i] += v
            self.data[2 * i + 1] += v
            self.lazy[i] = 0

    def add(self, l, r, x):
        """
        区間[l, r)の値にxを加算
        l, r: index(0-index)
        x: additional value
        """
        *ids, = self._gindex(l, r)
        l += self.num
        r += self.num
        while l < r:
            if l & 1:
                self.lazy[l] += x
                self.data[l] += x
                l += 1
            if r & 1:
                self.lazy[r - 1] += x
                self.data[r - 1] += x
            r >>= 1
            l >>= 1
        for i in ids:
            self.data[i] = self.segfunc(self.data[2 * i], self.data[2 * i + 1]) + self.lazy[i]


    def query(self, l, r):
        """
        [l, r)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
        *ids, = self._gindex(l, r)
        self.prop(*ids)

        res = self.ide_ele

        l += self.num
        r += self.num
        while l < r:
            if l & 1:
                res = self.segfunc(res, self.data[l])
                l += 1
            if r & 1:
                res = self.segfunc(res, self.data[r - 1])
            l >>= 1
            r >>= 1
        return res

    def get(self, i):
        i += self.num
        self.prop(*self._gindex(i - self.num, i - self.num + 1))
        return self.data[i]
    
    def _gindex(self, l, r):
        """
        伝搬する対象の区間を求める
        lm: 伝搬する必要のある最大の左閉区間
        rm: 伝搬する必要のある最大の右開区間
        """
        l += self.num
        r += self.num
        lm = l >> (l & -l).bit_length()
        rm = r >> (r & -r).bit_length()

        while r > l:
            if l <= lm:
                yield l
            if r <= rm:
                yield r
            r >>= 1
            l >>= 1
        while l:
            yield l
            l >>= 1