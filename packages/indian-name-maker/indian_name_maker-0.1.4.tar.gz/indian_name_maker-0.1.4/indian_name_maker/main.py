"""Command-line interface for indian-name-maker package."""

import argparse
import sys
from indian_name_maker import __version__
from indian_name_maker.generator import (
    get_multiple_first_names,
    get_multiple_full_names,
    get_multiple_last_names
)

# Maximum number of names to generate at once
MAX_NAMES = 1000000

def main():
    """Execute the command-line interface."""
    parser = argparse.ArgumentParser(description="Generate Indian names")
    parser.add_argument("--version", action="version", 
                      version=f"indian-name-maker {__version__}")
    parser.add_argument("--count", type=int, default=1,
                      help=f"Number of names to generate (default: 1, max: {MAX_NAMES})")
    name_type = parser.add_mutually_exclusive_group()
    name_type.add_argument("--first-only", action="store_true",
                        help="Generate only first names")
    name_type.add_argument("--last-only", action="store_true",
                        help="Generate only last names")
    parser.add_argument("--separator", type=str, default=" ",
                      help="Separator between first and last name (default: space)")
    parser.add_argument("--batch-size", type=int, default=MAX_NAMES,
                      help="Number of names to generate per batch for large requests")
    
    args = parser.parse_args()
    
    try:
        if args.count < 1:
            raise ValueError("Count must be greater than 0")
        if args.count > MAX_NAMES:
            raise ValueError(f"Count must not exceed {MAX_NAMES}")
        if args.batch_size < 1:
            raise ValueError("Batch size must be greater than 0")
            
        # For very large requests, process in batches
        remaining = args.count
        batch_size = min(args.batch_size, MAX_NAMES)
        
        while remaining > 0:
            current_batch = min(remaining, batch_size)
            
            if args.first_only:
                names = get_multiple_first_names(current_batch)
            elif args.last_only:
                names = get_multiple_last_names(current_batch)
            else:
                names = get_multiple_full_names(current_batch, args.separator)
            
            # Print names as a single string for better output formatting
            print("\n".join(names))
            sys.stdout.flush()  # Ensure immediate output
            
            remaining -= current_batch
            
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
