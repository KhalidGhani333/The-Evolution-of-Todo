"""
Run Phase III database migration
"""
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ Error: DATABASE_URL not found in .env file")
    exit(1)

print("🔄 Running Phase III migration...")
print(f"📊 Database: {DATABASE_URL.split('@')[1].split('/')[0]}")

try:
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Read migration file
    with open('migrations/003_add_chat_tables.sql', 'r') as f:
        migration_sql = f.read()

    # Execute migration
    cursor.execute(migration_sql)
    conn.commit()

    print("✅ Migration completed successfully!")

    # Verify tables
    cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('conversations', 'messages', 'tool_calls')
        ORDER BY table_name;
    """)

    tables = cursor.fetchall()
    print(f"\n📋 Created tables:")
    for table in tables:
        print(f"   ✓ {table[0]}")

    cursor.close()
    conn.close()

    print("\n🎉 Phase III database setup complete!")
    print("💬 You can now use the AI chat feature!")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Try using Neon Web Console instead:")
    print("   1. Go to https://console.neon.tech/")
    print("   2. Open SQL Editor")
    print("   3. Copy-paste the SQL from migrations/003_add_chat_tables.sql")
    exit(1)
