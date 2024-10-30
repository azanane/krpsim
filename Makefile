################################################################################
##                               Code color                                   ##
################################################################################

COLOR_NORM		=	\033[0m
COLOR_RED			=	\033[31m
COLOR_BLUE	=	\033[36m

################################################################################
##                               SRCS                                         ##
################################################################################
CACHE = .cache
SRCS_DIR = srcs
SRCS = 	main.cpp 	\
		Krpsim.cpp	\
		Process.cpp
		
NAME = krpsim


OBJS_DIR = build
OBJS = $(addprefix $(OBJS_DIR)/,$(subst $(SRCS_DIR),,$(SRCS:.cpp=.o)))

CC = c++
CFLAGS = -Wall -Wextra -Werror -MMD -MP -Iincludes -g3 # -O3 -fsanitize=address
RM = rm -rf

# Set the number of object files 
NUM_OBJS = $(words $(OBJS))

################################################################################
##                       Compilation Environnement                            ##
################################################################################

# Define a function to print the progress bar 
define print_progress
	$(eval i = $(shell expr $(i) + 1))
	$(eval PERCENT = $(shell expr $(i) '*' 100 '/' $(NUM_OBJS)))
	@if [ $(i) -eq 1 ]; then \
        printf "$(COLOR_BLUE)Starting compilation...\n$(COLOR_NORM)"; \
  fi
	@printf "\r\033[K\t$(COLOR_BLUE)[$(PERCENT)%%]\t--> $(COLOR_NORM)$<\$(COLOR_NORM)"
	@printf "\r\033[K\t$(COLOR_BLUE)[$(PERCENT)%%]\t--> $(COLOR_NORM)$<\$(COLOR_NORM)"
endef

# Compilation rule for object files
$(OBJS_DIR)/%.o : $(SRCS_DIR)/%.cpp
	@mkdir -p $(dir $@)
	$(call print_progress)
	@$(CC) $(CFLAGS) -c $< -o $@

# Include the dependency files
-include $(OBJ:.o=.d)

# Default target
all: $(NAME)

# Link the final executable
$(NAME): $(OBJS)
	@printf "\n[✅]\tCompilation of $(COLOR_PURPLE)$(NAME)\$(COLOR_NORM)\n"
	@$(CC) $(CFLAGS) -o $(NAME) $(OBJS)

# Clean up object files and dependency files
clean:
	@$(RM) $(OBJS_DIR)
	@$(RM) $(DEPS_DIR)
	@$(RM) $(CACHE)

# Clean up object files, dependency files, and the executable
fclean: clean
	@$(RM) $(NAME)

# Rebuild everything
re: fclean all

.PHONY: all clean fclean re
