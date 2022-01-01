import snake as s

#---Test snake program---

board = s.Snake()
board.map[11] = ['X','X','X','X','X','X','X','X','X','X',5,4,3,2,1,'X','X','X','X','X']
gmax = 0
recap = []
repeat = 3
safety_bar = 15
skip_limit = 3
max = 0

for _ in range(repeat):
    score = board.crun(safety_bar,skip_limit)
    recap.append(score)
    
    board.restart()

print("Scores:", recap)
print()