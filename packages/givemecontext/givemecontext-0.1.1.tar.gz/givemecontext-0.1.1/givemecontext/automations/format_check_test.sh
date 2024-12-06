#!/bin/bash

# Verify required environment variables
if [ -z "$GIVEMECONTEXT_LOG_FILE" ]; then
    echo "Error: GIVEMECONTEXT_LOG_FILE environment variable is not set"
    exit 1
fi

if [ -z "$GIVEMECONTEXT_LOG_DIR" ]; then
    echo "Error: GIVEMECONTEXT_LOG_DIR environment variable is not set"
    exit 1
fi

if [ -z "$GIVEMECONTEXT_LOG_DIR_NAME" ]; then
    echo "Error: GIVEMECONTEXT_LOG_DIR_NAME environment variable is not set"
    exit 1
fi

# Ensure log directory exists
mkdir -p "$GIVEMECONTEXT_LOG_DIR"

# Clear the log file
> "$GIVEMECONTEXT_LOG_FILE"

# Execute commands and log output
script -q -c '{
    echo
    echo "PYTHONPATH: $PYTHONPATH"
    echo "Log Directory: $GIVEMECONTEXT_LOG_DIR_NAME"
    
    echo
    
    echo "<command>black .</command>" | tee -a "$GIVEMECONTEXT_LOG_FILE";
    echo "<output>" | tee -a "$GIVEMECONTEXT_LOG_FILE";
    black . 2>&1 | tee -a "$GIVEMECONTEXT_LOG_FILE";
    echo "</output>" | tee -a "$GIVEMECONTEXT_LOG_FILE";
    
    echo
    
    echo "<command>ruff check . --fix --exclude venv,site-packages,.venv,.local,.pythonlibs,bin,.*</command>" | tee -a "$GIVEMECONTEXT_LOG_FILE";
    echo "<output>" | tee -a "$GIVEMECONTEXT_LOG_FILE";
    ruff check . --fix --exclude venv,site-packages,.venv,.local,.pythonlibs,bin,.* 2>&1 | tee -a "$GIVEMECONTEXT_LOG_FILE";
    echo "</output>" | tee -a "$GIVEMECONTEXT_LOG_FILE";

    echo

    echo "<command>pytest</command>" | tee -a "$GIVEMECONTEXT_LOG_FILE";
    echo "<output>" | tee -a "$GIVEMECONTEXT_LOG_FILE";
    pytest 2>&1 | tee -a "$GIVEMECONTEXT_LOG_FILE";
    echo "</output>" | tee -a "$GIVEMECONTEXT_LOG_FILE";
}' "$GIVEMECONTEXT_LOG_FILE"