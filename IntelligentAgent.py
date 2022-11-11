import math
import time

from BaseAI import BaseAI
class IntelligentAgent(BaseAI):

    def getMove(self, grid):
        start_time = time.time()
        self.overtime = False
        move = self.maximize(grid, -math.inf, math.inf, 1, 4, start_time)

        # if (time.time() - start_time >= 0.20):
        #     print("overtime")
        #     return None

        return move

    def minimize(self, grid, alpha, beta, depth, max_depth, start_time):

        empty = grid.getAvailableCells()
        if(len(empty) == 0 or depth == max_depth ):
            return None, self.eval(grid)
        if (time.time() - start_time >= 0.15):
            return None, self.eval(grid)
        else:
            minExpected = math.inf
            for a in grid.getAvailableCells():
                clone2 = grid.clone()
                clone4 = grid.clone()
                sum2 = 0
                sum4 = 0
                if a and grid.canInsert(a):
                    clone2.setCellValue(a, 2)
                    if time.time() - start_time >= 0.15:
                        return None, self.eval(grid)
                    max2 = self.maximize(clone2, alpha, beta, depth+1, max_depth, start_time)
                    if time.time() - start_time >= 0.15:
                        return None, self.eval(grid)
                    sum2 += max2[1]

                    clone4.setCellValue(a, 4)
                    max4 = self.maximize(clone4, alpha, beta, depth+1, max_depth, start_time)
                    if time.time() - start_time >= 0.15:
                        return None, self.eval(grid)
                    sum4 += max4[1]
                expected = 0.9*sum2 + 0.1*sum4
                if (time.time() - start_time >= 0.15):
                    return newGrid, minExpected
                if expected < minExpected:
                    newGrid = a
                    minExpected = expected

                if minExpected <= alpha:
                    break
                if minExpected < beta:
                    beta = minExpected
            # print("Computer: ", minExpected)
            return newGrid, minExpected

    def maximize(self, grid, alpha, beta, depth, max_depth, start_time):
        if (not grid.canMove() or depth == max_depth or depth != 1 and time.time() - start_time >= 0.15 ):
            # self.overtime = True
            return None, self.eval(grid)

        else:
            pos_moves = grid.getAvailableMoves()

            maxVal = -math.inf
            move = pos_moves[0]
            if time.time() - start_time >= 0.15:
                return move[0]
            moved_grid = grid
            for m in pos_moves:
                moved_grid = m[1]
                val = self.minimize(moved_grid.clone(), alpha, beta, depth+1, max_depth, start_time)[1]
                if val > maxVal:
                    maxVal = val
                    move = m
                    moved_grid = m[1]
                if(time.time() - start_time >= 0.15):
                    return move[0]
                if maxVal >= beta:
                    break
                if maxVal > alpha:
                    alpha = maxVal

            if depth == 1 or time.time() - start_time >= 0.15:
                return move[0]
            return moved_grid, maxVal

    #evaluation function
    def eval(self, grid):
        return self.monotonicity(grid) + 50*len(grid.getAvailableCells()) - self.smoothness(grid) + grid.getMaxTile() + 100* self.max_tile_position(grid)

    # heuristics
    def max_tile_position(self, grid):
        maxTile = grid.getMaxTile()
        if grid.getCellValue((0, 0)) == maxTile or grid.getCellValue((0, 3)) == maxTile or grid.getCellValue((3, 3)) == maxTile or grid.getCellValue((3, 0)) == maxTile:
            return 1
        return 0
    def adjacent_equals(self, grid):
        gridNums = grid.map
        diff = 0
        for i in range(grid.size):
            for j in range(grid.size-1):
                if gridNums[i][j] == gridNums[i][j+1]:
                    diff += 1
        for i in range(grid.size-1):
            for j in range(grid.size):
                 if(gridNums[i][j] == gridNums[i+1][j]):
                     diff += 1
        return diff
    def smoothness(self, grid):
        gridNums = grid.map
        diff = 0
        for i in range(grid.size):
            for j in range(grid.size-1):
                diff += abs(gridNums[i][j] - gridNums[i][j+1])
        for i in range(grid.size-1):
            for j in range(grid.size):
                diff += abs(gridNums[i][j] - gridNums[i+1][j])
        return diff
    def monotonicity(self, grid):
        gridNums = grid.map
        diff = 0
        for i in range(grid.size):
            sign = gridNums[i][0] - gridNums[i][1]
            for j in range(grid.size-1):
                newSign = gridNums[i][j]-gridNums[i][j+1]
                if(sign * newSign > 0):
                    diff += 1
                sign = newSign
        for i in range(grid.size):
            sign = gridNums[0][i] - gridNums[1][i]
            for j in range(grid.size-1):
                newSign = gridNums[j][i]-gridNums[j+1][i]
                if(sign * newSign > 0):
                    diff += 1
                sign = newSign
        return diff


