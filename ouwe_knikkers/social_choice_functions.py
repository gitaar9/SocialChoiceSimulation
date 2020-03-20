import random


class SocialChoiceFunction:

    def __init__(self, verbose=False):
        self.verbose = verbose

    @staticmethod
    def print_profile(profile, choice=None):
        for ballot in profile:
            print(" ".join(ballot))
        if choice:
            print('-' * 10, '\n', choice.upper())

    def __call__(self, profile):
        if len(profile) == 0:
            raise KeyError('A profile should consists of at least one ballot')
        choice = self._apply_function(profile)
        if self.verbose:
            self.print_profile(profile, choice)
        return choice

    def _apply_function(self, profile):
        raise NotImplementedError('This function should be implemented by subclasses.')

    @staticmethod
    def _apply_optional_random_tiebreaker(choices):
        if len(choices) == 1:
            return choices[0]

        # In this case we have more options in the set of social choices
        return choices[int(random.random() / (1 / len(choices)))]


class Plurality(SocialChoiceFunction):
    def _apply_function(self, profile):
        # Count votes for every ballot
        alternatives_hist = {alternative: 0 for alternative in profile[0]}
        for agent in profile:
            alternatives_hist[agent[0]] += 1

        # Decide the set of choices from plurality
        choices = []
        max_count = -1
        for ballot, count in alternatives_hist.items():
            if count > max_count:
                choices = [ballot]
                max_count = count
            elif count != 0 and count == max_count:
                choices.append(ballot)

        return self._apply_optional_random_tiebreaker(choices)


class RandomDictatorship(SocialChoiceFunction):
    def _apply_function(self, profile):
        return profile[random.randint(0, len(profile) - 1)][0]
