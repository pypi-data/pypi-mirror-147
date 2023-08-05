import smtplib
from email.utils import formataddr
from email.message import EmailMessage
from string import Template
from os.path import exists
from pathlib import Path
from re import findall
from validators import url
from mimetypes import guess_type
from string import digits
from textwrap import dedent
from schedule import every, run_pending
from dataclasses import dataclass, field
from typing import Tuple, Union
from .errors import InvalidPathError


def split_num_text(s):
    head = s.lstrip(digits)
    return head, int(s[:len(head)])


def parse_freq(unit, n):
    time_table = {'s': every(n).seconds,
                  'm': every(n).minutes,
                  'h': every(n).hours,
                  'd': every(n).days}
    return time_table[unit]


def parse_attr(size_attrs):
    for attr in size_attrs:
        property = 'width' if attr[0] == 'w' else 'height'
        yield f'{property}="{int(attr[1:])}"'


def make_tuple(content):
    return content if isinstance(content, tuple) else tuple(content) \
        if isinstance(content, list) else (content,)


@dataclass(frozen=True)
class Info:
    recipients: Union[str, Tuple[str]]
    name: str
    subject: str
    body: str
    images: Union[str, Tuple[str]] = field(default_factory=tuple)
    attachments: Union[str, Tuple[str]] = field(default_factory=tuple)
    font_name: str = 'Verdana'
    font_size: int = 12

    def __post_init__(self):
        object.__setattr__(self, 'recipients', make_tuple(self.recipients))
        object.__setattr__(self, 'images', make_tuple(self.images))
        object.__setattr__(self, 'attachments', make_tuple(self.attachments))


def _get_attachments(attas):
    for path in attas:
        p = Path(path)
        mtype = guess_type(path)[0]
        stype = mtype.split('/')[1]
        content = p.read() if mtype == 'text' else p.read_bytes()
        yield content, mtype, stype, path


class Sender:
    def __init__(self, sender: str, app_pwd: str, close_after: int = None):
        self.sender = sender
        self.app_pwd = app_pwd
        self._img_files = {}
        self.counter = 0
        self.limit = close_after
        self.conn = smtplib.SMTP("smtp.gmail.com", 587)
        self.conn.ehlo()
        self.conn.starttls()
        self.conn.login(sender, app_pwd)
        self._cache = {}

    def send(self, info, every=None):
        if msg := self._cache.get(info):
            self.counter += 1
            return self._send_mail(msg, every)

        body = info.body

        for string, link in findall(r'\[(.+?)\]\((.+?)\)', body):
            text = f'[{string}]({link})'
            path = f'<a href="{link}" target="_blank">{string}</a>'
            body = body.replace(text, path)

        msg = EmailMessage()
        msg['Subject'] = info.subject
        msg['From'] = formataddr((info.name, self.sender))
        msg['To'] = info.recipients if isinstance(info.recipients, str) \
            else ','.join(info.recipients)
        msg.set_content(info.body)

        imgs = info.images
        img_nums = [int(i) for i in findall(r'\$img(\d)', body)]
        assert len(img_nums) == len(imgs) or len(set(img_nums)) == len(imgs)

        template = Template(dedent(f'''
                        <html><body><pre style="font-size: {info.font_size}px">
                        <font face="{info.font_name}, sans-serif, Times New Roman,
                                    Georgia, monospace">{body}
                        </font></pre></body></html>'''))

        msg.add_alternative(self._get_template(template, imgs, img_nums), subtype='html')

        for img_cid, (path, img_ext, img_con) in self._img_files.items():
            msg.get_body().add_related(img_con, 'image', img_ext, cid=img_cid, filename=path)

        attas = info.attachments

        for content, mtype, stype, path in _get_attachments(attas):
            msg.add_attachment(content, mtype, stype, filename=path)

        self._cache[info] = msg
        self.counter += 1
        self._send_mail(msg, every)

    def _get_template(self, template, imgs, img_nums):
        img_maps = {}
        for img_n in img_nums:
            img = imgs[img_n - 1]

            if isinstance(img, str):
                path, dims = img, ''
            else:
                path, dims = img[0], ' '.join(parse_attr(img[1:]))

            if exists(path):
                p = Path(path)
                img_cid, img_ext, img_con = f'<img{img_n}>', p.suffix[1:], p.read_bytes()
                self._img_files[img_cid] = (path, img_ext, img_con)
                img_maps[f'img{img_n}'] = f'<img src="cid:img{img_n}" {dims}/>'
            elif url(path):
                img_maps[f'img{img_n}'] = f'<img src="{path}" {dims}/>'
            else:
                raise InvalidPathError(path)

        return template.substitute(img_maps)

    def _send_mail(self, msg, every):
        if not every:
            self.conn.send_message(msg)
        else:
            unit, n = split_num_text(every)
            parse_freq(unit, n).do(self.conn.send_message, msg)
            while 1:
                run_pending()

        if self.counter == self.limit:
            self.close()

    def close(self):
        self.conn.quit()
