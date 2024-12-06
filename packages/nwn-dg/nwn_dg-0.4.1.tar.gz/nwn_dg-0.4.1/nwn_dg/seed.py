import ast
import os
import random

from . import constants as C


class Seed:
    def __init__(self, args):
        self._seed = args.get("seed")
        self._output_seed = args.get("output_seed", C.DEFAULT_OUTPUT_SEED)
        self._output_seed_early = args.get("output_seed_early", C.DEFAULT_OUTPUT_SEED)
        self._filepath = args["filepath"]

        if self._seed and os.path.isfile(self._seed):
            filename = self._seed
            with open(filename, encoding="UTF-8") as fd:
                state = fd.read()
            state = ast.literal_eval(state)
            random.setstate(state)
        else:
            random.seed(self._seed)
        self._saved_state = random.getstate()

        # Debug feature: save the seed before generation, in case of crash
        if self._output_seed_early:
            self.save()

    def save(self):
        if True not in [self._output_seed, self._output_seed_early]:
            return
        filename = self._filepath + ".seed"
        with open(filename, mode="w", encoding="UTF-8") as fd:
            fd.write(str(self._saved_state))
