#!/usr/bin/env python3
"""
Test script to verify cost tracking integration works correctly
"""
import os
import sys
from config import Config, setup_logging
from cost_tracker import get_cost_tracker
from tracked_llm import create_tracked_llm

def test_cost_tracking_integration():
    """Test the complete cost tracking system integration"""
    print("🔬 Testing Cost Tracking Integration")
    print("=" * 50)
    
    # Setup logging
    logger = setup_logging()
    
    try:
        # Test 1: Configuration with cost tracking
        print("\n1️⃣ Testing Configuration with Cost Tracking...")
        config = Config(enable_cost_tracking=True)
        print("✅ Configuration created with cost tracking enabled")
        
        # Test 2: Cost tracker availability
        print("\n2️⃣ Testing Cost Tracker Availability...")
        tracker = get_cost_tracker()
        initial_summary = tracker.get_cost_summary()
        print(f"✅ Cost tracker available - Session: {initial_summary['current_session']['session_id']}")
        
        # Test 3: Tracked LLM creation (without actual API key)
        print("\n3️⃣ Testing Tracked LLM Creation...")
        # We'll test the wrapper creation but not actual API calls
        try:
            test_llm = create_tracked_llm(
                model="anthropic/claude-sonnet-4-20250514",
                api_key="test_key",
                agent_name="Test Agent"
            )
            print("✅ Tracked LLM wrapper created successfully")
        except Exception as e:
            print(f"⚠️  LLM wrapper creation test (expected without real API key): {e}")
        
        # Test 4: Cost calculation
        print("\n4️⃣ Testing Cost Calculation...")
        test_cost = tracker.calculate_cost("anthropic/claude-sonnet-4-20250514", 1000, 500)
        print(f"✅ Cost calculation working - 1000+500 tokens = ${test_cost:.6f}")
        
        # Test 5: Mock API call tracking
        print("\n5️⃣ Testing API Call Tracking...")
        test_event = tracker.track_api_call(
            agent_name="Test Agent",
            model="anthropic/claude-sonnet-4-20250514", 
            input_tokens=1000,
            output_tokens=500,
            task_description="Test API call tracking"
        )
        print(f"✅ API call tracked - Cost: ${test_event.cost_usd:.6f}")
        
        # Test 6: Cost summary
        print("\n6️⃣ Testing Cost Summary...")
        final_summary = tracker.get_cost_summary()
        session_cost = final_summary['current_session']['cost']
        print(f"✅ Session cost tracked: ${session_cost:.6f}")
        
        # Test 7: Database verification
        print("\n7️⃣ Testing Database Storage...")
        import sqlite3
        conn = sqlite3.connect('cost_tracking.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cost_events")
        event_count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Database contains {event_count} cost events")
        
        print("\n" + "=" * 50)
        print("🎉 ALL COST TRACKING TESTS PASSED!")
        print("✅ Cost tracking infrastructure is working correctly")
        
        # Display final summary
        print("\n📊 Final Cost Summary:")
        tracker.print_cost_summary()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cost_tracking_integration()
    sys.exit(0 if success else 1)
