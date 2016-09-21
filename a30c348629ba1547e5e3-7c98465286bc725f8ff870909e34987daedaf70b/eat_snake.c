// This is a simple game: eat snake.
// Use h,j,k,l to control the snake. 
// Maybe you can use this game to practise vim control
//
#include <string.h>
#include <stdlib.h>
#include <curses.h>
#include <term.h>
#include <unistd.h>
#include <sys/select.h>
#include <sys/time.h>
#include <sys/types.h>

enum Direction {
    DIR_INVALID = 0,
    DIR_UP = 1,
    DIR_DOWN = 2,
    DIR_LEFT = 3,
    DIR_RIGHT = 4,
};

// Some char 
const char BORDER_UP_DOWN = '-';
const char BORDER_LEFT_RIGHT = '|';
const char BORDER_CORNER = '+';
const char BORDER_SPACE = ' ';
const char SNAKE_BODY = '*';
const char SNAKE_HEAD = '@';
const char BEAN = '*';

// Command to control snake
const char CMD_UP = 'k';
const char CMD_DOWN = 'j';
const char CMD_LEFT = 'h';
const char CMD_RIGHT = 'l';

static char s_map[100][100];
static Direction s_dir_map[100][100];

static int s_num_row = 20;
static int s_num_column = 20;

static int s_head_x = 5;
static int s_head_y = 7;
static int s_tail_x = 5;
static int s_tail_y = 5;

// Old termios used to change term back
static struct termios old_ios;

// Counter for move snake
int s_move_counter = 0;
// frequence for sanke move
int s_move_freq = 20;

// Clear screen
char TERM_CAP_CLEAR[] = "clear";
// cursor down 1 line
char TERM_CAP_CUD1[] = "cud1";
// cursor posistion to row #1 and column #2
char TERM_CAP_CUP[] = "cup";

struct TermCmd {
    char cmd[64];
    int len;
};

// CMD_STR
static struct TermCmd s_term_cmd_clear;
static struct TermCmd s_term_cmd_cud1;
static struct TermCmd s_term_cmd_cup;

void clear_scr() {
    write(1, s_term_cmd_clear.cmd, s_term_cmd_clear.len);
}

void cur_down_one() {
    write(1, s_term_cmd_cud1.cmd, s_term_cmd_cud1.len);
}

void cur_goto(int x, int y) {
    char* cmd = tparm(s_term_cmd_cup.cmd, x, y);
    write(1, cmd, strlen(cmd));
}

void teardown_env() {
    tcsetattr(0, TCSANOW, &old_ios);
}

void setup_env() {
    struct termios new_ios;
    tcgetattr(0, &old_ios);
    new_ios = old_ios;
    new_ios.c_iflag &= ~ICRNL;
    new_ios.c_lflag &= ~(ICANON | ECHO | ISIG | ECHOE);
    // ios.c_oflag &= ~ONLCR;
    tcsetattr(0, TCSANOW, &new_ios);

    // Get Terminal cmd
    int error;
    setupterm(NULL, 0, &error);

    char* tmp_cmd = tigetstr(TERM_CAP_CLEAR);
    strcpy(s_term_cmd_clear.cmd, tmp_cmd);
    s_term_cmd_clear.len = strlen(tmp_cmd);
    
    tmp_cmd = tigetstr(TERM_CAP_CUD1);
    strcpy(s_term_cmd_cud1.cmd, tmp_cmd);
    s_term_cmd_cud1.len = strlen(tmp_cmd);

    tmp_cmd = tigetstr(TERM_CAP_CUP);
    strcpy(s_term_cmd_cup.cmd, tmp_cmd);
    s_term_cmd_cup.len = strlen(tmp_cmd);
}

void drow_border_up_down() {
    char ch = BORDER_CORNER;
    write(1, &ch, 1);
    for (int j = 0; j < s_num_column; ++j) {
        char ch = BORDER_UP_DOWN;
        write(1, &ch, 1);
    }
    ch = BORDER_CORNER;
    write(1, &ch, 1);
}

void draw_border() {
    drow_border_up_down();
    cur_down_one();
    for (int i = 0; i < s_num_row; ++i) {
        char ch = BORDER_LEFT_RIGHT;
        write(1, &ch, 1);
        for (int j = 0; j < s_num_column; ++j) {
            ch = BORDER_SPACE;
            write(1, &ch, 1);
        }
        ch = BORDER_LEFT_RIGHT;
        write(1, &ch, 1);
        // Down one line
        cur_down_one();
    }
    drow_border_up_down();
    cur_down_one();
}

void random_star() {
    int new_x = 0;
    int new_y = 0;
    do {
        new_x = random() % s_num_row;
        new_y = random() % s_num_column;
    } while (s_map[new_x][new_y] != BORDER_SPACE);

    s_map[new_x][new_y] = BEAN;
}

void init_snake() {
    for (int i = 0; i < s_num_row; ++i) {
        for (int j = 0; j < s_num_column; ++j) {
            s_map[i][j] = BORDER_SPACE;
            s_dir_map[i][j] = DIR_INVALID;
        }
    }
    s_map[5][5] = SNAKE_BODY;
    s_dir_map[5][5] = DIR_RIGHT;
    s_map[5][6] = SNAKE_BODY;
    s_dir_map[5][6] = DIR_RIGHT;
    s_map[5][7] = SNAKE_HEAD;
    s_dir_map[5][7] = DIR_RIGHT;

    random_star();
}

