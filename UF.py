class UF:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
    
    def get_size(self, x):
        return self.size[self.find(x)]
    """
        UF lib
        uf = UF(n)          # init
        uf.find(x)          # xの根を取得
        uf.union(x, y)      # xとyを連結
        uf.get_size(x)      # xが属する集合のサイズ
    """
