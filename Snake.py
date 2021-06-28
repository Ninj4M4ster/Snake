import tkinter as tk
import random


def lengthen_snake(snake_list, x, y):
    global game_frame
    n = len(snake_list) - 1
    snake_list.append(tk.Label(game_frame, width=2, height=1, bg="green"))
    snake_list[n + 1].place(x=x, y=y)


def create_coordinates_table():
    table = []
    for i in range(63):
        tmp = []
        for j in range(26):
            tmp.append((4 + i * 22, 4 + j * 23))
        table.append(tmp)
    return table


def create_snake(game_frame, coordinates):
    global direction
    snake_list = []
    position_y = random.choice([i for i in range(4, 21)])
    position_x = random.choice([i for i in range(4, 55)])
    if position_x < 32:
        direction = (22, 0)
    else:
        direction = (-22, 0)
    for i in range(5):
        snake_list.append(tk.Label(game_frame, width=2, height=1, bg="green"))
    snake_list[0].place(x=coordinates[position_x][position_y][0], y=coordinates[position_x][position_y][1])
    i = 1
    while i < len(snake_list):
        snake_list[i].place(x=coordinates[position_x][position_y][0] - direction[0] * i,
                            y=coordinates[position_x][position_y][1] - direction[1] * i)
        i += 1
    return snake_list


def move(snake_list, root):
    global snake_move_id
    global apple
    global apple_position
    global game_frame
    end = False
    if int(snake_list[0].place_info()['x']) + direction[0] < 4 \
            or int(snake_list[0].place_info()['x']) + direction[0] > 1368 or \
            int(snake_list[0].place_info()['y']) + direction[1] < 4 \
            or int(snake_list[0].place_info()['y']) + direction[1] > 579:
        stop(root)
        end = True
    else:
        first_pos_x = int(snake_list[0].place_info()['x']) + direction[0]
        first_pos_y = int(snake_list[0].place_info()['y']) + direction[1]
        for widget in snake_list:
            if int(widget.place_info()['x']) == first_pos_x\
                    and int(widget.place_info()['y']) == first_pos_y:
                stop(root)
                end = True
    if not end:
        i = len(snake_list) - 1
        tmp_x = int(snake_list[i].place_info()['x'])
        tmp_y = int(snake_list[i].place_info()['y'])
        while i > 0:
            snake_list[i].place(x=int(snake_list[i-1].place_info()['x']),
                                y=int(snake_list[i-1].place_info()['y']))
            i -= 1
        snake_list[0].place(x=int(snake_list[0].place_info()['x']) + direction[0],
                            y=int(snake_list[0].place_info()['y']) + direction[1])
        if int(snake_list[0].place_info()['x']) == apple_position[0] and \
                int(snake_list[0].place_info()['y']) == apple_position[1]:
            game_frame.delete('apple')
            lengthen_snake(snake_list, tmp_x, tmp_y)
            place_apple(snake_list)
            score_text = score.get().split()
            score_text[1] = str(int(score_text[1]) + 1)
            score.set(' '.join(score_text))

        snake_move_id = root.after(150, move, snake_list, root)


def stop(root):
    global total_end
    total_end = True
    root.after_cancel(snake_move_id)
    print("stopped the snake")


