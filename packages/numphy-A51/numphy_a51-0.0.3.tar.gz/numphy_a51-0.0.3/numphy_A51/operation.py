def ailabs():
    lab = input()

    if lab == 'ailab1':
        code =   """
                # DFS
                def dfs(graph, start, visited=None):

                    if visited is None:
                        visited = set()  # Initialize visited set if not provided

                    # Mark the current node as visited
                    visited.add(start)
                    print(start, end=" ")  # Print the node

                    # Recur for all the adjacent vertices
                    for neighbor in graph[start]:
                        if neighbor not in visited:
                            dfs(graph, neighbor, visited)
                    
                    return visited


                # Example graph represented as an adjacency list
                graph = {
                    'A': ['B', 'C'],
                    'B': ['A', 'D', 'E'],
                    'C': ['A', 'F'],
                    'D': ['B'],
                    'E': ['B', 'F'],
                    'F': ['C', 'E']
                }

                # Call DFS
                print("DFS Traversal:")
                dfs(graph, 'A')
                """
        return code

    if lab == 'ailab2':
            code =   """
                    from collections import deque

                    def bfs(graph, start):

                        visited = set()  # Track visited nodes
                        queue = deque([start])  # Initialize queue with the starting node
                        visited_order = []  # To store the order of visited nodes

                        while queue:
                            # Dequeue a node
                            current = queue.popleft()

                            # If not visited, process the node
                            if current not in visited:
                                visited.add(current)
                                visited_order.append(current)
                                print(current, end=" ")  # Print the node

                                # Enqueue all unvisited neighbors
                                for neighbor in graph[current]:
                                    if neighbor not in visited:
                                        queue.append(neighbor)

                        return visited_order


                    # Example graph represented as an adjacency list
                    graph = {
                        'A': ['B', 'C'],
                        'B': ['A', 'D', 'E'],
                        'C': ['A', 'F'],
                        'D': ['B'],
                        'E': ['B', 'F'],
                        'F': ['C', 'E']
                    }

                    # Call BFS
                    print("BFS Traversal:")
                    bfs(graph, 'A')
                    """
            return code
        
    else:
        return "The correct format: eg:- ailab1, please check the format of input"
