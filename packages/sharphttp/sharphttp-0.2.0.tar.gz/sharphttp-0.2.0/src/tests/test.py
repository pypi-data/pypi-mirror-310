import asyncio
import time
from statistics import mean
import aiohttp
from sharphttp import ClientSession

async def test_aiohttp():
    async with aiohttp.ClientSession() as session:
        start = time.perf_counter()
        async with session.get('http://example.com') as response:
            await response.text()
        return time.perf_counter() - start

async def test_sharp_client():
    async with ClientSession() as session:
        start = time.perf_counter()
        response = await session.get('http://example.com')
        await response.text()
        return time.perf_counter() - start

async def main():
    # Warm up
    print("Warming up...")
    for _ in range(3):
        await test_aiohttp()
        await test_sharp_client()
    
    # Real tests
    print("\nRunning tests...")
    n_tests = 100
    
    # Test aiohttp
    aiohttp_times = []
    for _ in range(n_tests):
        time_taken = await test_aiohttp()
        aiohttp_times.append(time_taken)
    
    # Test sharp client
    sharp_times = []
    for _ in range(n_tests):
        time_taken = await test_sharp_client()
        sharp_times.append(time_taken)
    
    # Print results
    print(f"\nResults over {n_tests} requests:")
    print(f"{'Client':<15} {'Mean (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12}")
    print("-" * 51)
    print(f"{'Sharp Client':<15} {mean(sharp_times)*1000:>11.2f} {min(sharp_times)*1000:>11.2f} {max(sharp_times)*1000:>11.2f}")
    print(f"{'aiohttp':<15} {mean(aiohttp_times)*1000:>11.2f} {min(aiohttp_times)*1000:>11.2f} {max(aiohttp_times)*1000:>11.2f}")
    
    # Calculate improvement
    improvement = (mean(aiohttp_times) / mean(sharp_times) - 1) * 100
    print(f"\nSharp client is {improvement:.1f}% faster on average")

if __name__ == "__main__":
    asyncio.run(main())
