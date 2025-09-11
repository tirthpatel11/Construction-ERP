from supabase import create_client, Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    try:
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            logger.error("Supabase credentials not configured")
            return None
        
        supabase: Client = create_client(
            settings.SUPABASE_URL, 
            settings.SUPABASE_ANON_KEY
        )
        return supabase
    except Exception as e:
        logger.error(f"Error creating Supabase client: {e}")
        return None

def sync_user_to_supabase(user_data):
    """Sync user data to Supabase"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
            
        # Insert or update user in Supabase
        result = supabase.table('users').upsert({
            'email': user_data.get('email'),
            'username': user_data.get('username'),
            'first_name': user_data.get('first_name', ''),
            'last_name': user_data.get('last_name', ''),
            'phone_number': user_data.get('phone_number', ''),
            'company': user_data.get('company', ''),
            'address': user_data.get('address', ''),
            'django_user_id': user_data.get('django_user_id'),
        }).execute()
        
        return result.data[0] if result.data else None
    except Exception as e:
        logger.error(f"Error syncing user to Supabase: {e}")
        return None