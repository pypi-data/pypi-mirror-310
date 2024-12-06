import argparse
from name_generator import NameGenerator

def main():
    """Main CLI function for generating Indian names."""
    parser = argparse.ArgumentParser(description="Generate Indian names")
    parser.add_argument("--count", type=int, default=1,
                      help="Number of names to generate (default: 1)")
    parser.add_argument("--first-only", action="store_true",
                      help="Generate only first names")
    parser.add_argument("--separator", type=str, default=" ",
                      help="Separator between first and last name (default: space)")
    
    args = parser.parse_args()
    
    generator = NameGenerator()
    
    if args.first_only:
        names = generator.get_multiple_names(args.count, full_name=False)
    else:
        names = [generator.get_full_name(separator=args.separator) for _ in range(args.count)]
    
    for name in names:
        print(name)

if __name__ == "__main__":
    main()
