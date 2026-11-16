
class LSeg:
    def __init__(self, A, op, e, mapping, composition, id_):
        self._op = op
        self._e = e
        self._mapping = mapping
        self._composition = composition
        self._id = id_

        if isinstance(A, int):
            A = [e] * A

        self.N = len(A)
        self._log = (self.N - 1).bit_length()
        self.size = 1 << self._log
        self.tree = [e] * (2 * self.size)
        self._lz = [id_] * self.size

        for i in range(self.N):
            self.tree[self.size + i] = A[i]

        for i in range(self.size - 1, 0, -1):
            self._update(i)

    # A[i] = x
    def update(self, i, x):
        assert 0 <= i < self.N
        i += self.size
        for j in range(self._log, 0, -1):
            self._push(i >> j)
        self.tree[i] = x
        for j in range(1, self._log + 1):
            self._update(i >> j)

    # A[i] += x（数値を扱う場合）
    def add(self, i, x):
        self.update(i, self.get(i) + x)

    # A[i] を取得
    def get(self, i):
        assert 0 <= i < self.N
        i += self.size
        for j in range(self._log, 0, -1):
            self._push(i >> j)
        return self.tree[i]

    # [l, r) の結果
    def query(self, l, r):
        assert 0 <= l <= r <= self.N
        if l == r:
            return self._e

        l += self.size
        r += self.size

        for i in range(self._log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)

        left = self._e
        right = self._e

        while l < r:
            if l & 1:
                left = self._op(left, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                right = self._op(self.tree[r], right)
            l >>= 1
            r >>= 1

        return self._op(left, right)

    # 全体の結果
    def all(self):
        return self.tree[1]

    # 配列を表示
    def print(self):
        print(self.list_seg())

    # 配列を取得
    def list_seg(self):
        return [self.get(i) for i in range(self.N)]

    # 木の中身を表示
    def print_tree(self):
        print(self.tree)

    # 木の中身を取得
    def list_seg_tree(self):
        return self.tree.copy()

    # [l, r) に操作 f を適用
    def apply(self, l, r, f):
        assert 0 <= l <= r <= self.N
        if l == r:
            return

        l += self.size
        r += self.size

        for i in range(self._log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)

        l2, r2 = l, r

        while l < r:
            if l & 1:
                self._all_apply(l, f)
                l += 1
            if r & 1:
                r -= 1
                self._all_apply(r, f)
            l >>= 1
            r >>= 1

        l, r = l2, r2

        for i in range(1, self._log + 1):
            if ((l >> i) << i) != l:
                self._update(l >> i)
            if ((r >> i) << i) != r:
                self._update((r - 1) >> i)

    # 左端 l を固定して条件を満たす最大の右端
    def max_right(self, l, f):
        assert 0 <= l <= self.N
        assert f(self._e)

        if l == self.N:
            return self.N

        l += self.size
        for i in range(self._log, 0, -1):
            self._push(l >> i)

        sm = self._e
        first = True

        while first or (l & -l) != l:
            first = False
            while l % 2 == 0:
                l >>= 1

            if not f(self._op(sm, self.tree[l])):
                while l < self.size:
                    self._push(l)
                    l *= 2
                    if f(self._op(sm, self.tree[l])):
                        sm = self._op(sm, self.tree[l])
                        l += 1
                return l - self.size

            sm = self._op(sm, self.tree[l])
            l += 1

        return self.N

    # 右端 r を固定して条件を満たす最小の左端
    def min_left(self, r, f):
        assert 0 <= r <= self.N
        assert f(self._e)

        if r == 0:
            return 0

        r += self.size
        for i in range(self._log, 0, -1):
            self._push((r - 1) >> i)

        sm = self._e
        first = True

        while first or (r & -r) != r:
            first = False
            r -= 1
            while r > 1 and r % 2:
                r >>= 1

            if not f(self._op(self.tree[r], sm)):
                while r < self.size:
                    self._push(r)
                    r = 2 * r + 1
                    if f(self._op(self.tree[r], sm)):
                        sm = self._op(self.tree[r], sm)
                        r -= 1
                return r + 1 - self.size

            sm = self._op(self.tree[r], sm)

        return 0

    def _update(self, k):
        self.tree[k] = self._op(
            self.tree[2 * k],
            self.tree[2 * k + 1]
        )

    def _all_apply(self, k, f):
        self.tree[k] = self._mapping(f, self.tree[k])
        if k < self.size:
            self._lz[k] = self._composition(f, self._lz[k])

    def _push(self, k):
        self._all_apply(2 * k, self._lz[k])
        self._all_apply(2 * k + 1, self._lz[k])
        self._lz[k] = self._id


"""
LSeg(A, op, e, mapping, composition, id_)

op(a,b)           : 区間情報の結合
e                 : opの単位元
mapping(f,x)      : xに操作fを適用
composition(f,g)  : gの後にfを適用
id_               : 何もしない操作

update(i,x)       : 1点代入
add(i,x)          : 1点加算（数値用）
get(i)            : 1点取得
query(l,r)        : 区間取得
all()             : 全体取得
apply(l,r,f)      : 区間更新
max_right(l,f)    : 条件を満たす最大の右端
min_left(r,f)     : 条件を満たす最小の左端
print()           : 配列表示
list_seg()        : 配列取得
print_tree()      : 木の内部表示
list_seg_tree()   : 木の内部配列取得

# 区間加算 + 区間最小値
# op = min
# e = INF
# mapping = lambda f,x: x+f
# composition = lambda f,g: f+g
# id_ = 0

※ 区間は[l,r)
※ mapping等は操作に応じて変更
※ max_right/min_leftは判定の単調性が必要
"""


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

    # [追加] 左端lを固定して条件を満たす最大の右端を取得
    # f(query(l,r)) == True となる最大のr
    # O(logN)
    def max_right(self, l, f):
        assert 0 <= l <= self.N
        assert f(self.e)

        if l == self.N:
            return self.N

        l += self.size
        sm = self.e

        first = True
        while first or (l & -l) != l:
            first = False
            while l % 2 == 0:
                l >>= 1

            if not f(self.func(sm, self.tree[l])):
                while l < self.size:
                    l *= 2
                    if f(self.func(sm, self.tree[l])):
                        sm = self.func(sm, self.tree[l])
                        l += 1
                return l - self.size

            sm = self.func(sm, self.tree[l])
            l += 1

        return self.N

    # [追加] 右端rを固定して条件を満たす最小の左端を取得
    # f(query(l,r)) == True となる最小のl
    # O(logN)
    def min_left(self, r, f):
        assert 0 <= r <= self.N
        assert f(self.e)

        if r == 0:
            return 0

        r += self.size
        sm = self.e

        first = True
        while first or (r & -r) != r:
            first = False
            r -= 1
            while r > 1 and r % 2:
                r >>= 1

            if not f(self.func(self.tree[r], sm)):
                while r < self.size:
                    r = 2 * r + 1
                    if f(self.func(self.tree[r], sm)):
                        sm = self.func(self.tree[r], sm)
                        r -= 1
                return r + 1 - self.size

            sm = self.func(self.tree[r], sm)

        return 0

