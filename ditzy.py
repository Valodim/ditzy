# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import email
import mailproc
import hashlib
import re
import datetime

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'ditzy.db'),
    DEBUG=True,
    SECRET_KEY='abc'
))
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'], isolation_level=None)
    rv.row_factory = sqlite3.Row
    rv.execute("pragma foreign_keys=on")
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_antrag():
    if 'logged_in' not in session:
        return render_template('nope.html')

    db = get_db()
    cur = db.execute(""" select id, name, short from vorstand order by id """)
    vorstand = dict([ (row['id'],(row['name'],row['short'])) for row in cur.fetchall() ])

    cur = db.execute("""
        select antrag.id, msg_id, subject, ub, starter,
                group_concat(vorstand) as vorstand, group_concat(state) as state, group_concat(verified) as verified
            from antrag
                left join votes on (antrag.id = votes.antrag)
            group by antrag.id
        """)
    row = cur.fetchone()
    entries = []
    while row is not None:
        votes = {}
        states = row['state'].split(',')
        verified = row['verified'].split(',')
        for v in reversed(row['vorstand'].split(',')):
            votes[int(v)] = (int(states.pop()), int(verified.pop()))

        entries.append({
            'subject': row['subject'],
            'ub': row['ub'],
            'starter': row['starter'],
            'votes': votes,
        })

        row = cur.fetchone()

    return render_template('show_antrags.html', vorstand=vorstand, entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST' and 'password' in request.form and 'username' in request.form:
        db = get_db()
        pw = hashlib.sha256(request.form['password']).hexdigest()
        cur = db.execute('select name from vorstand where name = ? AND pass = ?',
                [ request.form['username'], pw ])
        row = cur.fetchall()
        if len(row) == 0:
            error = 'bad username or password'
        else:
            session['logged_in'] = True
            session['nick'] = row[0]['name']
            flash('You were logged in')
            return redirect(url_for('show_antrag'))
    return render_template('login.html', error=error)

@app.route('/post', methods=['POST'])
def postmail():
    if request.remote_addr != '127.0.0.1':
        abort(403)
    if not request.data:
        abort(500)

    # parse mail
    mail = email.message_from_string(request.data)
    if not mail.has_key('List-Id') or 'vorstand.stratum0.org' not in mail.get('List-Id'):
        app.logger.warning('List-Id should be vorstand.stratum0.org!')
        return "no list-id, ignoring\n"

    mid = mail.get('Message-Id')
    if mid is None:
        app.logger.warning('Message id found, ignoring mail!')
        return "no msg id, ignoring\n"

    # at this point, it's either an [antrag] thread start, or a reply
    db = get_db()

    cur = db.execute('select msg_id from msgs where msg_id = ?', [ mid ])
    if cur.fetchone():
        app.logger.debug('Ignoring duplicate')
        return "duplicate msg\n"

    # parse subject
    subject = email.utils.unquote(mail.get('Subject')) if mail.has_key('Subject') else ''

    # get parent reply
    pid = mail.get('In-Reply-To')
    if pid is None and '[antrag]' not in subject.lower():
        app.logger.debug('Ignoring non-antrag thread start')
        return "Ignoring non-antrag thread start\n"

    # check if it's a reply
    if pid is not None:
        cur = db.execute('select thread_id from msgs where msg_id LIKE ?', [ pid ])
        # we either need a parent to proceed
        row = cur.fetchone()
        if row:
            tid, = row
        # or maybe this is an antrag with a rogue in-reply-to header
        elif '[antrag]' in subject.lower():
            # new thread -> thread id == msg id
            tid = mid
        else:
            app.logger.debug('no corresponding antrag found')
            return "no corresponding antrag found\n"
    else:
        # it must be a new antrag, then (we checked this above)
        tid = mid

    # add msg to tracking table
    db.execute('replace into msgs (msg_id, thread_id) VALUES (?, ?) ', [ mid, tid ])

    aid = None

    subject = re.sub('\[antrag\]', '', subject, re.IGNORECASE)
    subject = subject.replace('[#StratumV]', '')

    # if message id is thread id, this is a new antrag!
    if mid == tid:
        # insert new aid into db
        app.logger.debug('Creating new antrag %s', subject)
        date = datetime.datetime.now()
        ub = 'ub-{}-{:2d}-'.format(date.year, date.month)
        cur = db.execute('select max(ub) as ub from antrag where ub LIKE ?', [ ub + '%' ])
        row, = cur.fetchone()
        if row is not None:
            ub = ub + '{:2d}'.format(int(row[11:])+1)
        else:
            ub = ub + '01'
        cur = db.execute('insert into antrag (msg_id, subject, ub, starter, public) values (?, ?, ?, ?, ?)',
            [ mid, subject, 'ub-04-01', mail.get('From'), 'false' ]
        )
        aid = cur.lastrowid
        app.logger.debug('New antrag id: %d', aid)

    # everything further on deals with votes

    # find sender
    f = mail.get('From')
    f = f[f.find('<')+1 : f.find('>')]
    cur = db.execute('select id, pubkey from vorstand where ? LIKE email', [ f ])
    row = cur.fetchone()
    if not row:
        app.logger.debug('unknown sender, ignoring potential vote in msg %s', mid)
        return "unknown sender\n"
    vid, key = row

    # find if there is a vote, and try to verify it
    keypath = os.path.join(app.root_path, 'keys/{}.gpg'.format(key))
    result = mailproc.check(mail, keypath)

    if not result:
        app.logger.debug('No signed data found in msg %s', mid)
        return "no signed data\n"

    text, sig, state, verified = result

    if state is None:
        app.logger.debug('No vote found in msg %s', mid)
        return "no vote\n"

    # if there is no previous aid (from new thread), get it
    if aid is None:
        cur = db.execute('select id from antrag where msg_id = ?', [ tid ])
        row = cur.fetchone()
        if row:
            aid, = row
        else:
            app.logger.debug('No antrag found for msg %s', mid)
            return "error finding antrag\n"

    app.logger.debug('Inserting vote %d from %s for %s, sign status %d', state, vid, aid, verified)
    db.execute('replace into votes (antrag, vorstand, text, sig, verified, state) VALUES (?, ?, ?, ?, ?, ?)', [
        aid, vid, text, sig, verified, state
    ])

    return "ok: vote {} from {} for antrag {}, verification {}\n".format(state, vid, aid, verified)

@app.route('/clear')
def clear():
    db = get_db()
    db.execute('delete from votes')
    db.execute('delete from antrag')
    db.execute('delete from msgs')
    return "ok\n"

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_antrag'))

if __name__ == '__main__':
    app.run()

