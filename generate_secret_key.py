from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("Generated Django SECRET_KEY:")
    print("=" * 50)
    print(secret_key)
    print("=" * 50)
    print("\nTo use this key on PythonAnywhere:")
    print("1. Go to your PythonAnywhere Dashboard")
    print("2. Click on 'Tasks' > 'Environment variables'")
    print("3. Set SECRET_KEY to the value above")
    print("4. Set DEBUG to 'false' for production")
