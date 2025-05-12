from srcs.Parsing import Parser
from srcs.Qlearning import QLearning


if __name__=="__main__":
    try:
        parser = Parser()
        qlearning = QLearning(parser.krpsim.stocks, parser.krpsim.processes, parser.krpsim.optimized_stocks, parser.krpsim.delay)
        qlearning.train(parser.krpsim.epochs)
        qlearning.run()
    except Exception as e:
        print(f'{str(e)}')
        exit(1)