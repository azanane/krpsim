from srcs.Parsing import Parser
from srcs.Qlearning import QLearning


if __name__=="__main__":
    parser = Parser()
    qlearning = QLearning(parser.krpsim.stocks, parser.krpsim.processes, parser.krpsim.optimized_stocks, parser.krpsim.delay)
    qlearning.train(50000)
    qlearning.run()