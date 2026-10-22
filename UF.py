class UF:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.n = n
        self.cnt = n  # 連結成分数

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx
        self.size[rx] += self.size[ry]

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        self.cnt -= 1
        return True

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def get_size(self, x):
        return self.size[self.find(x)]

    def count(self):
        return self.cnt

    def get_parent(self):
        return [self.find(i) for i in range(self.n)]

    def groups(self):
        res = {}
        for i in range(self.n):
            r = self.find(i)
            if r not in res:
                res[r] = []
            res[r].append(i)
        return list(res.values())

    def members(self, x):
        r = self.find(x)
        return [i for i in range(self.n) if self.find(i) == r]

    def all_same(self):
        return self.cnt <= 1

    """
    UF lib

    uf = UF(n)          # n個の頂点で初期化
    uf.find(x)          # xの根を取得
    uf.union(x, y)      # xとyを連結（連結済みならFalse、新たに連結したらTrue）
    uf.same(x, y)       # xとyが同じ集合に属するか判定
    uf.get_size(x)      # xが属する集合のサイズを取得
    uf.count()          # 連結成分の個数（根の数）を取得
    uf.get_parent()     # 全頂点の根をリストで取得
    uf.groups()         # 連結成分ごとに頂点をまとめたリストを取得
    uf.members(x)       # xと同じ集合に属する頂点をリストで取得
    uf.all_same()       # 全頂点が連結しているか判定（n=0の場合もTrue）
    """
