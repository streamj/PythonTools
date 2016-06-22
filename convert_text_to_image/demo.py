# coding: utf-8
# only support python2
import Image, ImageFont, ImageDraw


FONT = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
# inputfile = u'welcome to free lancer web site, www.freelancer.com'

inputfile = u""
with open('demo.txt') as f:
    lines = f.readlines()
for line in lines:
    inputfile += line
print inputfile
font = ImageFont.truetype(FONT, 16)
output = 'demo.png'

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

    lines = []
    line = u""

    # image line length
    fixed_size = out_put_width - leftpadding - rightpadding
    # image width
    img_width = out_put_width

    REPLACE = u'\uFFFD'
    NEWLINE_REPLACEMENT = ' ' + REPLACE + ' '
    # replace the LF, or they will be ignored during the spilt
    text = inputfile.replace('\n', NEWLINE_REPLACEMENT)

    for word in text.split():
        # if meet LF
        if word == REPLACE:
            # add to list as  a new output line,slice the beginning ' '
            lines.append(line[1:])
            line = u""
            lines.append(line)
        # current line + a space + a single word <= image line length
        elif font.getsize(line + ' ' + word)[0] <= fixed_size:
            # line growth
            line += ' ' + word
        # if not LF and > fixed width
        else:
            # also add to list as a new output line, slice the beginning ' '
            lines.append(line[1:])
            line = u""
            line += ' ' + word

    # if still something left behind:
    if len(line) != 0:
        lines.append(line[1:])

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


text2png(inputfile, output, FONT)
