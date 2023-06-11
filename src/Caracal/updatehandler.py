import pygame


class UpdateHandler:
    """Needs work for other events such as mouse events, KEYUP etc."""

    def __init__(self, state, app) -> None:
        self.app = app
        self.update_tasks = []
        self.input_tasks = {
            pygame.QUIT: {"func": self.app.stop}
        }
        self.state = state

    def update(self):
        for task in self.update_tasks:
            state_to_draw = task["state"]
            _task = task["task"]
            if self.state == state_to_draw:
                _task()
        self._check_input()

    def _check_input(self):
        # input task structure
        # task = {KEYDOWN : [{KEY_A : func}] }

        for event in pygame.event.get():
            if event.type in self.input_tasks:
                _dict = self.input_tasks[event.type]
                if event.type == pygame.QUIT:
                    self.input_tasks[pygame.QUIT]["func"]()
                elif event.type == pygame.KEYDOWN:
                    _task = _dict[event.key]
                    _task()
                else:
                    raise NotImplementedError(
                        "Only KEYDOWN has been implemented at the moment."
                    )
