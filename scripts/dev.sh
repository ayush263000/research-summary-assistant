#!/bin/bash

# Development utility script for Document-Aware GenAI Assistant

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_green() {
    echo -e "${GREEN}$1${NC}"
}

print_yellow() {
    echo -e "${YELLOW}$1${NC}"
}

print_red() {
    echo -e "${RED}$1${NC}"
}

# Help function
show_help() {
    cat << EOF
Document-Aware GenAI Assistant - Development Tools

Usage: $0 [COMMAND]

Commands:
    setup       Setup the development environment
    test        Run all tests
    lint        Run code linting (black, flake8, mypy)
    clean       Clean up generated files and cache
    run         Run the application
    api         Run API server only
    deps        Install/update dependencies
    demo        Create demo data for testing
    backup      Backup current data directory
    help        Show this help message

Examples:
    $0 setup       # Initial setup
    $0 test        # Run tests
    $0 lint        # Check code quality
    $0 run         # Start the application

EOF
}

# Setup development environment
setup_dev() {
    print_yellow "Setting up development environment..."
    
    # Install dependencies
    print_green "Installing dependencies..."
    pip install -r requirements.txt
    
    # Setup environment
    if [ ! -f .env ]; then
        cp .env.example .env
        print_yellow "Created .env file. Please edit with your API keys."
    fi
    
    # Create directories
    mkdir -p data/uploads logs
    
    print_green "Development environment setup complete!"
}

# Run tests
run_tests() {
    print_yellow "Running tests..."
    python -m pytest tests/ -v --tb=short
    print_green "Tests completed!"
}

# Run linting
run_lint() {
    print_yellow "Running code quality checks..."
    
    print_green "Running black (code formatting)..."
    python -m black app/ tests/ --check --diff
    
    print_green "Running flake8 (style guide)..."
    python -m flake8 app/ tests/
    
    print_green "Running mypy (type checking)..."
    python -m mypy app/ --ignore-missing-imports
    
    print_green "Code quality checks completed!"
}

# Clean up
clean_up() {
    print_yellow "Cleaning up..."
    
    # Remove Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Remove test artifacts
    rm -rf .pytest_cache test.db test_uploads
    
    # Remove logs
    rm -rf logs/*.log
    
    print_green "Cleanup completed!"
}

# Run application
run_app() {
    print_yellow "Starting Document-Aware GenAI Assistant..."
    python run.py
}

# Run API only
run_api() {
    print_yellow "Starting API server only..."
    python run.py --api-only
}

# Install/update dependencies
update_deps() {
    print_yellow "Updating dependencies..."
    pip install -r requirements.txt --upgrade
    print_green "Dependencies updated!"
}

# Create demo data
create_demo() {
    print_yellow "Creating demo data..."
    
    # Create sample documents
    mkdir -p data/demo
    
    cat > data/demo/sample_research.txt << EOF
# Artificial Intelligence in Healthcare: A Comprehensive Review

## Abstract
This research paper examines the current applications and future potential of artificial intelligence (AI) in healthcare. The study analyzes various AI technologies including machine learning, natural language processing, and computer vision in medical contexts.

## Introduction
Artificial intelligence has emerged as a transformative force in healthcare, offering unprecedented opportunities to improve patient outcomes, reduce costs, and enhance clinical efficiency. This paper provides a comprehensive review of current AI applications in healthcare and explores future directions.

## Key Findings
1. AI-powered diagnostic systems show 95% accuracy in medical imaging
2. Natural language processing reduces clinical documentation time by 60%
3. Predictive analytics improves patient risk assessment by 40%

## Machine Learning Applications
Machine learning algorithms have shown remarkable success in:
- Medical image analysis and radiology
- Drug discovery and development
- Personalized treatment recommendations
- Clinical decision support systems

## Challenges and Limitations
Despite promising results, several challenges remain:
- Data privacy and security concerns
- Regulatory compliance requirements
- Integration with existing healthcare systems
- Need for clinical validation

## Conclusion
AI represents a paradigm shift in healthcare delivery. While challenges exist, the potential benefits far outweigh the risks. Continued investment in AI research and development is essential for realizing the full potential of these technologies.

## References
1. Smith, J. et al. (2024). "AI in Medical Imaging: Current State and Future Directions"
2. Johnson, A. (2024). "Natural Language Processing in Clinical Settings"
3. Brown, M. (2023). "Predictive Analytics for Patient Care"
EOF

    print_green "Demo data created in data/demo/"
}

# Backup data
backup_data() {
    print_yellow "Backing up data directory..."
    
    backup_name="backup_$(date +%Y%m%d_%H%M%S)"
    tar -czf "${backup_name}.tar.gz" data/
    
    print_green "Backup created: ${backup_name}.tar.gz"
}

# Main script logic
case "${1:-help}" in
    setup)
        setup_dev
        ;;
    test)
        run_tests
        ;;
    lint)
        run_lint
        ;;
    clean)
        clean_up
        ;;
    run)
        run_app
        ;;
    api)
        run_api
        ;;
    deps)
        update_deps
        ;;
    demo)
        create_demo
        ;;
    backup)
        backup_data
        ;;
    help|*)
        show_help
        ;;
esac
