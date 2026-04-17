from flask import Flask, render_template, request, redirect, url_for, session
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
        data = c.fetchone()
        conn.close()
        if data:
            session['user'] = u
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        train = request.form['train']
        seats = request.form['seats']
        pnr = str(random.randint(100000,999999))

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (username,train,seats,pnr) VALUES (?,?,?,?)",
                  (session['user'],train,seats,pnr))
        conn.commit()
        conn.close()

        return render_template('ticket.html', train=train, seats=seats, pnr=pnr)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE username=?", (session['user'],))
    bookings = c.fetchall()
    conn.close()

    return render_template('dashboard.html', bookings=bookings)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
