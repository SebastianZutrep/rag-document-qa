from src.db import supabase

def login(email, password):
    print(f"Intentando iniciar sesión con email: {email}")
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        print("Respuesta de Supabase:", response)
        return response
    except Exception as e:
        print("Error en login:", str(e))
        raise

def signup(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })

def logout():
    return supabase.auth.sign_out()

def get_user():
    return supabase.auth.get_user()