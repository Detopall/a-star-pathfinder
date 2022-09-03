import pygame
from queue import PriorityQueue
from spot_class import *
from draw_grid import *
from main import *

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1-x2) + abs(y1-y2)


def algorithm_a_star(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}

	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)
		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			start.make_start()
			return True
		
		for neighbour in current.neighbours:
			temp_g_score = g_score[current] + 1
			if temp_g_score < g_score[neighbour]:
				came_from[neighbour] = current
				g_score[neighbour] = temp_g_score
				f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
				if neighbour not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbour], count, neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open()
		draw()
		if current != start:
			current.make_closed()



def reconstruct_path(came_from, currentNode, draw):
	while currentNode in came_from:
		currentNode = came_from[currentNode]
		currentNode.make_path()
		draw()