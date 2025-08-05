#!/usr/bin/env python3
"""
Basic test to verify Python execution works
"""

print("🤖 JAEGIS Basic Test")
print("✅ Python execution working")
print("✅ Basic imports working")

import asyncio
import sys

async def test_async():
    print("✅ Async/await working")
    await asyncio.sleep(0.1)
    print("✅ Asyncio working")

if __name__ == "__main__":
    print(f"✅ Python version: {sys.version}")
    asyncio.run(test_async())
    print("🎉 All basic tests passed!")
