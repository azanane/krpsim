#include "main.hpp"

int main(int argc, char **argv) {
    if (argc != 3) {
        std::cerr << "use: ./krpsim path/to/process/file delay" << std::endl;
        exit(1);
    }

    Parser parser = Parser(std::string(argv[1]), std::string(argv[2]));

    Krpsim krp = parser.getKrspim();

    // DynamicProgramming dyn(krp);

    return 0;
}