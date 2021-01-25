from py3pin.Pinterest import Pinterest
import requests
import os
import secret_account_info as sai

def download_image(url, path):
    print("Downloading " + url)
    r = requests.get(url=url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def dump_pin(file, pin):
    url = pin['images']['orig']['url']
    title = pin['grid_title']
    if len(title) < 1:
        title = pin['title']
    description = pin['description']
    link = ''
    if pin['link'] is None:
        link = ''
    else:
        link = pin['link']
    pin_html = '<a href="' + link + '">' + title + '<img src="' + url + '"></img><p>' + description + '</p></a>' + '\r\n'
    file.write(pin_html)

def fetch_pins(file, board):
    # get all pins for the board
    board_pins = []
    pin_batch = pinterest.board_feed(board_id=board['id'])

    while len(pin_batch) > 0:
        board_pins += pin_batch
        pin_batch = pinterest.board_feed(board_id=board['id'])

    for pin in board_pins:
        if pin['type'] == 'pin':
            dump_pin(file, pin)

def print_board(board):
    print('Board: ' + board['name'] + ' ')
    print('Pin count: ' + str(board['pin_count']) + ' ')
    print('Section count: ' + str(board['section_count']) + ' ')

def dump_board(file, board):
    if board['owner']['username'] == sai.USER:
        print_board(board)
        title = '<h1>' + str(board['name']) + '</h1>'
        data = '<div>' + str(board['pin_count']) + ' pins</div>'
        data += '<div>' + str(board['section_count']) + ' sections</div>'
        board_data = title + data + '\r\n'
        file.write(board_data)
        fetch_pins(file, board)

pinterest = Pinterest(email=sai.EMAIL,
                      password=sai.PWD,
                      username=sai.USER,
                      cred_root='cred_root')

# your boards
boards = pinterest.boards()

file = open('./index.html', "w+", encoding="utf-8")
file.write('<html lang="en"><head><meta charset="UTF-8"><title>Pinterest Archive</title></head><body>\r\n')
for board in boards:
    dump_board(file, board)
    file.flush()

file.write('</body>')
file.close()

