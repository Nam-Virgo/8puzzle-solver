import tkinter as tk
import time
import math
from tkinter import messagebox, ttk
from collections import deque
import heapq
import random
from collections import deque
import threading

# Thuật toán BFS (Breadth First Search)
def bfs(start, goal):
    print("\n🔍 Đang chạy BFS...")
    queue = deque([(start, [])])
    visited = set()
    visited.add(tuple(map(tuple, start)))

    while queue:
        state, path = queue.popleft()
        if state == goal:
            return path
        zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
        moves = get_valid_moves(zero_pos)

        for move in moves:
            new_state = swap_tiles([row[:] for row in state], zero_pos, move)
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple not in visited:
                visited.add(state_tuple)
                queue.append((new_state, path + [new_state]))
    return None


# Thuật toán DFS (Depth First Search)
def dfs(start, goal, max_depth=50):
    print("\n🔍 Đang chạy DFS...")
    for depth in range(max_depth):
        result = limited_dfs(start, goal, [], depth)
        if result is not None:
            return result
    return None

def limited_dfs(state, goal, path, depth):
    if state == goal:
        return path
    if depth == 0:
        return None

    zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
    moves = get_valid_moves(zero_pos)

    for move in moves:
        new_state = swap_tiles([row[:] for row in state], zero_pos, move)
        if new_state not in path:
            new_path = path + [new_state]
            result = limited_dfs(new_state, goal, new_path, depth - 1)
            if result is not None:
                return result
    return None

# Thuật toán IDS (Iterative Deepening Search)
def ids(start, goal, max_depth=50):
    print("\n🔍 Đang chạy IDS...")
    for depth in range(max_depth):
        visited = set()
        result = limited_dfs_ids(start, goal, [], depth, visited)
        if result is not None:
            return result
    return None

def limited_dfs_ids(state, goal, path, depth, visited):
    if state == goal:
        return path
    if depth == 0:
        return None

    state_tuple = tuple(map(tuple, state))  # Chuyển state thành dạng hashable để lưu vào set
    if state_tuple in visited:
        return None
    visited.add(state_tuple)

    zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
    moves = get_valid_moves(zero_pos)

    for move in moves:
        new_state = swap_tiles([row[:] for row in state], zero_pos, move)
        if new_state not in path:
            new_path = path + [new_state]
            result = limited_dfs_ids(new_state, goal, new_path, depth - 1, visited)
            if result is not None:
                return result
    return None

# Thuật toán UCS (Uniform Cost Search)
def ucs(start, goal):
    print("\n🔍 Đang chạy UCS...")
    priority_queue = [(0, start, [])]  # (Chi phí, trạng thái, đường đi)
    visited = set()
    visited.add(tuple(map(tuple, start)))

    while priority_queue:
        cost, state, path = heapq.heappop(priority_queue)
        if state == goal:
            return path
        zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
        moves = get_valid_moves(zero_pos)

        for move in moves:
            new_state = swap_tiles([row[:] for row in state], zero_pos, move)
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple not in visited:
                visited.add(state_tuple)
                heapq.heappush(priority_queue, (cost + 1, new_state, path + [new_state]))
    return None

# Thuật toán Greedy Best-First Search
def greedy(start, goal):
    print("\n🔍 Đang chạy Greedy...")
    priority_queue = [(manhattan_distance(start, goal), start, [])]
    visited = set()
    visited.add(tuple(map(tuple, start)))

    while priority_queue:
        _, state, path = heapq.heappop(priority_queue)
        if state == goal:
            return path
        zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
        moves = get_valid_moves(zero_pos)

        for move in moves:
            new_state = swap_tiles([row[:] for row in state], zero_pos, move)
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple not in visited:
                visited.add(state_tuple)
                heapq.heappush(priority_queue, (manhattan_distance(new_state, goal), new_state, path + [new_state]))
    return None

# Thuật toán A* Search
def a_star(start, goal):
    print("\n🔍 Đang chạy A*...")
    priority_queue = [(manhattan_distance(start, goal), 0, start, [])]  # (h(n) + g(n), g(n), state, path)
    visited = set()
    visited.add(tuple(map(tuple, start)))

    while priority_queue:
        _, cost, state, path = heapq.heappop(priority_queue)
        if state == goal:
            return path
        zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
        moves = get_valid_moves(zero_pos)

        for move in moves:
            new_state = swap_tiles([row[:] for row in state], zero_pos, move)
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple not in visited:
                visited.add(state_tuple)
                new_cost = cost + 1
                priority = new_cost + manhattan_distance(new_state, goal)
                heapq.heappush(priority_queue, (priority, new_cost, new_state, path + [new_state]))
    return None

