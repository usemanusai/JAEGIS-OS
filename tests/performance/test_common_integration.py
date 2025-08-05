#!/usr/bin/env python3
"""
Test integration with JAEGIS Common Library
==========================================

This test verifies that the JAEGIS-METHOD-v2.1.1 project can successfully
import and use functions from the common shared library.
"""

import sys
import os
from pathlib import Path

# Add the common library to the path for testing
common_path = str(Path(__file__).parent.parent.parent / "common")
sys.path.insert(0, common_path)
print(f"Added to path: {common_path}")

def test_common_library_import():
    """Test that we can import from the common library"""
    try:
        # Try direct import first
        import utils.parsing_utils as parsing_utils
        print("✅ Successfully imported parsing utilities from common library")
        return True
    except ImportError as e:
        print(f"❌ Failed to import from common library: {e}")
        print(f"Current sys.path includes: {sys.path[:3]}...")
        return False

def test_parsing_functions():
    """Test that the parsing functions work correctly"""
    try:
        from utils.parsing_utils import parse_python_file, get_file_handler
        
        # Test with this file itself
        current_file = __file__
        
        # Test get_file_handler
        file_type, parser_func = get_file_handler(current_file)
        assert file_type == "python", f"Expected 'python', got '{file_type}'"
        
        # Test parse_python_file
        result = parse_python_file(current_file)
        assert "functions" in result, "Expected 'functions' key in result"
        assert "classes" in result, "Expected 'classes' key in result"
        assert "imports" in result, "Expected 'imports' key in result"
        
        print("✅ Parsing functions work correctly")
        return True
    except Exception as e:
        print(f"❌ Parsing functions failed: {e}")
        return False

def test_markdown_parsing():
    """Test markdown parsing functionality"""
    try:
        from utils.parsing_utils import parse_markdown_file
        
        # Create a temporary markdown file for testing
        test_md_content = """# Test Document

## Section 1
Some content here.

### Subsection 1.1
More content.

## Section 2
Final content.
"""
        
        test_file = Path(__file__).parent / "test_temp.md"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_md_content)
        
        try:
            result = parse_markdown_file(str(test_file))
            assert "headings" in result, "Expected 'headings' key in result"
            assert len(result["headings"]) == 4, f"Expected 4 headings, got {len(result['headings'])}"
            
            # Check heading levels
            expected_levels = [1, 2, 3, 2]
            actual_levels = [h["level"] for h in result["headings"]]
            assert actual_levels == expected_levels, f"Expected levels {expected_levels}, got {actual_levels}"
            
            print("✅ Markdown parsing works correctly")
            return True
        finally:
            # Clean up test file
            if test_file.exists():
                test_file.unlink()
                
    except Exception as e:
        print(f"❌ Markdown parsing failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🧪 Testing JAEGIS Common Library Integration")
    print("=" * 50)
    
    tests = [
        test_common_library_import,
        test_parsing_functions,
        test_markdown_parsing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\n🔍 Running {test.__name__}...")
        if test():
            passed += 1
        else:
            print(f"   Test failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Common library integration successful.")
        return True
    else:
        print("❌ Some tests failed. Check the integration setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
