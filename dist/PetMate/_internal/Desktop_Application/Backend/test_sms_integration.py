# test_sms_integration.py
import os
import sys

# Add the project to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'myproject'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django

django.setup()

from petInfoSys.sms_utils import PhilSMSService


def test_philsms():
    print("=== Testing PhilSMS Integration ===\n")

    try:
        # 1. Initialize service
        sms_service = PhilSMSService()
        print("✓ SMS Service initialized successfully")
        print(f"  Sender ID: {sms_service.sender_id}")

        # 2. Check balance (if API supports it)
        print("\n2. Checking balance...")
        balance_result = sms_service.check_balance()
        if balance_result.get('success'):
            print(f"✓ Balance check successful")
            print(f"  Data: {balance_result.get('data', 'N/A')}")
        else:
            print(f"✗ Balance check failed: {balance_result.get('error', 'Unknown error')}")
            print("  (This is okay if your API plan doesn't include balance endpoint)")

        # test_sms_integration.py - Uncomment and modify this section:
        print("\n3. Testing SMS send...")
        test_number = "639272483891"  # ← REPLACE THIS with YOUR actual test number
        test_message = "Test SMS from PetMate Animal Clinic system"

        send_result = sms_service.send_sms(test_number, test_message)

        if send_result.get('success'):
            print(f"✓ SMS sent successfully!")
            print(f"  Status: {send_result.get('status')}")
            print(f"  Message: {send_result.get('message')}")
            print(f"  Full response: {send_result}")
        else:
            print(f"✗ SMS sending failed:")
            print(f"  Error: {send_result.get('error')}")
            print(f"  Full response: {send_result}")

        print("\n=== Test Complete ===")
        print("\nNext steps:")
        print("1. Update your .env file with actual PHILSMS_API_KEY")
        print("2. Uncomment the SMS sending test above")
        print("3. Run this test again with a real phone number")

    except Exception as e:
        print(f"✗ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_philsms()