# Thuật toán IDA* (Iterative Deepening A*)
def ida_star(start, goal):
    """ Giải bài toán 8-Puzzle bằng thuật toán IDA* """
    print("\n🔵 Đang chạy IDA*...")

    def search(path, g, bound):
        state = path[-1]
        f = g + manhattan_distance(state, goal)
        if f > bound:
            return f
        if state == goal:
            return path

        min_cost = float('inf')
        zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
        moves = get_valid_moves(zero_pos)

        for move in moves:
            new_state = swap_tiles([row[:] for row in state], zero_pos, move)
            if new_state not in path:  # Tránh lặp lại trạng thái đã đi qua
                path.append(new_state)
                result = search(path, g + 1, bound)
                if isinstance(result, list):  # Tìm thấy lời giải
                    return result
                min_cost = min(min_cost, result)
                path.pop()
        return min_cost

    bound = manhattan_distance(start, goal)
    path = [start]

    while True:
        result = search(path, 0, bound)
        if isinstance(result, list):  # Nếu tìm thấy lời giải
            return result
        if result == float('inf'):
            return None  # Không tìm thấy lời giải
        bound = result  # Cập nhật giới hạn chi phí cho vòng lặp tiếp theo


# Thuật toán Simple Hill Climbing
def simple_hill_climbing(start, goal):
    print("\n🔍 Đang chạy Simple Hill Climbing...")
    current_state = start
    path = [current_state]
    visited = set()
    visited.add(tuple(map(tuple, current_state)))

    while current_state != goal:
        zero_pos = [(i, row.index(0)) for i, row in enumerate(current_state) if 0 in row][0]
        moves = get_valid_moves(zero_pos)

        # Tìm trạng thái con tốt nhất (có khoảng cách Manhattan nhỏ nhất)
        best_state = None
        best_heuristic = float('inf')

        for move in moves:
            new_state = swap_tiles([row[:] for row in current_state], zero_pos, move)
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple not in visited:
                heuristic = manhattan_distance(new_state, goal)
                if heuristic < best_heuristic:
                    best_heuristic = heuristic
                    best_state = new_state

        # Nếu không tìm thấy trạng thái con nào tốt hơn, dừng lại
        if best_state is None:
            print("❌ Đã dừng lại tại cực đại cục bộ!")
            return path

        # Chuyển sang trạng thái tốt nhất
        current_state = best_state
        visited.add(tuple(map(tuple, current_state)))
        path.append(current_state)

    return path

# Thuật toán Steepest Ascent Hill Climbing
def steepest_ascent_hill_climbing(start, goal):
    print("\n🔍 Đang chạy Steepest Ascent Hill Climbing...")
    current_state = start
    path = [current_state]
    visited = set()
    visited.add(tuple(map(tuple, current_state)))

    while current_state != goal:
        zero_pos = [(i, row.index(0)) for i, row in enumerate(current_state) if 0 in row][0]
        moves = get_valid_moves(zero_pos)

        # Tìm trạng thái con tốt nhất (có khoảng cách Manhattan nhỏ nhất)
        best_states = []
        best_heuristic = float('inf')

        for move in moves:
            new_state = swap_tiles([row[:] for row in current_state], zero_pos, move)
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple not in visited:
                heuristic = manhattan_distance(new_state, goal)
                if heuristic < best_heuristic:
                    best_heuristic = heuristic
                    best_states = [new_state]
                elif heuristic == best_heuristic:
                    best_states.append(new_state)

        # Nếu không tìm thấy trạng thái con nào tốt hơn, dừng lại
        if not best_states:
            print("❌ Đã dừng lại tại cực đại cục bộ!")
            return path

        # Chọn ngẫu nhiên một trạng thái tốt nhất để tiếp tục
        current_state = random.choice(best_states)
        visited.add(tuple(map(tuple, current_state)))
        path.append(current_state)

    return path

