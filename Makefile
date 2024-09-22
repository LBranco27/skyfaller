# Define the virtual environment directory
VENV_DIR = venv

# Python version (you can specify the version you need)
PYTHON = python3

# Default target to create and install everything
install: venv install-deps

# Create virtual environment
venv:
	@echo "Creating virtual environment"
	$(PYTHON) -m venv $(VENV_DIR)

# Install dependencies inside virtual environment
install-deps:
	@echo "Installing dependencies..."
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt

# Clean up the virtual environment and other temporary files
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
