import itertools, random, time, matplotlib,sys
import matplotlib.pyplot as plt

"Do not mistake the repeated entries in 'Pre' to assume that the algorithm goes to the same node twice. It is because when the weight patterns are changed and the new tour appended to the previous tour, it begins from the node where it left of in the previous graph and hence the repetition. this bug has to be fixed."

def greedy_tsp(G, tour=0):
	print('here')
 	
	Pre = tour
	print(Pre)
	print(Pre[-1])
	Curr = Pre[-1]
	print('Curr')
	print(Curr)
	Tree = []
	Distance = 0

	while len(Pre)<=len(G):
		print(len(Pre))
		print(len(G))
		for u in range(len(G)):
			Tree.append(Curr)
			chng=raw_input('Want to change weight patterns? Enter Y or N.')
			if chng=='Y' or chng=='y':
				print(Tree)
				return Tree
			else:
				Dis = float("inf")
				for v in range(len(G[u])):
					if Curr == v or v in Pre:
						continue
					else:
						if G[Curr][v] < Dis and G[Curr][v]!=0:
							Dis = G[Curr][v]
							Next = v
						else:
							continue
					Distance += Dis
				Pre.append(Curr)
				Curr = Next
	#print(Distance)
	print(Tree)
	print(Pre)
	return Pre