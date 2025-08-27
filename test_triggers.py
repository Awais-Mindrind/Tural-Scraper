#!/usr/bin/env python3
"""
Test script for the new modular TikTok Scraper system
"""

import requests
import time
import json
import os

# API base URL
BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing API endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   API Info: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test active hashtags
    try:
        response = requests.get(f"{BASE_URL}/active-hashtags")
        print(f"✅ Active hashtags: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Active hashtags failed: {e}")
    
    # Test LLM query endpoint
    try:
        data = {"query": "Find TikTok profiles about travel with more than 10k followers"}
        response = requests.post(f"{BASE_URL}/llm-query", json=data)
        print(f"✅ LLM query: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ LLM query failed: {e}")
    
    # Test starting a scraper
    try:
        data = {"hashtag": "test", "num_profiles": 10}
        response = requests.post(f"{BASE_URL}/start-scraper", json=data)
        print(f"✅ Start scraper: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            task_id = response.json()["task_id"]
            print(f"   Task ID: {task_id}")
            
            # Test task status
            time.sleep(2)
            response = requests.get(f"{BASE_URL}/task-status/{task_id}")
            print(f"✅ Task status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
    except Exception as e:
        print(f"❌ Start scraper failed: {e}")
    
    # Test LLM-initiated scraper
    try:
        data = {"query": "Find food bloggers on TikTok"}
        response = requests.post(f"{BASE_URL}/start-scraper-with-llm", json=data, params={"num_profiles": 50})
        print(f"✅ LLM scraper: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ LLM scraper failed: {e}")
    
    # Test active tasks
    try:
        response = requests.get(f"{BASE_URL}/active-tasks")
        print(f"✅ Active tasks: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Active tasks failed: {e}")
    
    # Test task statistics
    try:
        response = requests.get(f"{BASE_URL}/task-statistics")
        print(f"✅ Task statistics: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Task statistics failed: {e}")
    
    # Test profile endpoints
    try:
        # Test GET /profiles with filters
        response = requests.get(f"{BASE_URL}/profiles", params={
            "hashtag": "travel",
            "limit": 10
        })
        print(f"✅ GET /profiles: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test GET /profiles/stats
        response = requests.get(f"{BASE_URL}/profiles/stats")
        print(f"✅ GET /profiles/stats: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test GET /profiles/search
        response = requests.get(f"{BASE_URL}/profiles/search", params={
            "q": "travel",
            "limit": 5
        })
        print(f"✅ GET /profiles/search: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test POST /profiles/ai
        data = {"query": "Find profiles with travel content and high followers"}
        response = requests.post(f"{BASE_URL}/profiles/ai", json=data)
        print(f"✅ POST /profiles/ai: {response.status_code}")
        print(f"   Response: {response.json()}")
        
    except Exception as e:
        print(f"❌ Profile endpoints failed: {e}")

def test_airtable_integration():
    """Test Airtable integration"""
    print("\n🔗 Testing Airtable integration...")
    
    try:
        from airtable import get_active_hashtags
        hashtags = get_active_hashtags()
        print(f"✅ Active hashtags from Airtable: {len(hashtags)}")
        print(f"   Hashtags: {hashtags[:5]}...")  # Show first 5
    except Exception as e:
        print(f"❌ Airtable integration failed: {e}")

def test_llm_integration():
    """Test LLM integration"""
    print("\n🤖 Testing LLM integration...")
    
    try:
        from llm_query import parse_query_to_filters
        
        # Test query parsing
        test_queries = [
            "Find travel influencers with more than 50k followers",
            "Show me food bloggers from USA",
            "Get fitness profiles with high engagement"
        ]
        
        for query in test_queries:
            try:
                filters = parse_query_to_filters(query)
                print(f"✅ Query parsed: '{query}'")
                print(f"   Filters: {filters}")
            except Exception as e:
                print(f"❌ Failed to parse query '{query}': {e}")
                
    except Exception as e:
        print(f"❌ LLM integration failed: {e}")

def test_task_manager():
    """Test task manager functionality"""
    print("\n⚙️ Testing Task Manager...")
    
    try:
        from task_manager import task_manager, generate_task_id, create_task_info
        
        # Test task creation
        task_id = generate_task_id()
        print(f"✅ Generated task ID: {task_id}")
        
        # Test task info creation
        task_info = create_task_info("test_hashtag", 100, "test")
        print(f"✅ Created task info: {task_info}")
        
        # Test task manager
        task_manager.add_task(task_id, task_info)
        print(f"✅ Added task to manager")
        
        # Test getting task status
        status = task_manager.get_task_status(task_id)
        print(f"✅ Task status: {status.status}")
        
        # Test statistics
        stats = task_manager.get_task_statistics()
        print(f"✅ Task statistics: {stats}")
        
    except Exception as e:
        print(f"❌ Task manager test failed: {e}")

def test_schemas():
    """Test schema validation"""
    print("\n📋 Testing Schema Validation...")
    
    try:
        from schemas import ScraperRequest, ScraperResponse, LLMQueryResponse
        
        # Test ScraperRequest
        request_data = {"hashtag": "test", "num_profiles": 100, "priority": 2}
        request = ScraperRequest(**request_data)
        print(f"✅ ScraperRequest validation: {request}")
        
        # Test ScraperResponse
        response_data = {
            "task_id": "test_123",
            "message": "Test message",
            "status": "queued",
            "hashtags": ["test"]
        }
        response = ScraperResponse(**response_data)
        print(f"✅ ScraperResponse validation: {response}")
        
        # Test LLMQueryResponse
        from schemas import ProfileFilters
        filters = ProfileFilters(hashtag="test", min_followers=1000)
        llm_response = LLMQueryResponse(filters=filters, query="test query")
        print(f"✅ LLMQueryResponse validation: {llm_response}")
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")

if __name__ == "__main__":
    print("🚀 TikTok Scraper Modular System Test Suite")
    print("=" * 60)
    
    # Test individual components first
    test_schemas()
    test_task_manager()
    test_llm_integration()
    test_airtable_integration()
    
    # Test API endpoints (only if server is running)
    print("\n" + "=" * 60)
    print("Note: API tests require the server to be running on localhost:5000")
    print("Start the server with: python triggers.py")
    
    try:
        test_api_endpoints()
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: python triggers.py")
    except Exception as e:
        print(f"❌ API tests failed: {e}")
    
    print("\n✅ Test suite completed!")
    print("\n📁 New Modular Structure:")
    print("   - schemas.py: All BaseModel classes")
    print("   - task_manager.py: Task management and threading")
    print("   - api.py: FastAPI endpoints and LLM integration")
    print("   - triggers.py: Cron jobs and scheduling")
    print("   - airtable.py: Airtable integration")
    print("   - tikTok_Scraper.py: Enhanced scraper with logging")
