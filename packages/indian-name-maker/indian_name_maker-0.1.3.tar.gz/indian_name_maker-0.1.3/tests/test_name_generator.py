"""Test suite for indian-name-maker package."""

import pytest
import time
import csv
import os
from indian_name_maker import NameGenerator

@pytest.fixture
def generator():
    return NameGenerator()

def test_get_first_name(generator):
    name = generator.get_first_name()
    assert isinstance(name, str)
    assert len(name) > 0

def test_get_last_name(generator):
    name = generator.get_last_name()
    assert isinstance(name, str)
    assert len(name) > 0

def test_get_full_name(generator):
    name = generator.get_full_name()
    assert isinstance(name, str)
    assert " " in name
    first_name, last_name = name.split(" ")
    assert len(first_name) > 0
    assert len(last_name) > 0

def test_get_full_name_custom_separator(generator):
    name = generator.get_full_name(separator="-")
    assert "-" in name

def test_get_multiple_names(generator):
    names = generator.get_full_names(count=5)
    assert len(names) == 5
    assert all(isinstance(name, str) for name in names)
    assert all(" " in name for name in names)

def test_get_multiple_first_names(generator):
    names = generator.get_first_names(count=5)
    assert len(names) == 5
    assert all(isinstance(name, str) for name in names)

def test_invalid_count(generator):
    with pytest.raises(ValueError):
        generator.get_full_names(count=0)

def generate_and_save_names(generator, count, output_file):
    """Generate names and save them to a CSV file with performance metrics."""
    print(f"\nGenerating {count:,} names...")
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Generate full names with timing
    start_time = time.time()
    names = generator.get_full_names(count)
    elapsed = time.time() - start_time
    
    # Calculate metrics
    names_per_second = count / elapsed
    
    # Save to CSV
    with open(f'output/{output_file}', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['First Name', 'Last Name', 'Full Name'])
        
        for name in names:
            first_name, last_name = name.split(' ')
            writer.writerow([first_name, last_name, name])
    
    # Print performance metrics
    print(f"Performance metrics for {count:,} names:")
    print(f"- Time taken: {elapsed:.2f} seconds")
    print(f"- Names per second: {names_per_second:,.0f}")
    print(f"- Output saved to: output/{output_file}")
    
    return elapsed, names_per_second

def test_generate_different_sizes(generator):
    """Test generating different sizes of name datasets."""
    print("\nGenerating different sized datasets...")
    
    # Test cases with different sizes
    test_cases = [
        (5000, "names_5k.csv"),
        (50000, "names_50k.csv"),
        (500000, "names_500k.csv"),
        (5000000, "names_5m.csv")
    ]
    
    # Save performance metrics
    metrics = []
    
    for count, filename in test_cases:
        elapsed, names_per_second = generate_and_save_names(generator, count, filename)
        metrics.append({
            'count': count,
            'elapsed_seconds': elapsed,
            'names_per_second': names_per_second
        })
    
    # Save performance metrics to CSV
    with open('output/performance_metrics.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['count', 'elapsed_seconds', 'names_per_second'])
        writer.writeheader()
        writer.writerows(metrics)
    
    print("\nAll datasets generated successfully!")
    print("Performance metrics saved to: output/performance_metrics.csv")

def test_large_scale_performance(generator):
    """Test performance with large-scale name generation."""
    print("\nPerformance Test Results:")
    
    batch_sizes = [1000, 10000, 100000, 1000000]
    for batch_size in batch_sizes:
        # Test first names
        start_time = time.time()
        names = generator.get_first_names(batch_size)
        elapsed = time.time() - start_time
        print(f"\nGenerated {batch_size:,} first names:")
        print(f"- Time taken: {elapsed:.2f} seconds")
        print(f"- Names per second: {batch_size/elapsed:,.0f}")
        assert len(names) == batch_size
        
        # Test full names
        start_time = time.time()
        names = generator.get_full_names(batch_size)
        elapsed = time.time() - start_time
        print(f"\nGenerated {batch_size:,} full names:")
        print(f"- Time taken: {elapsed:.2f} seconds")
        print(f"- Names per second: {batch_size/elapsed:,.0f}")
        assert len(names) == batch_size

def test_memory_efficiency(generator):
    """Test memory efficiency with incremental generation."""
    print("\nMemory Efficiency Test:")
    
    total_names = 50_000_000
    batch_size = 1_000_000
    batches = total_names // batch_size
    
    start_time = time.time()
    names_generated = 0
    
    for _ in range(batches):
        names = generator.get_full_names(batch_size)
        names_generated += len(names)
        
        # Clear the names to free memory
        del names
    
    elapsed = time.time() - start_time
    print(f"\nGenerated {names_generated:,} names in batches of {batch_size:,}:")
    print(f"- Total time: {elapsed:.2f} seconds")
    print(f"- Average names per second: {names_generated/elapsed:,.0f}")
    
    assert names_generated == total_names

def test_name_uniqueness(generator):
    """Test the distribution of generated names."""
    print("\nUniqueness Test:")
    
    # Generate a large sample of names
    sample_size = 100000
    names = generator.get_full_names(sample_size)
    
    # Check uniqueness
    unique_names = set(names)
    uniqueness_ratio = len(unique_names) / sample_size
    
    print(f"\nIn a sample of {sample_size:,} names:")
    print(f"- Unique names: {len(unique_names):,}")
    print(f"- Uniqueness ratio: {uniqueness_ratio:.2%}")
    
    # We expect a good distribution of names
    assert uniqueness_ratio > 0.9, "Low name uniqueness detected"

if __name__ == "__main__":
    # For manual testing with pytest
    pytest.main([__file__, "-v", "-k", "generate_different_sizes"])
