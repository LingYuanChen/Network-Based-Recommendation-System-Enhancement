#!/bin/bash

# Color definitions for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default configuration
CATEGORY="musical_instruments"

# Function to display script usage
usage() {
    echo "Amazon Product Recommendation System Cleanup"
    echo "-----------------------------------------"
    echo "This script cleans up temporary files and results"
    echo "from the recommendation system pipeline."
    echo
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -c, --category CATEGORY    Product category to clean (default: musical_instruments)"
    echo "  -a, --all                  Clean all categories"
    echo "  -k, --keep-results         Keep final results and visualizations"
    echo "  -h, --help                 Display this help message"
    echo
    echo "Example:"
    echo "  $0 -c electronics          # Clean electronics category"
    echo "  $0 --all                   # Clean all categories"
    exit 1
}

# Initialize flags
CLEAN_ALL=false
KEEP_RESULTS=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--category)
            CATEGORY="$2"
            shift 2
            ;;
        -a|--all)
            CLEAN_ALL=true
            shift
            ;;
        -k|--keep-results)
            KEEP_RESULTS=true
            shift
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

# Function to clean a specific category
clean_category() {
    local category=$1
    echo -e "${YELLOW}Cleaning up ${category}...${NC}"
    
    # Remove temporary files
    rm -f "../amazon_${category}_review/"*.txt
    rm -f "../amazon_${category}_review/"*.json
    
    # Remove graph files
    rm -f "../amazon_${category}_review/G*_edgelist_*.txt"
    
    # Optionally remove results
    if [ "$KEEP_RESULTS" = false ]; then
        rm -f "../amazon_${category}_review/finalResults.txt"
        rm -rf "../amazon_${category}_review/pic"
    fi
    
    echo -e "${GREEN}✓ Cleaned up ${category}${NC}"
}

# Main cleanup logic
if [ "$CLEAN_ALL" = true ]; then
    echo -e "${YELLOW}Cleaning all categories...${NC}"
    for dir in ../amazon_*_review/; do
        if [ -d "$dir" ]; then
            category=$(basename "$dir" | sed 's/amazon_\(.*\)_review\//\1/')
            clean_category "$category"
        fi
    done
else
    clean_category "$CATEGORY"
fi

echo -e "${GREEN}Cleanup completed successfully!${NC}"
if [ "$KEEP_RESULTS" = true ]; then
    echo "Final results and visualizations have been preserved."
fi 