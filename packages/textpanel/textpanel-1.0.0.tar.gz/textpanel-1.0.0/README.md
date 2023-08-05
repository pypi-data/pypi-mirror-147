# textpanel
> Create boxes in the terminal.

Python port of [boxen](https://github.com/sindresorhus/boxen)
## Install
```bash
pip install textpanel
```

## Usage
```python
from textpanel import panel

print(panel("Hello World!",padding=1))
#╭──────────────╮
#│              │
#│ Hello World! │
#│              │
#╰──────────────╯

print(panel("Hello World!", padding=1, title='title'))
#╭───── title ──────╮
#│                  │
#│   Hello World!   │
#│                  │
#╰──────────────────╯
```

## API

### panel(text, style?, padding?, margin?, width?, expand?, border_color?, text_alignment?, text_color?, border?, title?, title_alignment?)

#### text
*Required*\
Type: `string`\
Text inside the box

#### border_style
Type: `string | dict`\
Default: `single`\
Values:
- `'single'`
```text
┌───┐
│foo│
└───┘
```
- `'double'`
```text
╔═══╗
║foo║
╚═══╝
```
- `'round'`
```text
╭───╮
│foo│
╰───╯
```
- `'bold'`
```text
┏━━━┓
┃foo┃
┗━━━┛
```
- `'single-double'`
```text
╓───╖
║foo║
╙───╜
```
- `'double-single'`
```text
╒═══╕
│foo│
╘═══╛
```
- `'classic'`
```text
+---+
|foo|
+---+
```
- `'arrow'`
```text
↘↓↓↓↙
→foo←
↗↑↑↑↖
```
Box border style

Can be custom defined with a dict:
```python
{
    "topLeft": "┌",
    "topRight": "┐",
    "bottomRight": "┘",
    "bottomLeft": "└",
    "left": "│",
    "right": "│",
    "top": "─",
    "bottom": "─"
}
```
#### title 
Type: `str`\
Display a title at the top of the box.

#### title_alignment
Type: `str`\
Default: `left`\
Values: `left` `center` `right`\
Align the title in the top bar.

- `'left'`
```text
┌ title ────────┐
│foo bar foo bar│
└───────────────┘
```
- `'center'`
```text
┌──── title ────┐
│foo bar foo bar│
└───────────────┘
```
- `'right'`
```text
┌──────── title ┐
│foo bar foo bar│
└───────────────┘
```

#### padding
Type: `number`\
Default: `0`\
Space between the text and box border.

#### margin
Type: `number`\
Default: `0`\
Space around the box.

#### width 
Type: `number`\
Default: `0`\
Width of the box.

#### expand 
Type: `bool`\
Default: `False`\
Expand the box to the terminal width.

#### border_color
Type: `str`\
Values: `"black"` `"red"` `"green"` `"orange"` `"blue"` `"purple"` `"cyan"` `"lightgrey"` `"darkgrey"` `"lightred"` `"lightgreen"` `"yellow"` `"lightblue"` `"pink"` `"lightcyan"`\
Color of the box border.

#### text_alignment
Type: `str`\
Default: `left`\
Values: `left` `center` `right`\
Alignment of the text inside the box.

#### text_color
Type: `str`\
Values: `"black"` `"red"` `"green"` `"orange"` `"blue"` `"purple"` `"cyan"` `"lightgrey"` `"darkgrey"` `"lightred"` `"lightgreen"` `"yellow"` `"lightblue"` `"pink"` `"lightcyan"`\
Color of the text inside the box.