# Thuật toán Stochastic Hill Climbing
def stochastic_hill_climbing(start, goal, max_iterations=10000, temperature=0.1):
    print("\n🔍 Đang chạy Stochastic Hill Climbing...")
    current_state = start
    path = [current_state]
    visited = set()
    visited.add(tuple(map(tuple, current_state)))
    iteration = 0

    while current_state != goal and iteration < max_iterations:
        zero_pos = [(i, row.index(0)) for i, row in enumerate(current_state) if 0 in row][0]
        moves = get_valid_moves(zero_pos)

        # Tạo danh sách các trạng thái con (neighbors)
        neighbors = []
        heuristics = []
        for move in moves:
            new_state = swap_tiles([row[:] for row in current_state], zero_pos, move)
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple not in visited:
                neighbors.append(new_state)
                heuristics.append(manhattan_distance(new_state, goal))

        # Nếu không có trạng thái con nào, dừng lại
        if not neighbors:
            print("❌ Đã dừng lại tại cực đại cục bộ!")
            return path

        # Tính xác suất chọn từng trạng thái con
        current_heuristic = manhattan_distance(current_state, goal)
        probabilities = []
        for h in heuristics:
            delta = h - current_heuristic  # Sự thay đổi heuristic
            if delta <= 0:  # Nếu trạng thái con tốt hơn hoặc bằng
                prob = 1.0
            else:  # Nếu trạng thái con tệ hơn
                prob = math.exp(-delta / temperature)  # Xác suất chấp nhận trạng thái tệ hơn
            probabilities.append(prob)

        # Chuẩn hóa xác suất
        total_prob = sum(probabilities)
        if total_prob == 0:
            probabilities = [1/len(probabilities)] * len(probabilities)  # Nếu tất cả xác suất bằng 0, chọn ngẫu nhiên
        else:
            probabilities = [p/total_prob for p in probabilities]

        # Chọn ngẫu nhiên một trạng thái con dựa trên xác suất
        next_state = random.choices(neighbors, weights=probabilities, k=1)[0]

        # Cập nhật trạng thái hiện tại
        current_state = next_state
        visited.add(tuple(map(tuple, current_state)))
        path.append(current_state)
        iteration += 1

    if iteration >= max_iterations:
        print("❌ Đã đạt giới hạn số lần lặp!")
    return path

