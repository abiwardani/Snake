import random as rd
import time

#---Define board---

class Snake:
    def __init__(self,Map=[['X' for i in range(20)] for j in range(20)]):
        self.map = Map
        self.size = (20,20)
        self.fmap = [[0 for i in range(20)] for j in range(20)]
        self.apple = self.food()
        self.score = 5
        self.skip = 0

    def restart(self):
        self.size = (20,20)
        self.map = [['X' for i in range(20)] for j in range(20)]
        self.map[11] = ['X','X','X','X','X','X','X','X','X','X',5,4,3,2,1,'X','X','X','X','X']
        self.fmap = [[0 for i in range(20)] for j in range(20)]
        self.apple = self.food()
        self.score = 5
        self.skip = 0
        return None
    
    #---Define random---

    @staticmethod
    def rd():
        return int(rd.random()*18)+1
    
    @staticmethod
    def rdir(dir):
        c = rd.random()
        if c > 0.6:
            i = int(rd.random()*4)
            return ['U','R','D','L'][i]
        else:
            return dir
    
    @staticmethod
    def rdir2(dir):
        c = rd.random()
        dirs = ['U','R','D','L']
        while True:
            i = int(c*4)
            if dirs[i] != dir:
                return dirs[i]
            else:
                c = rd.random()
    
    def mprint(self):
        for i in range(20):
            for j in range(20):
                k = self.map[i][j]
                if k == 'X':
                    if self.fmap[i][j] == 1:
                        print('Ó', end=' ')
                    else:
                        print(' ', end=' ')
                else:
                    h = self.head()
                    if k == self.map[h[0]][h[1]]:
                        print('O', end=' ')
                    else:
                        print('#', end=' ')
            print()
        return None
    
    def food(self):
        x = Snake.rd()
        y = Snake.rd()
        while self.fmap[y][x] == 0:
            u = self.map[y-1][x-1:x+2] + self.map[y][x-1:x+2] + self.map[y+1][x-1:x+2]
            if u.count('X') == 9:
                self.fmap[y][x] = 1
                return (y,x)
            else:
                x = Snake.rd()
                y = Snake.rd()
    
    def next(self):
        for i in range(20):
            for j in range(20):
                if self.map[i][j] != 'X':
                    self.map[i][j] -= 1
                
                if self.map[i][j] == 0:
                    self.map[i][j] = 'X'
        return None
    
    def mUp(self,i,j):
        v = self.map[i][j]
        if self.valid('U'):
            if self.fmap[i][j] != 1:
                self.map[i-1][j] = v+1
                self.next()
                return True
            else:
                self.map[i-1][j] = v+1
                self.fmap[i][j] = 0
                self.apple = self.food()
                self.score += 1
                return True
        else:
            return False

    def mLeft(self,i,j):
        v = self.map[i][j]
        if self.valid('L'):
            if self.fmap[i][j] != 1:
                self.map[i][j-1] = v+1
                self.next()
                return True
            else:
                self.map[i][j-1] = v+1
                self.fmap[i][j] = 0
                self.apple = self.food()
                self.score += 1
                return True
        else:
            return False
        
    def mDown(self,i,j):
        v = self.map[i][j]
        if self.valid('D'):
            if self.fmap[i][j] != 1:
                self.map[i+1][j] = v+1
                self.next()
                return True
            else:
                self.map[i+1][j] = v+1
                self.fmap[i][j] = 0
                self.apple = self.food()
                self.score += 1
                return True
        else:
            return False
        
    def mRight(self,i,j):
        v = self.map[i][j]
        if self.valid('R'):
            if self.fmap[i][j] != 1:
                self.map[i][j+1] = v+1
                self.next()
                return True
            else:
                self.map[i][j+1] = v+1
                self.fmap[i][j] = 0
                self.apple = self.food()
                self.score += 1
                return True
        else:
            return False
        
    def head(self):
        max = 1
        (i,j) = (0,0)
        for k in range(20):
            for l in range(20):
                if self.map[k][l] != 'X':
                    if self.map[k][l] > max:
                        max = self.map[k][l]
                        (i,j) = (k,l)
        return (i,j)
        
    def move(self,dir):
        (x,y) = self.head()
        v = False
        if dir == 'U':
            v = self.mUp(x,y)
        elif dir == 'R':
            v = self.mRight(x,y)
        elif dir == 'D':
            v = self.mDown(x,y)
        elif dir == 'L':
            v = self.mLeft(x,y)
        if v:
            return True
        else:
            return False
    
    def seek(self,dir):
        u = self.fmap
        y = self.head()[0]
        x = self.head()[1]
        if dir == 'U':
            f = [u[i][x] for i in range(0,y)]
            if 1 in f:
                return dir
        elif dir == 'L':
            f = u[y][0:x]
            if 1 in f:
                return dir
        elif dir == 'D':
            f = [u[i][x] for i in range(y-1,20)]
            if 1 in f:
                return dir
        elif dir == 'R':
            f = u[y][x-1:20]
            if 1 in f:
                return dir
        
        f = [[u[i][j] for j in range(x-2,x+3) if j >= 0 and j < 20] for i in range(y-2,y+3) if i >= 0 and i < 20]
        got = False
            
        for i in f:
            for j in i:
                if j == 1:
                    p = i.index(j)
                    got = True
                    break
            if got:
                q = f.index(i)
                break
        
        if got:
            if dir == 'U' or dir == 'D':
                if p > 2:
                    return 'R'
                else:
                    return 'L'
            elif dir == 'R' or dir == 'L':
                if q > 2:
                    return 'D'
                else:
                    return 'U'
        else:
            return Snake.rdir(dir)
    
    def valid(self,dir):
        u = self.map
        (i,j) = self.head()
        if dir == 'U':
            if i > 0:
                if self.map[i-1][j] == 'X':
                    return True
                else:
                    return False
            else:
                return False
        elif dir == 'L':
            if j > 0:
                if self.map[i][j-1] == 'X':
                    return True
                else:
                    return False
            else:
                return False
        elif dir == 'D':
            if i+1 < 20:
                if self.map[i+1][j] == 'X':
                    return True
                else:
                    return False
            else:
                return False
        elif dir == 'R':
            if j+1 < 20:
                if self.map[i][j+1] == 'X':
                    return True
                else:
                    return False
            else:
                return False
    
    def home(self,dir):
        u = self.fmap
        (q1,p1) = self.head()
        (q,p) = self.apple
        
        if dir == 'U' or dir == 'D':
            if p == p1:
                if q < q1:
                    return 'U'
                elif q > q1:
                    return 'D'
                else:
                    return dir
            elif p < p1:
                return 'L'
            else:
                return 'R'
        elif dir == 'R' or dir == 'L':
            if q == q1:
                if p > p1:
                    return 'R'
                elif p < p1:
                    return 'L'
                else:
                    return dir
            elif q < q1:
                return 'U'
            else:
                return 'D'

    def crun(self,safety_bar,skip_limit):
        print('\n'*100)
        d = self.home(self.home('L'))
        case = True
        c = 0
        
        while case:
            print(chr(27)+"[2J")
            
            if self.score > safety_bar:
                if self.skip < skip_limit:
                    d = self.home(d)
                
            b = True
            o = []
            
            while b:
                dirs = ['U','L','D','R']
                
                if self.skip >= 3 and len(o) > 0:
                    if self.skip == 3:
                        self.skip += 1
                    
                    if self.valid(d):
                        case = self.move(d)
                        self.skip -= 0.21
                        b = False
                    else:
                        o += d
                        d = Snake.rdir2(d)
                if b:
                    for i in dirs:
                        if d == i:
                            if self.valid(d):
                                case = self.move(d)
                                d = self.home(d)
                                b = False
                                self.skip = 0
                                c = 0
                            elif self.skip <3:
                                d = self.home(d)
                                if self.valid(d):
                                    case = self.move(d)
                                    d = self.home(d)
                                    b = False
                                    self.skip = 0
                                    c = 0
                                else:
                                    o += d
                                    self.skip += 1
                                    
                                    if len(o) >= 10:
                                        if d == self.seek(d):
                                            d = Snake.rdir2(d)
                                    else:
                                        d = self.seek(d)
                                    
                            else:
                                o += d
                                self.skip += 1
                                
                                if len(o) >= 10:
                                    if d == self.seek(d):
                                        d = Snake.rdir2(d)
                                else:
                                    d = self.seek(d)
                
                if len(o) >= 50:
                    if len(set(o)) == 4:
                        if c > 4:
                            b = False
                            case = False
                        else:
                            self.skip = 0
                            b = False
                            case = True
                            o = []
                            c += 1
                            d = 'U'
                    else:
                        d = Snake.rdir2(d)
                
            self.mprint()
            print()
            print('Your score is:', self.score)

            time.sleep(0.05)
        
        if case == False:
            print()
            print('[GAME OVER]')
            return self.score