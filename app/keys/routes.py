from flask import render_template, redirect, url_for, jsonify, request
from app.db import db
from app.keys import bp
from app.keys.forms import KeyForm
from flask_login import current_user, login_required
from app.models.users import User
from app.models.keys import Key

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = KeyForm()
    if form.validate_on_submit():
        key = Key(key_name=form.keyname.data, key_value=form.keyvalue.data, user_id=current_user.user_id)
        db.session.add(key)
        db.session.commit()
        return redirect(url_for('keys.index'))
    return render_template('index.html', key_form=form)

@bp.route('/<keyname>', methods=['GET', 'POST'])
@login_required
def key(keyname):
    """
    Returns a key for the user if it exists.
    """
    key = Key.query.filter_by(user_id=current_user.user_id, key_name=keyname).first()
    if request.method == 'POST':
        val = request.values.get('keyvalue')
        if not val:
            return jsonify({'status': '400', 'message': 'You must provide a keyvalue.'})
        if key:
            key.key_value = val
            db.session.commit()
            return jsonify({'status': '200', 'message': 'Key successfully updated.'})
        key = Key(key_name=keyname, key_value=val, user_id=current_user.user_id)
        db.session.add(key)
        db.session.commit()
        return jsonify({'status': '200', 'message': 'Key successfully created.'})

@bp.route('/delete_key/<int:keyid>', methods=['POST'])
@login_required
def delete_key(keyid):
    key = Key.query.get(int(keyid))
    if key is None or key.creator.user_id != current_user.user_id:
        # rather than throw a 403, return 404 so the user cannot infer if the key exists or not
        #return jsonify({'status': '404', 'message': 'Key not found/you do not have access to delete this key'})
        return redirect(url_for('keys.index'))
    db.session.delete(key)
    db.session.commit()
    return redirect(url_for('keys.index'))
    #return jsonify({'status': '200', 'message': 'Key successfully deleted'})
