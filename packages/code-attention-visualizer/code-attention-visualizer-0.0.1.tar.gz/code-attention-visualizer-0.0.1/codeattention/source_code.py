"""Class to represent some source code."""

import json

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from matplotlib.pyplot import imshow
from pkg_resources import resource_filename

from .viz_token import FlexibleVisualToken


class SourceCode(object):
    """Class to represent some source code."""

    def __init__(self, file_with_tokens, join_sequence=None):
        """Initialize the source code representation.

        - file_with_tokens: str
            path to a json file containing tokens in this form:
            [
                {'t': 'def', 'i': 0, 'l': 1, 'c': 0},
                {'t': 'hello', 'i': 1, 'l': 1, 'c': 4, 'si': 0, 'd': 2},
                {'t': 'python', 'i': 1, 'l': 1, 'c': 10, 'si': 1, 'd': 2},
                {'t': '(', 'i': 2, 'l': 1, 'c': 16},
                ...
            ]
            where:
                - 't' key contains the string reperesentation of the token,
                - 'i' key contains the major index position of the token,
                - 'si' key contains the minor index position (si = subindex),
                - 'l' key contains the line number of the token,
                - 'c' key contains the column number of the token.
                - 'd' key contains the number of other tokens sharing the same
                  index
        - join_sequence: str
            (used in the string representation of the source code)
            a string to join the tokens within the same major index.
            in the example above, the join_sequence='_' would create a string
            representation of the source code like this:
            "def hello_python( ..."
        """
        self.tokens = json.loads(open(file_with_tokens, 'r').read())
        self.join_sequence = join_sequence

    def __str__(self):
        """Return a string representation of the source code."""
        string_reperesentation = ''
        col = 0
        line = 0
        for token in self.tokens:
            # reach the location of the token
            while line < token['l']:
                string_reperesentation += '\n'
                line += 1
                col = 0
            while col < token['c']:
                string_reperesentation += ' '
                col += 1
            string_reperesentation += token['t']
            col += len(token['t'])
            line += token['t'].count('\n')
            # check if the character will be followed by another subtoken
            if (
                    ("si" in token.keys()) and
                    (self.join_sequence is not None) and
                    token['d'] - token["si"] > 1
                ):
                string_reperesentation += self.join_sequence
                col += len(self.join_sequence)

        return string_reperesentation

    def show_with_weights(self, weights, squares=None, named_color='green'):
        """Show the source code colored according to the weights.

        Parameters:
            - named_color: str
                name of the color to use for the source code
            - weights: list of floats (required)
                list of weights for each token. The higher the more intense the
                color is. In this example the first token is the one with a
                darker shade, while the last token will be completely white.
                weights=[10,5,6,7,3,1]
            - squares: list of floats (default: None)
                one-hot encoding to decide wether some tokens should be
                surrounded by a red square. In this example the first and last
                tokens will be surrounded by a square:
                squares=[1,0,0,0,0,1]
        """
        # PREPARE IMAGE
        path_font_file = resource_filename("codeattention", "assets/FreeMono.ttf")
        surce_code_content = self.__str__()
        # img_name = folder + data['id'] + data['rawdictionarykey'][1:] + '.png'

        ratio = (8.4/14)
        char_height = 20
        char_width = char_height * ratio

        # compute max width and height required
        lines = surce_code_content.splitlines()
        lines_len = [len(line) for line in lines]
        max_width = int(max(lines_len) * char_width)
        max_height = int(char_height * len(lines))

        img = Image.new('RGB', (max_width, max_height), color=(255, 255, 255))
        fnt = ImageFont.truetype(path_font_file, char_height)
        drw = ImageDraw.Draw(img, 'RGBA')
        drw.text((0, 0), surce_code_content, font=fnt, fill=(0, 0, 0))
        # CAN BE DELAYED AT AFTER TOKEN DRAWING img.save(img_name)

        # check clicked tokens to draw squares around them
        if squares is not None:
            squared_tokens = np.array(squares)
            squared_tokens_indices = np.where(squared_tokens == 1)[0].tolist()
        else:
            squared_tokens_indices = []

        # INSTANTIATE TOKENS
        # get the positon form the metadata of tokens
        viz_tokens = []
        # DEBUG print(tokens)
        # DEBUG print(formattedcode)
        for i, t in enumerate(self.tokens):
            # print(t)
            new_token = \
                FlexibleVisualToken(
                    index_id=t['i'],
                    text=t['t'],
                    x=char_width * int(t['c']),
                    y=char_height * int(t['l']),
                    width=char_width * len(t['t']),
                    height=char_height,
                    clicked=(i in squared_tokens_indices))
            viz_tokens.append(new_token)

        # COMPUTE ATTENTION
        global_attention = 1
        # compute attention
        for att, viz_token in zip(weights, viz_tokens):
            viz_token.add_attention(att)

        # COMPUTE REFERENCE ATTENTION TO RESCALE
        # sum all the attention received by the tokens
        global_attention = 0
        attentions = []
        for viz_token in viz_tokens:
            attentions.append(viz_token.attention)
        global_attention = max(attentions) * 1.33

        # check user was right to decide the color of the tokens (red vs green)
        # correct_answered decides the color
        for viz_token in viz_tokens:
            # print(token)
            viz_token.draw_PIL(drw, global_attention, named_color)

        # img.save(img_name)
        # return img_name
        imshow(np.asarray(img))
        fig = plt.gcf()
        # print(f'max_width: {max_width}')
        # print(f'max_width: {max_height}')
        FACTOR = 60
        fig.set_size_inches(max_width / FACTOR, max_height / FACTOR)

        ax = plt.gca()
        return fig, ax
