import re
import random
from abc import ABC, abstractmethod
from typing import List, Union


# TODO: lazy encoding (generator)
class BaseEncoder(ABC):
    def __init__(self, text: str) -> None:
        pass

    @abstractmethod
    def encode(self) -> Union[str, List[str]]:
        pass


TO_SHUFFLE_REGEX = re.compile(r'(?P<left>[^a-zA-Z]|\w)(?P<middle>[a-zA-Z]{2,})(?P<right>[^a-zA-Z]|\w)', re.U)


class Encoder:
    def __init__(self, text: str) -> None:
        self._text = text

    def encode(self) -> Union[str, List[str]]:
        encoded: List[str] = ['\n-weird-\n']
        shuffled_words: List[str] = []
        for word in self._text.split(' '):
            if self._word_to_encode(word):
                encoded.append(self._shuffle(word))
                shuffled_words.append(word)
            else:
                encoded.append(word)
        encoded.append('\n-weird-\n')
        encoded_text = ' '.join(word for word in encoded)
        return encoded_text, shuffled_words

    def _word_to_encode(self, word: str) -> bool:
        # TODO: regex
        mid_letters = set()
        for char in word[1:-1]:
            if char.isalpha():
                mid_letters.add(char)
            if len(mid_letters) > 1:
                return True
        return False

    def _shuffle(self, word: str) -> str:
        if match := TO_SHUFFLE_REGEX.match(word):
            match_groups = match.groupdict()
            to_shuffle = match_groups['middle']
        else:
            return word
        shuffled = to_shuffle
        while shuffled == to_shuffle:
            shuffled_chars = random.sample(to_shuffle, len(to_shuffle))
            shuffled = ''.join(shuffled_chars)
        return match_groups['left'] + shuffled + match_groups['right']


if __name__ == '__main__':
    text = 'Alice in the wonderland. This is my favourite movie.'
    weird_encoder = Encoder(text)
    print(weird_encoder.encode())
