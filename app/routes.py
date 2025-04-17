from flask import Blueprint, render_template, request, jsonify, session, redirect, flash
from flask_login import login_required
from forms.forms import HairChangerForm
from hair.core import run_hair_inference
from utils.inference import chat_with_ai
from PIL import Image
import io
import os
from time import sleep

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        image_file = request.files.get('image_path')

        image_path = None
        if image_file:
            image_path = f"/tmp/{image_file.filename}"
            image_file.save(image_path)

        ai_response = chat_with_ai(user_input, image_path, session['chat_history'])
        session['chat_history'].append({"role": "user", "content": user_input})
        session['chat_history'].append({"role": "assistant", "content": ai_response})
        session.modified = True

        return jsonify({"response": ai_response})
    return render_template('chat.html', chat_history=session['chat_history'][1:])

@main_bp.route('/clear_chat')
@login_required
def clear_chat():
    session.pop('chat_history', None)
    return redirect('/chat')

@main_bp.route("/hairchanger", methods=['GET', 'POST'])
@login_required
def hairchanger():
    form = HairChangerForm()

    if request.method == 'POST' and form.validate_on_submit():
        image_file = form.image.data
        hair_style = form.hair_style.data
        color = form.color.data if form.color.data != "unchanged" else None

        if not image_file:
            flash("Please upload an image.", "danger")
            return jsonify({"error": "Image not provided"}), 400

        image_bytes = io.BytesIO()
        image = Image.open(image_file)
        image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        output_path = run_hair_inference(image_bytes, hair_style, color)

        return jsonify({
            "result_image_url": output_path,
            "message": "Hairstyle changed successfully!"
        })

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field} error: {error}", "danger")
    return render_template("hairchanger.html", form=form)
