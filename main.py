from srcs.Parsing import Parser
from srcs.DQN import KrpsimDQN


if __name__=="__main__":
    parser = Parser()
    qlearning = KrpsimDQN(parser.krpsim.stocks, parser.krpsim.processes, parser.krpsim.optimized_stocks, parser.krpsim.delay)
    qlearning.train(parser.krpsim.epochs)