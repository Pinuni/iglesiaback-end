@auth.route('/registro', methods=['POST'])
def registrar_usuario():
    username = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    print("Nombre:", username)
    print("Email:", email)
    print("Password:", password)
    print("Confirm:", confirm_password)

    if not all([username, email, password, confirm_password]):
        return jsonify({'message': 'Todos los campos son obligatorios'}), 400

    if password != confirm_password:
        return jsonify({'message': 'Las contraseñas no coinciden'}), 400

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                if cursor.fetchone():
                    return jsonify({'message': 'El usuario ya existe'}), 400

                cursor.execute(
                    "INSERT INTO usuarios (username, email, password, created_at) VALUES (%s, %s, %s, %s)",
                    (username, email, password, datetime.now())
                )
                connection.commit()
                print("Usuario registrado:", email)
                return redirect("https://iglesiarefugioquebs.site/login.html")

    except Exception as e:
        import traceback
        print("🔥 Error al registrar:", e)
        traceback.print_exc()
        return jsonify({'message': 'Error interno del servidor'}), 500
