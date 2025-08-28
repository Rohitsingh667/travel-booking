1. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the database:**

   ```bash
   python manage.py migrate
   ```

3. **Add some sample data:**

   ```bash
   python manage.py create_sample_data
   ```

4. **Run:**

   ```bash
   python manage.py runserver
   ```

5. **Open your browser** and go to `http://127.0.0.1:8000`

## What the sample data creates

The `python manage.py create_sample_data` command creates:

- **Admin user**: `admin` / `admin123`
- **5 travel options**: flights, trains, and buses between major Indian cities (Mumbai, Delhi, Bangalore, etc.)
- All sample travel data is set for 7 days from today

**Where it's stored**: All data goes into your SQLite database (`db.sqlite3` file) in the following tables:

- `auth_user` - for the admin user
- `booking_traveloption` - for the travel options

You can also just create your own account by clicking the signup link.
