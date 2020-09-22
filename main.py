from startup import init_dependencies
from game import GameController

if __name__ == '__main__':
    init_dependencies()
    gc = GameController()
    gc.run()
