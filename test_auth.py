from auth import register_user, login_user

# Test registration
print("Testing registration...")
success, msg = register_user("test_user_ai", "test_pass_123")
print(f"Success: {success}, Message: {msg}")

# Test login
print("\nTesting login...")
success, msg = login_user("test_user_ai", "test_pass_123")
print(f"Success: {success}, Message: {msg}")
