from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import SelectField, FileField
from wtforms.validators import Regexp, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

def validate_image(form, field):
    if field.data:
        filename = field.data.filename.lower()
        if not (filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg')):
            flash('Invalid file format. Only PNG, JPG, and JPEG are allowed.', 'danger')
            raise ValidationError('Invalid file format. Only PNG, JPG, and JPEG are allowed.')

class HairChangerForm(FlaskForm):
    image = FileField('Upload Image', validators=[DataRequired(), validate_image])
    hair_style = SelectField('Hair Style', choices=[
        ('', 'Select a hairstyle'),
        ('BuzzCut', 'BuzzCut'), ('UnderCut', 'UnderCut'), ('Pompadour', 'Pompadour'),
        ('SlickBack', 'SlickBack'), ('CurlyShag', 'CurlyShag'), ('WavyShag', 'WavyShag'),
        ('FauxHawk', 'FauxHawk'), ('Spiky', 'Spiky'), ('CombOver', 'CombOver'),
        ('HighTightFade', 'HighTightFade'), ('ManBun', 'ManBun'), ('Afro', 'Afro'),
        ('LowFade', 'LowFade'), ('UndercutLongHair', 'UndercutLongHair'),
        ('TwoBlockHaircut', 'TwoBlockHaircut'), ('TexturedFringe', 'TexturedFringe'),
        ('BluntBowlCut', 'BluntBowlCut'), ('LongWavyCurtainBangs', 'LongWavyCurtainBangs'),
        ('MessyTousled', 'MessyTousled'), ('CornrowBraids', 'CornrowBraids'),
        ('LongHairTiedUp', 'LongHairTiedUp'), ('Middle-parted', 'Middle-parted'),
        ('ShortPixieWithShavedSides', 'ShortPixieWithShavedSides'),
        ('ShortNeatBob', 'ShortNeatBob'), ('DoubleBun', 'DoubleBun'), ('Updo', 'Updo'),
        ('Spiked', 'Spiked'), ('bowlCut', 'bowlCut'), ('Chignon', 'Chignon'),
        ('PixieCut', 'PixieCut'), ('SlickedBack', 'SlickedBack'), ('LongCurly', 'LongCurly'),
        ('CurlyBob', 'CurlyBob'), ('StackedCurlsInShortBob', 'StackedCurlsInShortBob'),
        ('SidePartCombOverHairstyleWithHighFade', 'SidePartCombOverHairstyleWithHighFade'),
        ('WavyFrenchBobVibesfrom1920', 'WavyFrenchBobVibesfrom1920'), ('BobCut', 'BobCut'),
        ('ShortTwintails', 'ShortTwintails'), ('ShortCurlyPixie', 'ShortCurlyPixie'),
        ('LongStraight', 'LongStraight'), ('LongWavy', 'LongWavy'), ('FishtailBraid', 'FishtailBraid'),
        ('TwinBraids', 'TwinBraids'), ('Ponytail', 'Ponytail'), ('Dreadlocks', 'Dreadlocks'),
        ('Cornrows', 'Cornrows'), ('ShoulderLengthHair', 'ShoulderLengthHair'),
        ('LooseCurlyAfro', 'LooseCurlyAfro'), ('LongTwintails', 'LongTwintails'),
        ('LongHimeCut', 'LongHimeCut'), ('BoxBraids', 'BoxBraids')
    ], validators=[DataRequired()])
    color = SelectField('Hair Color', choices=[
        ('unchanged', 'Select a color'),
        ('blonde', 'Blonde'), ('platinumBlonde', 'Platinum Blonde'), ('brown', 'Brown'),
        ('lightBrown', 'Light Brown'), ('blue', 'Blue'), ('lightBlue', 'Light Blue'),
        ('purple', 'Purple'), ('lightPurple', 'Light Purple'), ('pink', 'Pink'),
        ('black', 'Black'), ('white', 'White'), ('grey', 'Grey'), ('silver', 'Silver'),
        ('red', 'Red'), ('orange', 'Orange'), ('green', 'Green'), ('gradient', 'Gradient'),
        ('multicolored', 'Multicolored'), ('darkBlue', 'Dark Blue'), ('burgundy', 'Burgundy'),
        ('darkGreen', 'Dark Green')
    ])
    