# coding: utf-8
# only support python2
# TODO support Chinese...
#import uniout # support list output chinese, sudo pip install uniout
import Image, ImageFont, ImageDraw
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

FONT = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"

# print "make sure the file your want to convert in the same path."
# filename = raw_input("input the filename you want to convert: ")
filename = 'chinese.txt'
with open(filename) as f:
    lines = f.readlines()

inputfile = u""
for line in lines:
    uni_line = unicode(line,"utf-8")
    inputfile += uni_line

print inputfile

font = ImageFont.truetype(FONT, 16)

# output = filename.split('.')[0] + '.png'
output = 'chinese.png'

def text2png(inputfile, output, fontpath=None,
             fontsize=16, color='#000', bgcolor='#FFF',
             leftpadding=5, rightpadding=5, out_put_width=350):
    # set up fonts
    if fontpath == None:
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(FONT, fontsize)

    # set up footnotes
    foot_note = 'created by Python via PIL'
    fontfoot_note = ImageFont.truetype(FONT, 18)
    foot_note_width = fontfoot_note.getsize(foot_note)[0]
    foot_note_height= fontfoot_note.getsize(foot_note)[1]

    # image line length
    fixed_size = out_put_width - leftpadding - rightpadding
    # image width
    img_width = out_put_width
    text = inputfile

    lines = process_text(text, fixed_size)
    for line in lines:
        # print  str(line).decode('string_escape')
        print line

    line_height = font.getsize(text)[1]
    img_height = line_height * (len(lines) + 3)

    img = Image.new("RGBA", (img_width, img_height), bgcolor)
    draw = ImageDraw.Draw(img)

    # draw text line
    y = 0
    for line in lines:
        draw.text( (leftpadding, y), line, color, font=font )
        y += line_height
    draw.text( (img_width - foot_note_width, img_height - foot_note_height),
               foot_note,color, font)
    img.save(output)


def process_text(text, fixed_size):
    # state flag
    in_word = False
    lines = []
    line = u""
    word = u""
    for char in text:
        print char
        print 'line is:', line
        print 'lines is:', lines
        num = ord(char.decode('utf-8'))
        print num
        if num < 128:
            lines, line, word, in_word = parse_ascii(char,
                                                     fixed_size,
                                                     lines,
                                                     line,
                                                     word,
                                                     in_word)
        else:
            lines, line = parse_chinese(char, fixed_size, lines, line)

    return lines

def parse_chinese(char, fixed_size, lines, line):
    if font.getsize(line)[0] <= fixed_size:
        if char != '\n':
            line += char
        else:
            lines.append(line)
            line = u""
    else:
        lines.append(line)
        line = char
    return lines, line


def parse_ascii(char, fixed_size, lines, line, word, in_word):
    if font.getsize(line+word)[0] <= fixed_size:
        if char != '\n':
            if char == ' ':
                in_word = False
                line += word
                word = u""
                # join space
                line += char
            else:
                in_word = True
                word += char
        # meet LF
        else:
            in_word = False
            line += word
            word = u""
            lines.append(line)
            line = u""
    # > fixed_size should append
    else:
        # last char was space or LF
        if in_word == False:
            # word can be add to line
            line += word
            # replace word with new char
            word = char
            lines.append(line)
            line = u""
        # last char was not space or LF
        else:
            # add char to current word and keep it
            word += char
            lines.append(line)
            line = u""
    return lines, line, word, in_word


if __name__ == "__main__":
    text2png(inputfile, output, FONT)