def change_direction(new_direction, snake_list, root):
    global game_frame
    global score
    global total_end
    global direction
    global end
    global snake_move_id
    if not total_end:
        changed = False
        if new_direction == "n":
            if direction != (0, 23) and direction != (0, 23):
                direction = (0, -23)
                changed = True
        elif new_direction == 's':
            if direction != (0, -23) and direction != (0, 23):
                direction = (0, 23)
                changed = True
        elif new_direction == 'e':
            if direction != (-22, 0) and direction != (22, 0):
                direction = (22, 0)
                changed = True
        elif new_direction == "w":
            if direction != (22, 0) and direction != (-22, 0):
                direction = (-22, 0)
                changed = True
        if not changed:
            pass
        else:
            root.after_cancel(snake_move_id)
            end = False
            if int(snake_list[0].place_info()['x']) + direction[0] < 4 \
                    or int(snake_list[0].place_info()['x']) + direction[0] > 1368 or \
                    int(snake_list[0].place_info()['y']) + direction[1] < 4 \
                    or int(snake_list[0].place_info()['y']) + direction[1] > 579:
                stop(root)
                end = True
            else:
                first_pos_x = int(snake_list[0].place_info()['x']) + direction[0]
                first_pos_y = int(snake_list[0].place_info()['y']) + direction[1]
                for widget in snake_list:
                    if int(widget.place_info()['x']) == first_pos_x \
                            and int(widget.place_info()['y']) == first_pos_y:
                        stop(root)
                        end = True
            if not end:
                i = len(snake_list) - 1
                tmp_x = int(snake_list[i].place_info()['x'])
                tmp_y = int(snake_list[i].place_info()['y'])
                while i > 0:
                    snake_list[i].place(x=int(snake_list[i - 1].place_info()['x']),
                                        y=int(snake_list[i - 1].place_info()['y']))
                    i -= 1
                snake_list[0].place(x=int(snake_list[0].place_info()['x']) + direction[0],
                                    y=int(snake_list[0].place_info()['y']) + direction[1])
                if int(snake_list[0].place_info()['x']) == apple_position[0] and \
                        int(snake_list[0].place_info()['y']) == apple_position[1]:
                    game_frame.delete('apple')
                    lengthen_snake(snake_list, tmp_x, tmp_y)
                    place_apple(snake_list)
                    score_text = score.get().split()
                    score_text[1] = str(int(score_text[1]) + 1)
                    score.set(' '.join(score_text))
                snake_move_id = root.after(150, move, snake_list, root)

def place_apple(snake_list):
    global game_frame
    global coordinates
    occupied_positions = []
    free_positions = []
    for part in snake_list:
        x = int(part.place_info()['x'])
        y = int(part.place_info()['y'])
        occupied_positions.append((x,y))
    for position in coordinates:
        if position not in occupied_positions:
            free_positions.append(position)
    global apple_position
    global game_frame
    apple_position = random.choice(random.choice(free_positions))
    game_frame.create_oval(apple_position[0], apple_position[1], apple_position[0] + 20, apple_position[1]+21,
                                   fill='red', tags='apple')


def start(snake_list, root, coordinates, start_button):
    start_button.destroy()

    global score
    score = tk.StringVar()
    score.set("Score: 0")

    global upper_frame
    score_label = tk.Label(upper_frame, textvariable=score, height=2, width=12, bg='#616361', fg='#25b825', relief='ridge')
    score_label.pack()

    place_apple(snake_list)
    move(snake_list, root)
    global total_end
    total_end = False

    root.bind("w", lambda e: change_direction("n", snake_list, root))
    root.bind("s", lambda e: change_direction("s", snake_list, root))
    root.bind("d", lambda e: change_direction("e", snake_list, root))
    root.bind("a", lambda e: change_direction("w", snake_list, root))

    root.bind("<Up>", lambda e: change_direction("n", snake_list, root))
    root.bind("<Down>", lambda e: change_direction("s", snake_list, root))
    root.bind("<Right>", lambda e: change_direction("e", snake_list, root))
    root.bind("<Left>", lambda e: change_direction("w", snake_list, root))


def create_game():
    root = tk.Tk()
    root.title("Snake")

    # height of one piece - 20
    # length of one piece - 21
    # first coordinate - (4,4)
    # last coordinate - (1368,579)
    # places in a row - 63
    # places in a column - 26
    global direction
    direction = random.choice([(0, 23), (22, 0), (0, -23), (-22, 0)])

    global coordinates
    coordinates = create_coordinates_table()

    global upper_frame
    upper_frame = tk.Frame(root, bg='#353738')
    upper_frame.pack()

    title = tk.Label(upper_frame, text="Snake 1.0", width=198, height=5, bg='#353738', fg='#25b825')
    title.pack()
    start_button = tk.Button(upper_frame, text="Start game", width=12, height=2, bg='#616361', fg='#25b825',
                             command=lambda: start(snake_list, root, coordinates, start_button))
    start_button.pack()

    global game_frame
    game_frame = tk.Canvas(root, width=1388, height=600, highlightthickness=2, highlightbackground="black", bg='#1b1c1b')
    game_frame.pack()

    snake_list = create_snake(game_frame, coordinates)

    root.mainloop()


if __name__ == '__main__':
    create_game()