void draw_snake() {
    for (int i = 0; i < s_num_row; ++i) {
        cur_goto(i + 1, 1);
        for (int j = 0; j < s_num_column; ++j) {
            write(1, &s_map[i][j], 1);
        }
    }
    cur_goto(s_num_row + 2, 0);
}

void init() {
    setup_env();
    clear_scr();
    draw_border();
    init_snake();
    draw_snake();
    atexit(teardown_env);
}

void change_dir(Direction dir) {
    int old_dir = s_dir_map[s_head_x][s_head_y];
    if (old_dir == dir) {
        return;
    }
    if (old_dir == DIR_UP && dir == DIR_DOWN) {
        return;
    }
    if (old_dir == DIR_DOWN && dir == DIR_UP) {
        return;
    }
    if (old_dir == DIR_LEFT && dir == DIR_RIGHT) {
        return;
    }
    if (old_dir == DIR_RIGHT && dir == DIR_LEFT) {
        return;
    }
    s_dir_map[s_head_x][s_head_y] = dir;
}

bool input_available() {
    fd_set readfds;

    FD_ZERO(&readfds);
    FD_SET(0, &readfds);

    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = 0;
    int ret = select(1, &readfds, NULL, NULL, &tv);
    switch (ret) {
    case 1:
        // Input
        return true;
    }
    return false;
}

void handle_input() {
    int ch = getchar();
    switch(ch) {
    case CMD_UP:
        change_dir(DIR_UP);
        break;
    case CMD_DOWN:
        change_dir(DIR_DOWN);
        break;
    case CMD_LEFT:
        change_dir(DIR_LEFT);
        break;
    case CMD_RIGHT:
        change_dir(DIR_RIGHT);
        break;
    default:
        break;
    }
}

void try_input() {
    bool handle = false;
    while (input_available()) {
        // Discard
        handle_input();
        // getchar();
    }
}

void change_pos(int *pos_x, int *pos_y, Direction dir) {
    switch (dir) {
    case DIR_UP:
        *pos_x -= 1;
        break;
    case DIR_DOWN:
        *pos_x += 1;
        break;
    case DIR_LEFT:
        *pos_y -= 1;
        break;
    case DIR_RIGHT:
        *pos_y += 1;
        break;
    default:
        break;
    }
}

int check_pos() {
    return 0;
}

bool is_bean(int x, int y) {
    return s_map[x][y] == BEAN && s_dir_map[x][y] == DIR_INVALID;
}

bool is_crash(int x, int y) {
    return x < 0 || y < 0 || x >= s_num_row || y >= s_num_column
            || (s_map[x][y] != BORDER_SPACE && s_dir_map[x][y] != DIR_INVALID);
}

void game_over() {
    clear_scr();
    cur_goto(1, 1);
    printf("Game Over!\n");
    getchar();
    exit(-1);
}

// Return true if eat a star
void update_head() {
    bool is_eat = false;
    int new_x = s_head_x;
    int new_y = s_head_y;

    change_pos(&new_x, &new_y, s_dir_map[new_x][new_y]);
    if (is_bean(new_x, new_y)) {
        is_eat = true;
    } else if (is_crash(new_x, new_y)) {
        game_over();
    }

    s_map[s_head_x][s_head_y] = SNAKE_BODY;
    s_dir_map[new_x][new_y] = s_dir_map[s_head_x][s_head_y];
    if (is_eat) {
        // Eat one bean
        s_map[new_x][new_y] = SNAKE_BODY;

        change_pos(&new_x, &new_y, s_dir_map[new_x][new_y]);
        s_map[new_x][new_y] = SNAKE_HEAD;
        s_dir_map[new_x][new_y] = s_dir_map[s_head_x][s_head_y];

        // rand
        random_star();
    } else {
        s_map[new_x][new_y] = SNAKE_HEAD;
    }

    s_head_x = new_x;
    s_head_y = new_y;
}

void update_tail() {
    int new_x = s_tail_x;
    int new_y = s_tail_y;

    change_pos(&new_x, &new_y, s_dir_map[s_tail_x][s_tail_y]);
    s_map[s_tail_x][s_tail_y] = BORDER_SPACE;
    s_dir_map[s_tail_x][s_tail_y] = DIR_INVALID;

    s_tail_x = new_x;
    s_tail_y = new_y;
}

// Change the sanke in memory
// Return True if need redraw sanke, ohterwise false
bool move_snake() {
    s_move_counter++;
    if (s_move_counter == s_move_freq) {
        s_move_counter = 0;
        // Try get input
        try_input();
        // Update 
        update_head();
        update_tail();
        return true;
    }
    return false;
}

void refresh_screen() {
    if (move_snake()) {
        draw_snake();
    }
}

int main() {
    init();
    while (1) {
        refresh_screen();
        usleep(10 * 1000);
    }
    return 0;
}
