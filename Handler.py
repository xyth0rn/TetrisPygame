import config


def getCellsAbsolutePosition(piece):
    '''取得方塊當前所有方格的座標'''
    return [(y + piece.y, x + piece.x) for y, x in piece.getCells()]


def fixPiece(shot, piece):
    '''固定已落地的方塊，並且在main中自動切到下一個方塊'''
    piece.is_fixed = True
    for y, x in getCellsAbsolutePosition(piece):
        shot.status[y][x] = 2
        shot.color[y][x] = piece.color

# 向左移動
def moveLeft(shot, piece):
    for y, x in getCellsAbsolutePosition(piece):
        if x == 0 or shot.status[y][x-1] == 2:
            return
    
    piece.x -= 1
    pass

# 向右移動
def moveRight(shot, piece):
    for y, x in getCellsAbsolutePosition(piece):
        if x+1 == config.columns or shot.status[y][x+1] == 2:
            return
    piece.x += 1
    pass

# 使方塊下落一格
def drop(shot, piece):
    # print('dropping')
    for y, x in getCellsAbsolutePosition(piece):
        if y>=0:
            if y+1 == config.rows or shot.status[y+1][x] == 2 :
                fixPiece(shot, piece)
                return
    piece.y += 1
    pass

# 瞬間掉落
def instantDrop(shot, piece):
    # print('instant')
    ymax=config.rows
    while True:
        for y, x in getCellsAbsolutePosition(piece):
            if y+1==ymax or shot.status[y+1][x]==2 :
               fixPiece(shot,piece)
               return
        piece.y+=1
    return

# 旋轉方塊
def rotate(shot, piece):
    # print('rotate')
    piece.rotation+=1
    for y, x in getCellsAbsolutePosition(piece):
        if 0<y<config.rows and 0<x<config.columns :
            if shot.status[y][x] == 2 :
                piece.rotation -= 1
                break
        else:
            piece.rotation -= 1
            break
    return


# 判斷是否死掉（出局）
def isDefeat(shot, piece):
    for y, x in getCellsAbsolutePosition(piece):
        if y==0 and shot.status[y][x]==2 :
            # print('stop! y=', y, 'x=', x)
            return True
    return False

def erase(shot, y, x):
    for i in range(y-1, -1, -1):
            for j in range(config.columns):
                # print(i, j)
                if shot.status[i][j] == 2:
                    shot.status[i+1][j] = 2
                    shot.color[i+1][j] = shot.color[i][j]
                    shot.status[i][j] = 0

# 消去列 UNDONE UNDONE UNDONE UNDONE
def eliminateFilledRows(shot, piece):
    org = shot.line_count

    for y in range(config.rows):
        flag = False
        for x in range(config.columns):
            if shot.status[y][x] == 0:
                flag = False
                break
            else:
                flag = True
        
        if flag:
            for x in range(config.columns):
                shot.status[y][x] = 0
            erase(shot, y, x)
            shot.line_count += 1

    # shot.score += config.score_count[ (shot.line_count - org) ]
    cnt = shot.line_count - org
    if cnt > 0:
        shot.score += config.score_count[cnt]
    pass
