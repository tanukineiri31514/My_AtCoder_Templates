### glaf

def bfs(pos):
    dist[pos] = 0
    q = deque([pos])
    while q:
        np = q.popleft()
        for nx in grid[np]:
            if dist[nx] == -1:
                dist[nx] = dist[np]+1
                q.append(nx)



### grid

def bfs(pos):
    x,y = pos
    vis[x][y] = 0
    q = deque([pos])
    while q:
        x,y = q.popleft()
        for nx,ny in move4:
            if 0<=nx+x<h and 0<=ny+y<w:
                if grid[nx+x][ny+y] == "." and vis[nx+x][ny+y] == -1:
                    vis[nx+x][ny+y] = vis[x][y]+1
                    q.append((nx+x,ny+y))

### dijkstra

def dks(pos):
    # graf[i] = (pos, dist)
    q = [(0, pos)]
    dist[pos] = 0
    while q:
        d, p = pop(q)
        if d > dist[p]:
            continue
        for ps, w in graf[p]:
            nd = d + w
            if dist[ps] > nd:
                dist[ps] = nd
                push(q, (nd, ps))