"""
Load testing script for Azure Monitor demo.
Generates random requests to various endpoints including error codes.
"""
import random
import sys
import time

import requests

BASE_URL = "http://localhost:8000"

# Mix of successful and error endpoints
ENDPOINTS = [
    "/demo/info",
    "/demo/warning",
    "/demo/error",
    "/demo/metrics",
    "/demo/trace",
    "/demo/dependency",
    "/demo/all",
    "/demo/http-errors/400",
    "/demo/http-errors/404",
    "/demo/http-errors/500",
    "/demo/http-errors/503",
]


def run_load_test(iterations: int = 20):
    """Run load test with specified number of iterations."""
    print("\n🚀 Starting load test...\n")
    
    success_count = 0
    error_count = 0
    
    for i in range(iterations):
        endpoint = random.choice(ENDPOINTS)
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            if response.status_code < 400:
                success_count += 1
                print(f"✅ Request {i+1}/{iterations}: {endpoint} → {response.status_code}")
            else:
                error_count += 1
                print(f"❌ Request {i+1}/{iterations}: {endpoint} → {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"❌ Request {i+1}/{iterations}: {endpoint} → Error: {str(e)}")
        
        time.sleep(0.2)  # Small delay between requests
    
    print(f"\n📊 Load Test Results:")
    print(f"   Total: {iterations} requests")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📈 Error Rate: {(error_count/iterations)*100:.1f}%")
    print(f"\n💡 Check Azure Portal in 2-5 minutes to see the telemetry!\n")


if __name__ == "__main__":
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✓ Server is running at {BASE_URL}")
    except:
        print(f"✗ Server is not running at {BASE_URL}")
        print(f"Please start it with: docker-compose up -d\n")
        sys.exit(1)
    
    # Get number of iterations
    if len(sys.argv) > 1:
        iterations = int(sys.argv[1])
    else:
        iterations = 20
    
    run_load_test(iterations)
