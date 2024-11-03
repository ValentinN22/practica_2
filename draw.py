from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4



def game(c, board):
    cell_size = 40
    start_x = (letter[0] - (11 * cell_size)) / 2
    start_y = (letter[1] - (11 * cell_size)) / 2
    candy_colors = {1:colors.red, 2:colors.yellow, 3:colors.green, 4:colors.blue, 0:colors.white}
    for row in range(len(board)):
        for col in range(len(board)):
            color = candy_colors[board[row][col]]
            c.setFillColor(color)
            y_position = start_y + (len(board) - row - 1)* cell_size
            c.rect(start_x + col * cell_size, y_position, cell_size, cell_size, fill=1)


def games_2_pdf(c, game_grid, message):
    c.drawString(100, 750, message)
    game(c, game_grid)
    c.showPage()
