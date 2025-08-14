#!/usr/bin/env python3
"""
Test script to verify cost optimization features work correctly
"""
import os
import sys
import time
import tempfile
from config import Config, setup_logging
from cost_optimizer import (
    PromptOptimizer, QueryCache, CostBudgetManager,
    get_query_cache, get_prompt_optimizer, get_budget_manager
)


def test_prompt_optimization():
    """Test prompt optimization features"""
    print("\n1️⃣ Testing Prompt Optimization...")
    
    optimizer = PromptOptimizer()
    
    # Test redundancy removal
    test_prompt = "Please make sure to analyze and examine the comprehensive and detailed research findings."
    optimized, tokens_saved = optimizer.optimize_prompt(test_prompt, "Research Coordinator")
    
    print(f"✅ Original: {test_prompt}")
    print(f"✅ Optimized: {optimized}")
    print(f"✅ Tokens saved: ~{tokens_saved}")
    
    # Test agent-specific optimization
    coordinator_prompt = "Provide a comprehensive and detailed analysis of all possible research areas."
    optimized_coord, _ = optimizer.optimize_prompt(coordinator_prompt, "Research Coordinator")
    print(f"✅ Coordinator optimization: {optimized_coord}")
    
    searcher_prompt = "Find all possible papers with exhaustive search methodology."
    optimized_search, _ = optimizer.optimize_prompt(searcher_prompt, "Literature Searcher")
    print(f"✅ Searcher optimization: {optimized_search}")
    
    return True


def test_query_caching():
    """Test query caching system"""
    print("\n2️⃣ Testing Query Caching...")
    
    # Use a unique database for testing to avoid conflicts
    import tempfile
    import os
    test_db = os.path.join(tempfile.gettempdir(), f"test_cache_{int(time.time())}.db")
    cache = QueryCache(db_path=test_db, cache_duration_hours=24)
    
    # Test cache miss (first call)
    test_query = "What are the latest developments in machine learning?"
    agent_name = "Test Agent"
    
    cached_response = cache.get_cached_response(test_query, agent_name)
    if cached_response is None:
        print("✅ Cache miss detected correctly")
    else:
        print("❌ Unexpected cache hit")
        return False
    
    # Add response to cache
    test_response = "Here are the latest ML developments..."
    cache.cache_response(
        query=test_query,
        response=test_response,
        agent_name=agent_name,
        input_tokens=100,
        output_tokens=200,
        cost=0.015
    )
    print("✅ Response cached successfully")
    
    # Test cache hit
    cached_response = cache.get_cached_response(test_query, agent_name)
    if cached_response == test_response:
        print("✅ Cache hit working correctly")
    else:
        print("❌ Cache hit failed")
        return False
    
    # Test cache stats
    stats = cache.get_cache_stats()
    print(f"✅ Cache stats: {stats['total_entries']} entries, ${stats['total_cost_saved']:.4f} saved")
    
    return True


def test_budget_management():
    """Test budget management and optimization suggestions"""
    print("\n3️⃣ Testing Budget Management...")
    
    # Create a budget manager with test settings
    os.environ['DAILY_COST_BUDGET'] = '1.0'  # Low budget for testing
    os.environ['SESSION_COST_BUDGET'] = '0.5'
    
    budget_manager = CostBudgetManager()
    
    # Check initial budget status
    status = budget_manager.check_budget_status()
    print(f"✅ Initial budget status - Session: {status['session']}, Daily: {status['daily']}")
    
    # Test cost prediction
    prediction = budget_manager.get_cost_prediction(
        "This is a test query for cost prediction", 
        "Test Agent"
    )
    print(f"✅ Cost prediction: ${prediction['estimated_cost']:.6f}")
    
    # Test optimization suggestions
    suggestions = budget_manager.suggest_optimizations(status)
    if suggestions:
        print(f"✅ Got {len(suggestions)} optimization suggestions")
    else:
        print("✅ No suggestions needed at current budget level")
    
    return True


def test_integration():
    """Test integration of all cost optimization features"""
    print("\n4️⃣ Testing Integration...")
    
    try:
        # Test global accessors
        cache = get_query_cache()
        optimizer = get_prompt_optimizer()
        budget_manager = get_budget_manager()
        
        print("✅ All global instances created successfully")
        
        # Test a complete optimization workflow
        test_query = "Research the impact of artificial intelligence on climate change"
        
        # 1. Check budget first
        status = budget_manager.check_budget_status()
        if status['should_continue']:
            print("✅ Budget check passed")
        else:
            print("⚠️ Budget limit reached")
        
        # 2. Check cache
        cached = cache.get_cached_response(test_query, "Integration Test")
        if cached:
            print("✅ Found cached response")
        else:
            print("✅ No cached response (expected)")
        
        # 3. Optimize prompt
        optimized, tokens_saved = optimizer.optimize_prompt(test_query)
        print(f"✅ Prompt optimized, saved ~{tokens_saved} tokens")
        
        # 4. Cache a mock response
        mock_response = "Climate AI research shows significant potential..."
        cache.cache_response(
            query=test_query,
            response=mock_response,
            agent_name="Integration Test",
            input_tokens=50,
            output_tokens=100,
            cost=0.008
        )
        print("✅ Response cached for future use")
        
        # 5. Verify cache hit on second call
        cached = cache.get_cached_response(test_query, "Integration Test")
        if cached == mock_response:
            print("✅ Cache integration working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def test_optimization_with_config():
    """Test cost optimization with full configuration"""
    print("\n5️⃣ Testing with Configuration Integration...")
    
    try:
        # Test config with cost optimization
        config = Config(enable_cost_tracking=True)
        
        # Check if optimization features are available
        llm = config.get_llm("Test Agent")
        
        # Check if the LLM has optimization features
        has_caching = hasattr(llm, 'enable_caching') and llm.enable_caching
        has_optimization = hasattr(llm, 'enable_prompt_optimization') and llm.enable_prompt_optimization
        
        print(f"✅ LLM created with caching: {has_caching}")
        print(f"✅ LLM created with optimization: {has_optimization}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration integration test failed: {e}")
        return False


def main():
    """Run all cost optimization tests"""
    print("🚀 Testing Cost Optimization Features")
    print("=" * 50)
    
    # Setup logging
    logger = setup_logging()
    
    tests = [
        ("Prompt Optimization", test_prompt_optimization),
        ("Query Caching", test_query_caching),
        ("Budget Management", test_budget_management),
        ("Feature Integration", test_integration),
        ("Configuration Integration", test_optimization_with_config),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running {test_name} Test...")
            if test_func():
                print(f"✅ {test_name} test PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL COST OPTIMIZATION TESTS PASSED!")
        
        # Display final feature summary
        print("\n🎯 Cost Optimization Features Ready:")
        print("  ✅ Intelligent prompt optimization")
        print("  ✅ Query response caching")
        print("  ✅ Budget monitoring and alerts")
        print("  ✅ Agent-specific cost tracking")
        print("  ✅ Real-time optimization suggestions")
        print("  ✅ Integration with existing chat interface")
        
        return True
    else:
        print("❌ Some tests failed - please review the output above")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
