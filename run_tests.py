#!/usr/bin/env python3
"""
Comprehensive test of all features without requiring a live Solace broker.
Tests argument parsing, validation, and message generation.
"""

import sys
import subprocess
import json

def run_command(cmd, should_fail=False):
    """Run a command and return the result."""
    print(f"\n{'='*80}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*80}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if should_fail:
        if result.returncode != 0:
            print("✓ Failed as expected")
            return True
        else:
            print("✗ Should have failed but didn't")
            return False
    else:
        if result.returncode == 0:
            print("✓ Succeeded as expected")
            return True
        else:
            print("✗ Failed unexpectedly")
            return False

def main():
    """Run comprehensive tests."""
    print("COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Help output
    print("\n\nTEST 1: Help Output")
    if run_command(["python3", "solace_producer.py", "--help"]):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 2: Negative count validation
    print("\n\nTEST 2: Negative Count Validation")
    if run_command([
        "python3", "solace_producer.py",
        "--host", "tcp://test:55555",
        "--vpn", "test",
        "--username", "test",
        "--topic", "test/topic",
        "--count", "-5",
        "--size", "100",
        "--rate", "10"
    ], should_fail=True):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 3: Zero size validation
    print("\n\nTEST 3: Zero Size Validation")
    if run_command([
        "python3", "solace_producer.py",
        "--host", "tcp://test:55555",
        "--vpn", "test",
        "--username", "test",
        "--topic", "test/topic",
        "--count", "10",
        "--size", "0",
        "--rate", "10"
    ], should_fail=True):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 4: Negative rate validation
    print("\n\nTEST 4: Negative Rate Validation")
    if run_command([
        "python3", "solace_producer.py",
        "--host", "tcp://test:55555",
        "--vpn", "test",
        "--username", "test",
        "--topic", "test/topic",
        "--count", "10",
        "--size", "100",
        "--rate", "-1"
    ], should_fail=True):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 5: Message generation test
    print("\n\nTEST 5: Message Generation Test")
    if run_command(["python3", "test_generation.py"]):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Final summary
    print("\n\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print(f"Total Tests: {tests_passed + tests_failed}")
    print("="*80)
    
    if tests_failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {tests_failed} TEST(S) FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
