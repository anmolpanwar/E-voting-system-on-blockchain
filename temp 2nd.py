n = int(input())
m = int(input())
movecount = 0
chess = []
piece = []
for i in range(n):
    row = list(map(str, input().strip()))
    for j in row:
        if j=='.':
            continue

        elif j=='Q':
            piece.append({'name':'Q', 'x':j, 'y':i})

        elif j=='B':
            piece.append({'name':'B', 'x':j, 'y':i})

        else:
            piece.append({'name':'R', 'x':j, 'y':i})
    chess.append(row)


def queen(m,n,x,y,px,py):
    while()