# Thuật toán Simulated Annealing
def simulated_annealing(start_state, goal_state):
    print("\n🔍 Đang chạy Simulated Annealing...")
    current_state = [row[:] for row in start_state]
    best_state = [row[:] for row in start_state]
    path = []
    best_path = []
    temperature = 1000.0
    min_temperature = 0.01
    max_iterations = 10000
    cooling_rate = 0.995
    max_cost = manhattan_distance(start_state, goal_state) + 10
    current_cost = manhattan_distance(current_state, goal_state)
    best_cost = current_cost
    step_count = 0
    start_time = time.time()
    timeout = 10

    moves_dict = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    def find_blank(state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j

    def is_valid(x, y):
        return 0 <= x < 3 and 0 <= y < 3

    def move_tile(state, move):
        x, y = find_blank(state)
        dx, dy = moves_dict[move]
        new_x, new_y = x + dx, y + dy
        if is_valid(new_x, new_y):
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            return new_state
        return state

    for iteration in range(max_iterations):
        if time.time() - start_time > timeout:
            break
        step_count += 1
        if current_state == goal_state:
            print(f"✅ Tìm thấy lời giải sau {step_count} bước.")
            return [start_state] + [apply_move(start_state, move) for move in path]

        x, y = find_blank(current_state)
        possible_moves = [move for move, (dx, dy) in moves_dict.items() if is_valid(x + dx, y + dy)]
        if not possible_moves:
            break

        move_confidences = []
        for move in possible_moves:
            new_state = move_tile(current_state, move)
            new_cost = manhattan_distance(new_state, goal_state)
            move_confidence = 1 / (1 + new_cost / max_cost) if max_cost > 0 else 0.0
            move_confidences.append((move_confidence, move, new_state))
        confidences = [conf for conf, _, _ in move_confidences]
        total_conf = sum(confidences)
        probabilities = [conf / total_conf if total_conf > 0 else 1 / len(possible_moves)
                         for conf in confidences]

        _, move, new_state = random.choices(move_confidences, weights=probabilities, k=1)[0]
        new_cost = manhattan_distance(new_state, goal_state)
        cost_diff = new_cost - current_cost

        if cost_diff <= 0 or random.random() < math.exp(-cost_diff / temperature):
            current_state = [row[:] for row in new_state]
            current_cost = new_cost
            path.append(move)
            if current_cost < best_cost:
                best_state = [row[:] for row in current_state]
                best_cost = current_cost
                best_path = path[:]

        temperature *= cooling_rate
        if temperature < min_temperature:
            break

    # reconstruct path
    if best_state == goal_state:
        print(f"✅ Tìm thấy lời giải sau {step_count} bước.")
        result_path = [start_state]
        temp_state = [row[:] for row in start_state]
        for move in best_path:
            temp_state = move_tile(temp_state, move)
            result_path.append(temp_state)
        return result_path

    print("❌ Không tìm thấy lời giải bằng Simulated Annealing.")
    return None

# Thuật toán Beam Search
def beam_search(start, goal, beam_width=3):
    print("\n🔍 Đang chạy Beam Search...")
    # Hàng đợi ưu tiên: (heuristic, state, path)
    queue = [(manhattan_distance(start, goal), start, [start])]
    visited = set()
    visited.add(tuple(map(tuple, start)))

    while queue:
        # Lấy top beam_width trạng thái từ hàng đợi
        current_level = []
        for _ in range(min(beam_width, len(queue))):
            if not queue:
                break
            heuristic, state, path = heapq.heappop(queue)
            current_level.append((state, path))

        # Nếu không còn trạng thái nào để khám phá
        if not current_level:
            print("❌ Không tìm thấy lời giải!")
            return None

        # Khám phá các trạng thái trong level hiện tại
        next_queue = []
        for state, path in current_level:
            if state == goal:
                print(f"✅ Tìm thấy giải pháp với beam width {beam_width}!")
                return path

            zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
            moves = get_valid_moves(zero_pos)

            for move in moves:
                new_state = swap_tiles([row[:] for row in state], zero_pos, move)
                state_tuple = tuple(map(tuple, new_state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    new_path = path + [new_state]
                    heuristic = manhattan_distance(new_state, goal)
                    heapq.heappush(next_queue, (heuristic, new_state, new_path))

        # Cập nhật hàng đợi với top beam_width trạng thái từ next_queue
        queue = []
        for _ in range(min(beam_width, len(next_queue))):
            if not next_queue:
                break
            heapq.heappush(queue, heapq.heappop(next_queue))

    print("❌ Không tìm thấy lời giải!")
    return None

'''def and_or_graph_search(start_state, goal_state):
    stack = [(start_state, [])]
    visited = set()

    while stack:
        current_state, path = stack.pop()
        state_tuple = tuple(map(tuple, current_state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if current_state == goal_state:
            return path

        for neighbor in reversed(generate_neighbors(current_state)):
            if tuple(map(tuple, neighbor)) not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None'''

# Hàm tạo trạng thái tiếp theo từ một nước đi
def apply_move(state, move):
    zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
    new_state = swap_tiles([row[:] for row in state], zero_pos, move)
    return new_state

# Hàm tạo một chuỗi nước đi ngẫu nhiên
def generate_random_moves(length):
    moves = []
    for _ in range(length):
        # Mỗi nước đi là một hướng: 0 (lên), 1 (xuống), 2 (trái), 3 (phải)
        move = random.randint(0, 3)
        moves.append(move)
    return moves

# Hàm áp dụng chuỗi nước đi vào trạng thái ban đầu
def apply_moves_to_state(start_state, moves):
    state = [row[:] for row in start_state]
    zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
    for move in moves:
        # Chuyển đổi move (0, 1, 2, 3) thành tọa độ
        x, y = zero_pos
        if move == 0 and x > 0:  # Lên
            new_pos = (x - 1, y)
        elif move == 1 and x < 2:  # Xuống
            new_pos = (x + 1, y)
        elif move == 2 and y > 0:  # Trái
            new_pos = (x, y - 1)
        elif move == 3 and y < 2:  # Phải
            new_pos = (x, y + 1)
        else:
            continue  # Bỏ qua nước đi không hợp lệ
        state = swap_tiles(state, zero_pos, new_pos)
        zero_pos = new_pos
    return state

# Thuật toán Genetic Algorithm
def genetic_algorithm(start, goal, population_size=200, max_generations=2000, max_moves=70, mutation_rate=0.2):
    print("\n🔍 Đang chạy Genetic Algorithm (nâng cấp)...")

    def fitness_function(state, moves):
        # Hàm đánh giá: càng gần goal càng tốt, ít bước càng tốt
        return manhattan_distance(state, goal) + 0.1 * len(moves)

    # Khởi tạo quần thể: mỗi cá thể là chuỗi bước đi ngẫu nhiên
    population = [generate_random_moves(random.randint(30, max_moves)) for _ in range(population_size)]

    for generation in range(max_generations):
        fitness_scores = []
        for individual in population:
            final_state = apply_moves_to_state(start, individual)
            fitness = fitness_function(final_state, individual)
            fitness_scores.append((fitness, individual))

            if final_state == goal:
                print(f"✅ Tìm thấy giải pháp ở thế hệ {generation}!")

                # Dựng lại path từ individual
                path = [start]
                current_state = [row[:] for row in start]
                for move in individual:
                    zero_pos = [(i, row.index(0)) for i, row in enumerate(current_state) if 0 in row][0]
                    x, y = zero_pos
                    if move == 0 and x > 0:
                        new_pos = (x - 1, y)
                    elif move == 1 and x < 2:
                        new_pos = (x + 1, y)
                    elif move == 2 and y > 0:
                        new_pos = (x, y - 1)
                    elif move == 3 and y < 2:
                        new_pos = (x, y + 1)
                    else:
                        continue
                    current_state = swap_tiles([row[:] for row in current_state], zero_pos, new_pos)
                    path.append(current_state)
                return path

        # Chọn 30% cá thể tốt nhất
        fitness_scores.sort(key=lambda x: x[0])
        elite_count = population_size // 3
        selected = [individual for _, individual in fitness_scores[:elite_count]]

        # Tạo thế hệ mới
        new_population = selected[:]

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]

            # Đột biến
            if random.random() < mutation_rate:
                mutation_point = random.randint(0, len(child) - 1)
                child[mutation_point] = random.randint(0, 3)

            # Cắt ngắn nếu quá dài
            if len(child) > max_moves:
                child = child[:max_moves]
            new_population.append(child)

        population = new_population

        # In thông tin debug
        if generation % 100 == 0:
            best_fitness = fitness_scores[0][0]
            print(f"📊 Thế hệ {generation} - Fitness tốt nhất: {best_fitness:.2f}")

    print("❌ Không tìm thấy lời giải sau số thế hệ tối đa.")
    return None

def bfs_belief(initial_beliefs, goal_beliefs):
    print("\n🔍 Đang chạy BFS trên Belief States...")

    def apply_action_to_belief(belief_state, action):
        next_belief = set()
        for state in belief_state:
            state_list = [list(row) for row in state]
            zero_pos = [(i, row.index(0)) for i, row in enumerate(state_list) if 0 in row][0]
            x, y = zero_pos
            dx, dy = action
            nx, ny = x + dx, y + dy

            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state_list]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                next_belief.add(tuple(map(tuple, new_state)))
            else:
                # Không di chuyển được thì giữ nguyên
                next_belief.add(state)
        return next_belief

    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    action_names = ["↑", "↓", "←", "→"]

    # Biến trạng thái ban đầu và goal thành dạng hashable
    initial_belief = set(tuple(map(tuple, s)) for s in initial_beliefs)
    goal_set = set(tuple(map(tuple, g)) for g in goal_beliefs)

    visited = set()
    visited.add(frozenset(initial_belief))
    queue = deque([(initial_belief, [])])

    MAX_DEPTH = 50
    MAX_STEPS = 1_000_000
    step_counter = 0
    max_depth_seen = 0

    while queue:
        belief_state, path = queue.popleft()
        step_counter += 1
        max_depth_seen = max(max_depth_seen, len(path))

        if step_counter % 10000 == 0:
            print(f"🔄 BFS bước {step_counter:,} – belief size: {len(belief_state)} – depth: {len(path)}")

        # Kiểm tra điều kiện dừng
        if all(s in goal_set for s in belief_state):
            print(f"✅ Tìm thấy kế hoạch sau {step_counter:,} bước duyệt – độ sâu {len(path)}.")
            return path

        if len(path) >= MAX_DEPTH:
            continue

        for i, action in enumerate(actions):
            next_belief = apply_action_to_belief(belief_state, action)
            frozen_next = frozenset(next_belief)

            if frozen_next == frozenset(belief_state):
                # Nếu không có gì thay đổi, bỏ qua
                continue

            if frozen_next not in visited:
                visited.add(frozen_next)
                queue.append((next_belief, path + [action_names[i]]))

        if step_counter >= MAX_STEPS:
            print(f"⛔ Đạt giới hạn số bước: {MAX_STEPS:,}. Dừng BFS.")
            return None

    print(f"❌ Không tìm thấy kế hoạch sau {step_counter:,} bước duyệt. Chiều sâu cao nhất: {max_depth_seen}")
    return None

# Hàm tính khoảng cách Manhattan
def manhattan_distance(state, goal):
    distance = 0
    print("State:", state)
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:  # Không tính ô trống
                goal_x, goal_y = [(x, y) for x in range(3) for y in range(3) if goal[x][y] == value][0]
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

# Hàm lấy các nước đi hợp lệ
def get_valid_moves(zero_pos):
    x, y = zero_pos
    moves = []
    if x > 0: moves.append((x - 1, y))  # Lên trên
    if x < 2: moves.append((x + 1, y))  # Xuống dưới
    if y > 0: moves.append((x, y - 1))  # Sang trái
    if y < 2: moves.append((x, y + 1))  # Sang phải
    return moves

# Hàm đổi chỗ ô trống với ô bên cạnh
def swap_tiles(state, zero_pos, move):
    x1, y1 = zero_pos
    x2, y2 = move
    state[x1][y1], state[x2][y2] = state[x2][y2], state[x1][y1]
    return state

# Lớp giao diện
class PuzzleApp:
    def __init__(self, root, initial_state, goal_state):
        self.root = root
        self.root.title("Giải bài toán 8-Puzzle")
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.steps = []
        self.step_index = 0
        self.run_history = []  # lưu lịch sử chạy

        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Board bên trái
        board_frame = tk.LabelFrame(main_frame, text="Bảng 8-Puzzle", font=("Arial", 14))
        board_frame.grid(row=0, column=0, padx=10, pady=5)

        self.grid_buttons = [[tk.Button(board_frame, text=str(initial_state[i][j]) if initial_state[i][j] != 0 else "",
                                        font=('Arial', 24), width=4, height=2, bg="#ADD8E6")
                              for j in range(3)] for i in range(3)]

        for i in range(3):
            for j in range(3):
                self.grid_buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        # Text log bên phải (có thanh cuộn)
        log_frame = tk.LabelFrame(main_frame, text="Kết quả giải", font=("Arial", 14))
        log_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")

        self.output_text = tk.Text(log_frame, width=50, height=20, font=("Courier", 10), wrap=tk.WORD)
        scrollbar = tk.Scrollbar(log_frame, command=self.output_text.yview)
        self.output_text.config(yscrollcommand=scrollbar.set)
        self.output_text.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Cấu hình tag để thêm màu
        self.output_text.tag_config("time", foreground="blue")
        self.output_text.tag_config("stepcount", foreground="purple")
        self.output_text.tag_config("header", foreground="black", font=("Courier", 10, "bold"))
        self.output_text.tag_config("step", foreground="green")
        self.output_text.tag_config("error", foreground="red")

        # Khung chọn thuật toán phía dưới
        algo_frame = tk.LabelFrame(main_frame, text="Chọn thuật toán", font=("Arial", 14))
        algo_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        buttons = [
            ("BFS", self.solve_bfs),
            ("DFS", self.solve_dfs),
            ("UCS", self.solve_ucs),
            ("IDS", self.solve_ids),
            ("Greedy", self.solve_greedy),
            ("A*", self.solve_a_star),
            ("IDA*", self.solve_ida_star),
            ("Simple HC", self.solve_simple_hill_climbing),
            ("Steepest HC", self.solve_steepest_ascent_hill_climbing),
            ("Stochastic HC", self.solve_stochastic_hill_climbing),
            ("Simulated Annealing", self.solve_simulated_annealing),
            ("Beam Search", self.solve_beam_search),
            #("And/Or Graph", self.solve_and_or_graph),
            ("Genetic", self.solve_genetic),
            ("Belief BFS", self.solve_belief_bfs),
        ]

        for i, (label, func) in enumerate(buttons):
            tk.Button(algo_frame, text=label, width=15, command=func).grid(row=i//3, column=i%3, padx=5, pady=5)

        # Label trạng thái cuối cùng + nút lịch sử
        self.status_label = tk.Label(root, text="Chọn thuật toán để giải", font=("Arial", 12), fg="blue")
        self.status_label.pack(pady=5)

        tk.Button(root, text="🧠 Belief States", command=self.open_belief_state_window).pack(pady=5)
        tk.Button(root, text="🗂️ Lịch sử chạy", command=self.show_history).pack(pady=5)

    def log(self, msg, tag=None):
        self.output_text.insert(tk.END, msg + "\n", tag)
        self.output_text.see(tk.END)

    def show_next_step(self):
        if self.step_index < len(self.steps):
            self.update_grid(self.steps[self.step_index])
            self.step_index += 1
            self.root.after(400, self.show_next_step)
        else:
            self.status_label.config(text="\u2714\ufe0f Đã giải xong!", fg="green")

    def update_grid(self, state):
        for i in range(3):
            for j in range(3):
                self.grid_buttons[i][j].config(text=str(state[i][j]) if state[i][j] != 0 else "")

    def print_solution(self, steps, runtime):
        self.log(f"⏱️ Thời gian chạy: {runtime:.4f} giây", "time")
        self.log(f"🔢 Tổng số bước: {len(steps)}", "stepcount")
        self.log("\n🔹 Các bước giải bài toán 8-Puzzle:", "header")
        for i, state in enumerate(steps):
            self.log(f"\n🟢 Bước {i+1}:", "step")
            for row in state:
                self.log(" ".join(str(n) if n != 0 else "◻" for n in row))

    def run_solver(self, solver_func, name):
        self.status_label.config(text=f"Đang chạy {name}...", fg="orange")
        self.output_text.delete(1.0, tk.END)
        start_time = time.time()
        self.steps = solver_func(self.initial_state, self.goal_state)
        runtime = time.time() - start_time
        if self.steps:
            self.step_index = 0
            self.print_solution(self.steps, runtime)
            self.show_next_step()
            self.run_history.append({
                "index": len(self.run_history) + 1,
                "algorithm": name,
                "time": f"{runtime:.4f}s",
                "steps": len(self.steps)
            })
        else:
            self.status_label.config(text="Không tìm thấy lời giải!", fg="red")
            self.log("🛑 Không tìm thấy lời giải.", "error")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("🗂️ Lịch sử chạy")
        history_window.minsize(width=600, height=300)

        tree = ttk.Treeview(history_window, columns=("Index", "Algo", "Time", "Steps"), show="headings")
        tree.column("Index", anchor="center", width=50)
        tree.column("Algo", anchor="center", width=180)
        tree.column("Time", anchor="center", width=100)
        tree.column("Steps", anchor="center", width=80)

        tree.heading("Index", text="Lần")
        tree.heading("Algo", text="Thuật toán")
        tree.heading("Time", text="Thời gian")
        tree.heading("Steps", text="Số bước")

        for entry in self.run_history:
            tree.insert("", "end", values=(entry["index"], entry["algorithm"], entry["time"], entry["steps"]))

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Các hàm tương ứng mỗi thuật toán
    def solve_bfs(self): self.run_solver(bfs, "BFS")
    def solve_dfs(self): self.run_solver(dfs, "DFS")
    def solve_ucs(self): self.run_solver(ucs, "UCS")
    def solve_ids(self): self.run_solver(ids, "IDS")
    def solve_greedy(self): self.run_solver(greedy, "Greedy")
    def solve_a_star(self): self.run_solver(a_star, "A*")
    def solve_ida_star(self): self.run_solver(ida_star, "IDA*")
    def solve_simple_hill_climbing(self): self.run_solver(simple_hill_climbing, "Simple Hill Climbing")
    def solve_steepest_ascent_hill_climbing(self): self.run_solver(steepest_ascent_hill_climbing, "Steepest Ascent Hill Climbing")
    def solve_stochastic_hill_climbing(self): self.run_solver(stochastic_hill_climbing, "Stochastic Hill Climbing")
    def solve_simulated_annealing(self): self.run_solver(simulated_annealing, "Simulated Annealing")
    def solve_beam_search(self): self.run_solver(beam_search, "Beam Search")
    #def solve_and_or_graph(self): self.run_solver(and_or_graph_search, "And/Or Graph Searching")
    def solve_genetic(self): self.run_solver(genetic_algorithm, "Genetic Algorithm")

    def solve_belief_bfs(self):
        if not hasattr(self, 'initial_beliefs') or not hasattr(self, 'goal_beliefs'):
            messagebox.showerror("❌ Lỗi", "Chưa có dữ liệu belief states. Vui lòng nhập trước.")
            return

        self.output_text.delete(1.0, tk.END)
        self.log("🚀 Đang chạy BFS trên belief states...", "header")
        self.status_label.config(text="Đang chạy BFS trên belief states...", fg="orange")

        def run_belief_bfs_in_thread():
            start_time = time.time()
            plan = bfs_belief(self.initial_beliefs, self.goal_beliefs)
            end_time = time.time()
            self.root.after(0, lambda: self.handle_belief_bfs_result(plan, start_time, end_time))

        threading.Thread(target=run_belief_bfs_in_thread).start()

    def handle_belief_bfs_result(self, plan, start_time, end_time):
        if not plan:
            self.log("❌ Không tìm thấy kế hoạch nào.", "error")
            self.status_label.config(text="Không tìm thấy kế hoạch belief.", fg="red")
            return

        self.log(f"⏱️ Thời gian chạy: {end_time - start_time:.4f} giây", "info")
        self.log(f"🔢 Tổng số bước: {len(plan)}", "info")

        self.log("\n🎯 Goal Belief States:", "info")
        for g in self.goal_beliefs:
            self.log("───")
            for row in g:
                self.log(" ".join("◻" if n == 0 else str(n) for n in row))

        belief_state = set(tuple(map(tuple, s)) for s in self.initial_beliefs)

        self.log("\n🔹 Các bước giải bài toán 8-Puzzle trên belief state:\n", "info")

        actions = {
            "↑": (-1, 0),
            "↓": (1, 0),
            "←": (0, -1),
            "→": (0, 1)
        }

        def apply_action(state, action):
            state_list = [list(row) for row in state]
            zero_pos = [(i, row.index(0)) for i, row in enumerate(state_list) if 0 in row][0]
            x, y = zero_pos
            dx, dy = action
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state_list]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                return tuple(map(tuple, new_state))
            return None

        for step_idx, move in enumerate(plan):
            self.log(f"\n🟢 Bước {step_idx + 1}: {move}", "step")
            self.log(f"Belief state hiện tại ({len(belief_state)} trạng thái):", "info")
            for state in sorted(belief_state):
                self.log("───")
                for row in state:
                    self.log(" ".join("◻" if n == 0 else str(n) for n in row))
            self.log("")

            new_belief = set()
            for state in belief_state:
                result = apply_action(state, actions[move])
                if result:
                    new_belief.add(result)
                else:
                    new_belief.add(state)
            belief_state = new_belief

        self.status_label.config(text="✅ Đã tìm được kế hoạch belief!", fg="green")

 
    def open_belief_state_window(self):
        window = tk.Toplevel(self.root)
        window.title("Nhập trạng thái niềm tin (Belief States)")
        window.geometry("800x600")

        tk.Label(window, text="Số trạng thái khởi đầu:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        initial_count_var = tk.IntVar()
        tk.Entry(window, textvariable=initial_count_var, width=5).grid(row=0, column=1)

        tk.Label(window, text="Số trạng thái đích:", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        goal_count_var = tk.IntVar()
        tk.Entry(window, textvariable=goal_count_var, width=5).grid(row=0, column=3)

        input_frame = tk.Frame(window)
        input_frame.grid(row=2, column=0, columnspan=4, pady=10)

        boards = {"initial": [], "goal": []}

        def create_input_tables():
            for widget in input_frame.winfo_children():
                widget.destroy()

            def create_board(title, index, board_type):
                frame = tk.LabelFrame(input_frame, text=f"{title} #{index+1}", padx=5, pady=5)
                frame.grid(row=index // 2, column=index % 2 + (0 if board_type == "initial" else 2), padx=5, pady=5)
                cells = []
                for i in range(3):
                    row = []
                    for j in range(3):
                        entry = tk.Entry(frame, width=3, font=("Arial", 14), justify="center")
                        entry.grid(row=i, column=j, padx=2, pady=2)
                        row.append(entry)
                    cells.append(row)
                boards[board_type].append(cells)

            for i in range(initial_count_var.get()):
                create_board("Initial State", i, "initial")
            for i in range(goal_count_var.get()):
                create_board("Goal State", i, "goal")

        def read_belief_states():
            def read_board(cells):
                board = []
                for row in cells:
                    board_row = []
                    for entry in row:
                        try:
                            val = int(entry.get())
                            if val < 0 or val > 8:
                                raise ValueError
                        except:
                            messagebox.showerror("Lỗi", "Giá trị không hợp lệ! Vui lòng nhập số từ 0 đến 8.")
                            return None
                        board_row.append(val)
                    board.append(board_row)
                return board

            initial_beliefs = []
            for cells in boards["initial"]:
                board = read_board(cells)
                if board is None:
                    return
                initial_beliefs.append(board)

            goal_beliefs = []
            for cells in boards["goal"]:
                board = read_board(cells)
                if board is None:
                    return
                goal_beliefs.append(board)

            # ✅ Lưu vào thuộc tính của lớp để dùng sau
            self.initial_beliefs = initial_beliefs
            self.goal_beliefs = goal_beliefs

            # In kiểm tra
            print("🔹 Initial Belief States:")
            for b in initial_beliefs:
                for row in b:
                    print(row)
                print()

            print("🔹 Goal Belief States:")
            for b in goal_beliefs:
                for row in b:
                    print(row)
                print()

            messagebox.showinfo("✅ Thành công", f"Đã lưu {len(initial_beliefs)} initial và {len(goal_beliefs)} goal states.")

        tk.Button(window, text="Khởi tạo bảng nhập", command=create_input_tables).grid(row=1, column=0, columnspan=4, pady=5)
        # Placeholder button để sau này chạy thuật toán
        tk.Button(window, text="Đọc Belief States", command=read_belief_states).grid(row=99, column=0, columnspan=4, pady=10)

# Chạy chương trình
if __name__ == "__main__":
    initial_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]  # 0 là ô trống
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    root = tk.Tk()
    app = PuzzleApp(root, initial_state, goal_state)
    root.mainloop()
