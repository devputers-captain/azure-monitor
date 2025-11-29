"""
Test script to generate various HTTP error codes for Azure Monitor tracking.
This script demonstrates how different HTTP status codes appear in Azure Monitor.
"""

import time

import requests

# Base URL - change if running on different host/port
BASE_URL = "http://localhost:8000"

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'


def test_endpoint(url: str, expected_status: int, description: str) -> dict:
    """
    Test an endpoint and return the result.
    
    Args:
        url: The endpoint URL
        expected_status: Expected HTTP status code
        description: Description of the test
    
    Returns:
        Dictionary with test results
    """
    try:
        response = requests.get(url, timeout=10)
        success = response.status_code == expected_status
        
        color = Colors.GREEN if success else Colors.RED
        status_symbol = "✓" if success else "✗"
        
        print(f"{color}{status_symbol} {description}{Colors.END}")
        print(f"   Status: {response.status_code} | Expected: {expected_status}")
        
        # Try to print response body if it's JSON
        try:
            if response.headers.get('content-type', '').startswith('application/json'):
                import json
                print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}...")
        except:
            pass
        
        print()
        
        return {
            "url": url,
            "description": description,
            "expected": expected_status,
            "actual": response.status_code,
            "success": success,
            "response_time": response.elapsed.total_seconds(),
        }
    
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}✗ {description}{Colors.END}")
        print(f"   Error: {str(e)}\n")
        return {
            "url": url,
            "description": description,
            "expected": expected_status,
            "actual": None,
            "success": False,
            "error": str(e),
        }


def run_http_error_tests():
    """Run comprehensive HTTP error code tests."""
    
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}  Azure Monitor - HTTP Error Code Testing{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    test_cases = [
        # Success cases
        (f"{BASE_URL}/", 200, "Root endpoint (200 OK)"),
        (f"{BASE_URL}/health", 200, "Health check (200 OK)"),
        
        # Client errors (4xx)
        (f"{BASE_URL}/demo/http-errors/400", 400, "Bad Request (400)"),
        (f"{BASE_URL}/demo/http-errors/401", 401, "Unauthorized (401)"),
        (f"{BASE_URL}/demo/http-errors/403", 403, "Forbidden (403)"),
        (f"{BASE_URL}/demo/http-errors/404", 404, "Not Found (404)"),
        (f"{BASE_URL}/demo/http-errors/429", 429, "Too Many Requests (429)"),
        
        # Server errors (5xx)
        (f"{BASE_URL}/demo/http-errors/500", 500, "Internal Server Error (500)"),
        (f"{BASE_URL}/demo/http-errors/503", 503, "Service Unavailable (503)"),
    ]
    
    results = []
    
    print(f"{Colors.YELLOW}Testing HTTP Status Codes...{Colors.END}\n")
    
    for url, expected_status, description in test_cases:
        result = test_endpoint(url, expected_status, description)
        results.append(result)
        time.sleep(0.5)  # Small delay between requests
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}  Test Summary{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    total = len(results)
    passed = sum(1 for r in results if r.get("success", False))
    failed = total - passed
    
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {failed}{Colors.END}\n")
    
    # Azure Portal instructions
    print(f"{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}  How to View in Azure Portal{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    print("1. Go to Azure Portal → Application Insights → Your Resource")
    print("2. Wait 2-5 minutes for telemetry ingestion")
    print("3. Navigate to different views:\n")
    
    print(f"{Colors.YELLOW}📊 View Failed Requests:{Colors.END}")
    print("   • Click 'Failures' → See all HTTP errors grouped by status code")
    print("   • Filter by status code: 400, 401, 403, 404, 429, 500, 503\n")
    
    print(f"{Colors.YELLOW}📈 View Request Statistics:{Colors.END}")
    print("   • Click 'Performance' → See response times and success rates")
    print("   • Sort by 'Failed requests' to see error-prone endpoints\n")
    
    print(f"{Colors.YELLOW}🔍 Query with KQL (Logs):{Colors.END}")
    print("   Click 'Logs' and run these queries:\n")
    
    print("   // View all failed requests")
    print("   requests")
    print("   | where timestamp > ago(1h)")
    print("   | where success == false")
    print("   | project timestamp, name, resultCode, duration")
    print("   | order by timestamp desc\n")
    
    print("   // Count errors by status code")
    print("   requests")
    print("   | where timestamp > ago(1h)")
    print("   | where success == false")
    print("   | summarize count() by resultCode")
    print("   | order by count_ desc\n")
    
    print("   // View 4xx vs 5xx errors (CORRECTED)")
    print("   requests")
    print("   | where timestamp > ago(1h)")
    print("   | where success == false")
    print("   | extend resultCodeInt = toint(resultCode)")
    print("   | extend errorType = case(")
    print("       resultCodeInt >= 400 and resultCodeInt < 500, '4xx Client Error',")
    print("       resultCodeInt >= 500, '5xx Server Error',")
    print("       'Other')")
    print("   | summarize count() by errorType")
    print()
    
    return results


if __name__ == "__main__":
    import sys
    
    print(f"\n{Colors.BLUE}Starting Azure Monitor HTTP Error Testing...{Colors.END}\n")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"{Colors.GREEN}✓ Server is running at {BASE_URL}{Colors.END}\n")
    except:
        print(f"{Colors.RED}✗ Server is not running at {BASE_URL}{Colors.END}")
        print(f"Please start the server first with: docker-compose up -d\n")
        sys.exit(1)
    
    # Run tests
    run_http_error_tests()
    
    print(f"\n{Colors.GREEN}✓ Testing complete! Check Azure Portal in 2-5 minutes.{Colors.END}")
    print(f"{Colors.YELLOW}💡 For load testing, run: python tests/load_testing.py{Colors.END}\n")

