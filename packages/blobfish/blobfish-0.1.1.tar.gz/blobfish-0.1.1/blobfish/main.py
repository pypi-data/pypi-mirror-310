from typing import Self

BLOBFISH = '                                         .-@@@@@@@@@@@@@-.                      . -.:.--:.:--:-     \n                                    .@@@@#.             .-@@@@=                                     \n                                .@@@#                         :@@@*                                 \n                             .@@@.                                .@@@                              \n                           #@@.                                      .@@*                           \n                         =@@                                            @@:                         \n                        @@%                                              :@@                        \n                       @@.      +@.                              .@+       @@                       \n                     .@@.       -@.                              .@=        @@.                     \n                    *@@                                                      #@-                    \n                  :@@=                                                        .@@.                  \n                :@@.               :                            *               .@@.                \n              #@@.                 .@@.                      =@@.                  @@+              \n            -@@                      -@%                    @@.                      @@.            \n      @@@@@@@+                 :@@@@@@@@@                  @@@@@@@@@.                 .@@@@@@@      \n     @@   :@*             .#@@@:   :=@@@@@.              =@@@@+:.   #@@@+              +@-   @@     \n     @@*  @@            @@@:  @@@@:    .+@@@@          @@@-      %@@@#  *@@=            @@  *@@     \n       =@@@@          @@% .@@+  =@@@@=..    .+@@@@@@@@=.    .:+@@@@: .@@@. @@#          #@@@=       \n         :@@        +@@ *@@  :@@-                                  #@@. .@@: @@.        @@.         \n          @@+       @@     @@%                                       .@@@  .  @@       =@%          \n           :@@.      %@@@@@:                                            +@@@@@=      .@@.           \n             :@@@.                                                                .@@@              \n                 .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.\n'


class Const:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return BLOBFISH


END: Const = Const("END")


class Print:
    def __init__(self, string: str | None = None):
        self.str = string

    def __lshift__(self, other: str) -> Self:
        if not isinstance(other, str):
            raise Exception(BLOBFISH)
        return Print(other)

    def __rshift__(self, other: Const):
        if not isinstance(other, Const) or not self.str:
            raise Exception(BLOBFISH)
        __builtins__["print"](self.str)


print = Print()