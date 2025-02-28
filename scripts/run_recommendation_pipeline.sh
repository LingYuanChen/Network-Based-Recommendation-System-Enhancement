#!/bin/bash

# Color definitions for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default configuration
CATEGORY="musical_instruments"
RATING_THRESHOLD=4
REC_NUM=10
YEAR=2014
MONTHS="101112"

# Function to display script usage
usage() {
    echo "Amazon Product Recommendation Pipeline"
    echo "-------------------------------------"
    echo "This script runs the complete recommendation system pipeline,"
    echo "from data processing to evaluation."
    echo
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -c, --category CATEGORY    Product category (default: musical_instruments)"
    echo "  -r, --rating RATING        Minimum rating threshold (default: 4)"
    echo "  -n, --recommendations NUM  Number of recommendations per user (default: 10)"
    echo "  -y, --year YEAR           Year for analysis (default: 2014)"
    echo "  -m, --months MONTHS        Months for analysis (default: 101112)"
    echo "  -h, --help                Display this help message"
    echo
    echo "Example:"
    echo "  $0 -c electronics -r 4 -n 20"
    echo "  $0 --category musical_instruments --rating 3 --recommendations 15"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--category)
            CATEGORY="$2"
            shift 2
            ;;
        -r|--rating)
            RATING_THRESHOLD="$2"
            shift 2
            ;;
        -n|--recommendations)
            REC_NUM="$2"
            shift 2
            ;;
        -y|--year)
            YEAR="$2"
            shift 2
            ;;
        -m|--months)
            MONTHS="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown parameter: $1"
            usage
            ;;
    esac
done

# Function to check if a command was successful
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 completed successfully${NC}"
    else
        echo -e "${RED}✗ Error in $1${NC}"
        exit 1
    fi
}

# Function to run a Python script with timing
run_python_script() {
    echo -e "${YELLOW}Running $1...${NC}"
    start_time=$(date +%s)
    python3 "../src/$1" "$CATEGORY" "$2" "$3" "$4" 2>&1
    check_status "$1"
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo -e "${GREEN}✓ $1 completed in ${duration}s${NC}"
    echo "----------------------------------------"
}

# Create necessary directories
echo -e "${YELLOW}Setting up directories...${NC}"
mkdir -p "../amazon_${CATEGORY}_review/data"
mkdir -p "../amazon_${CATEGORY}_review/pic"
check_status "Directory setup"

# Main pipeline
echo -e "${YELLOW}Starting recommendation system pipeline...${NC}"
echo "Category: $CATEGORY"
echo "Rating Threshold: $RATING_THRESHOLD"
echo "Recommendations per user: $REC_NUM"
echo "----------------------------------------"

# Run the pipeline
run_python_script "parseGraph.py" "$RATING_THRESHOLD"
run_python_script "rollingWindow.py" "$RATING_THRESHOLD"
run_python_script "centrality.py" "$CATEGORY"
run_python_script "communityDetection.py" "$CATEGORY"
run_python_script "recommend.py" "$CATEGORY" "$REC_NUM"
run_python_script "recommendAnalyze.py" "$CATEGORY" "$YEAR" "$MONTHS" "$RATING_THRESHOLD" "$REC_NUM"

echo -e "${GREEN}Pipeline completed successfully!${NC}"
echo "Results can be found in amazon_${CATEGORY}_review/pic/"
echo "Check finalResults.txt for detailed analysis" 