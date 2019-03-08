"""Sudoku solver example."""

from z3 import Distinct, sat, Solver

from example_context import grilops


def main():
  """Sudoku solver example."""
  givens = [
      [5, 3, 0, 0, 7, 0, 0, 0, 0],
      [6, 0, 0, 1, 9, 5, 0, 0, 0],
      [0, 9, 8, 0, 0, 0, 0, 6, 0],
      [8, 0, 0, 0, 6, 0, 0, 0, 3],
      [4, 0, 0, 8, 0, 3, 0, 0, 1],
      [7, 0, 0, 0, 2, 0, 0, 0, 6],
      [0, 6, 0, 0, 0, 0, 2, 8, 0],
      [0, 0, 0, 4, 1, 9, 0, 0, 5],
      [0, 0, 0, 0, 8, 0, 0, 7, 9],
  ]

  solver = Solver()
  sym = grilops.make_number_range_symbol_set(1, 9)
  sg = grilops.SymbolGrid(9, 9, sym, solver)

  for given_row, grid_row in zip(givens, sg.grid):
    for given, grid_cell in zip(given_row, grid_row):
      if given != 0:
        solver.add(grid_cell == sym[given])

  for y in range(9):
    solver.add(Distinct(*sg.grid[y]))

  for x in range(9):
    solver.add(Distinct(*[r[x] for r in sg.grid]))

  for z in range(9):
    top = (z // 3) * 3
    left = (z % 3) * 3
    cells = [r[x] for r in sg.grid[top:top + 3] for x in range(left, left + 3)]
    solver.add(Distinct(*cells))

  result = solver.check()
  if result != sat:
    print(result)
  else:
    sg.print()


if __name__ == "__main__":
  main()
