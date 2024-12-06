# Telegram Markdown text

[![PyPI version](https://img.shields.io/pypi/v/telegram-markdown-text.svg)](https://pypi.org/project/telegram-markdown-text/)
[![Python version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)

**Python модуль, що був створений для спрощення роботи з MarkdownV2 при написанні телеграм бота. Основною ідеєю було
створити щось схоже на StringBuilder з мови програмування Kotlin.**

### Установка

Встановити можна командою `pip install telegram-markdown-text`.

### Як юзать?

Модуль підтримує усі доступні стилі з `MarkdownV2` описані
в [офіційній документації](https://core.telegram.org/bots/api#markdownv2-style)

```python
from telegram_markdown_text import *

Bold('Жирний текст')
# *Жирний текст*

Italic('Курсив')
# _Курсив_

Underline('Підкреслений текст')
# __Підкреслений текст__

Strikethrough('Закреслений текст')
# ~Закреслений текст~

Spoiler('Спойлер')
# ||Спойлер||

InlineUrl('Якась лінка', 'https://test.url')
# [Якась лінка](https://test.url)

InlineUser('Лінка на юзера', 123456)
# [Лінка на юзера](tg://user?id=123456)

Emoji('👍', 123456)
# [👍](tg://emoji?id=123456)

InlineCode('Відформатований рядок коду')
# `Відформатований рядок коду`

InlineCodeBlock('Відформатований блок коду з підсвіткою синтаксису', 'kotlin')
# ```kotlin
# Відформатований блок коду з підсвіткою синтаксису
# ````

QuoteBlock('Цитата')
# ```kotlin
# >Цитата**
# ````

PlainText('Просто текст')
# Просто текст
```

Варіант використання `MarkdownText` з `append()`

```python
from telegram_markdown_text import *

text = MarkdownText()
text.append('Простий текст ')
text.append(Bold('з жирними текстом'))
text.append(Italic(' та курсивом'))
print(text)

# Простий текст *з жирним текстом* та курсивом
```

Варіант використання з додаванням `+`

```python
from telegram_markdown_text import *

text = PlainText('Простий текст ') + Bold('з жирними текстом') + Italic(' та курсивом')
print(text)

# Простий текст *з жирним текстом* та курсивом
```

Варіант вкладання тексту одного стилю в інший

```python
from telegram_markdown_text import *

text = Bold((Italic('Жирний курсив') + ' та ' + Underline('жирний андерлайн')))
print(text)

# *Жирний курсив та __жирний андерлайн__*
```

Якщо `.append()` викликати на якомусь конкретному елементі, а не на `MarkdownText`, то доданий текст просто стане його
частиною і повторить його стиль

```python
from telegram_markdown_text import *

text = Bold('Жирний текст').append(' та такий же жирний текст')
print(text)

# *Жирний текст та такий же жирний текст*
```

### Цитати

Через особливотсі Telegram API, цитати автоматичного огортаються символом нового рядка `\n`

Використання цитати в якості окремого повідомлення

```python
from telegram_markdown_text import *

text = QuoteBlock("Процитований текст\nв два рядки")
```

Використання цитати в середині повідомлення

```python
from telegram_markdown_text import *

text = MarkdownText()
text.append('Початок повідомлення')
# Цитата завжди буде починатись з нового рядка
text.append(QuoteBlock("Процитований текст\nв два рядки"))
# текст після цитати також завжди починається з нового рядка
text.append('Кінець повідомлення')
```

Використання декількох цитат підряд в середині повідомлення

```python
from telegram_markdown_text import *

text = MarkdownText()
text.append('Початок повідомлення')
text.append(QuoteBlock("Перша цитата"))
text.append(QuoteBlock("Друга цитата\nв два рядки"))
text.append(QuoteBlock("Третя цитата"))
text.append('Кінець повідомлення')
```

### Екранування Markdown симовлів

Для того, щоб отримати екранований текст, достатньо просто викликати метод `escaped_text()`

```python
from telegram_markdown_text import *

text = PlainText('Простий текст з різними символами !"№;%:?*()')
text.escaped_text()  # екранований текст, який можна відправляти меседжем через API Телеграма
```

Або ж просто привести MarkdownText до str, як це робиться при виклику методу `print()`

```python
from telegram_markdown_text import *

text = PlainText('Простий текст з різними символами !"№;%:?*()')
print(text)  # виведеться уже екранований текст, оскільки в MarkdownText оверрайднутий метод __str__
```

## License

telegram-markdown-text
Copyright (c) 2024 Denys Yablonskyi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


