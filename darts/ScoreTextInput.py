from typing import List, Union, Tuple

from darts.commands import AddScore, ScoreValue


class ScoreTextInput:
    """This will handle the logic behind the text entry for scores."""

    def __init__(self):
        self.scores: List[Union[str, Tuple[str, str]]] = ['']

    def __str__(self):
        return ' + '.join(f"{score[0]} * {score[1]}" if isinstance(score, tuple) else score for score in self.scores)

    def reset(self):
        """Reset the ScoreTextInput in it's initial state."""
        self.scores = ['']

    def as_command(self) -> AddScore:
        """Convert the ScoreTextInput as an AddScore command."""
        scores = []
        for score in self.scores:
            if isinstance(score, tuple):
                factor, value = score
            else:
                value = score
                factor = '1'

            factor, value = int(factor), int(value)
            scores.append(ScoreValue(value=value, factor=factor))

        return AddScore(scores=scores, player=None)

    def del_last(self):
        """Delete the last character input."""
        if self.scores:
            score = self.scores.pop(-1)
            if score != '':
                if isinstance(score, tuple):
                    factor, value = score
                    if value == '':
                        score = factor
                    else:
                        score = (factor, value[:-1])
                elif isinstance(score, str):
                    score = score[:-1]

                self.scores.append(score)

    def mul_score(self):
        """Turn a simple (value) score as a (factor, value) score."""
        if self.scores and isinstance(self.scores[-1], str):
            score = self.scores.pop(-1)
            score = (score, '')
            self.scores.append(score)

    def add_score(self):
        """Add a new score to the list."""
        self.scores.append('')

    def add_digit(self, digit: str):
        """Add a digit to the latest score."""
        if len(digit) == 1 and digit.isnumeric():
            score = self.scores.pop(-1)
            if isinstance(score, tuple):
                factor, value = score
            elif isinstance(score, str):
                factor = score
                value = None
            else:
                raise NotImplementedError

            if value is None:
                factor = factor + digit
                score = factor
            else:
                value = value + digit
                score = (factor, value)

            self.scores.append(score)
