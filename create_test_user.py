from django.contrib.auth import get_user_model
User = get_user_model()
print(f"User Model: {User}")
if not User.objects.filter(username='testuser').exists():
    u = User.objects.create_user('testuser', 'test@example.com', 'testpass')
    print(f"User created: {u.username}")
else:
    u = User.objects.get(username='testuser')
    u.set_password('testpass')
    u.save()
    print("User exists, password reset to 'testpass'")

print("All users:")
for user in User.objects.all():
    print(f"- {user.username} (active: {user.is_active})")
