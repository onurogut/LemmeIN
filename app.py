from flask import Flask, render_template, Response, request, redirect
from camera import Video
import os, time
import sqlite3 as sql
import string

app=Flask(__name__)
app.config['SECRET_KEY'] = 'baba'




@app.route('/')
def index():
    return render_template('index.html',)
@app.route('/mat201')
def mat201():
    return render_template('mat201.html',)
@app.route('/mat102')
def mat102():
    return render_template('mat102.html',)
@app.route('/listele', methods = ['GET', 'POST'])
def listele():
	c = sql.connect('ogrenciler.sqlite')
	cur = c.cursor()
	cur.execute("SELECT * from kayitlar LIMIT 100")
	test = cur.fetchall()
	cur.execute("SELECT ogrenci_no from kayitlar")
	#adi_cek = cur.fetchall()
	#for ad in adi_cek:
    #		print("%s" % ad)
	#cur.execute("SELECT COUNT(*) FROM kayitlar;")
	#satir_sayisi=cur.fetchone()

	#print (satir_sayisi)
	#print (ad[0])
	#print (ad[1])
	#for satir in satir_sayisi:
    #		print("%s" % satir)
	#for x in range(0, satir):
	#		print (x)
			#print (ad[x])
	#print('Düzenlenecek Öğrenci: ', request.form.get(ad[x]))
	return render_template('listele.html', test=test)
@app.route('/gecmis', methods = ['GET', 'POST'])
def gecmis():
	c = sql.connect('ogrenciler.sqlite')
	cur = c.cursor()
	cur.execute("SELECT * from girisler LIMIT 100")
	gecmis = cur.fetchall()
	cur.execute("SELECT ogrenci_no from girisler")
	return render_template('gecmis.html', gecmis=gecmis)


    


@app.route('/ders_kontrol', methods = ['GET', 'POST'])
def ders_kontrol():
	if request.method == 'POST':
		db = sql.connect("ogrenciler.sqlite")
		cs= db.cursor()
		ders_sec=request.form['ders_sec']
		print (ders_sec)
		if (ders_sec=="mat201"):
			print ("mat201 babacim")
			return redirect('http://localhost:5000/mat201')
		if (ders_sec=="mat102"):
			print ("mat102 babacim")
			return redirect('http://localhost:5000/mat102')

		#print (ders_sec[1])
		#ders_duzen = cs.execute('SELECT * FROM kayitlar WHERE ogrenci_no=?',(ders_sec,)).fetchall()
		#print (ders_duzen[0])
		return render_template('ders_kontrol.html',)

 
@app.route('/mat201_canli')
def mat201_canli():
	db = sql.connect("ogrenciler.sqlite")
	cs= db.cursor()
	last_row = cs.execute('SELECT ogrenci_no FROM girisler ORDER by id DESC LIMIT 1').fetchone()
	son_giris = cs.execute('SELECT zaman FROM girisler ORDER by id DESC LIMIT 1').fetchone()
	#print (son_giris[0])
	#print (last_row[0])
	satirkontrol=last_row[0]
	#print (satirkontrol)
	durum = cs.execute('select * from kayitlar where ogrenci_no=?',(satirkontrol,)).fetchone()
	#print (durum)
	ogrenci_adi_kontrol = cs.execute('select ogrenci_adi from kayitlar where ogrenci_no=?',(satirkontrol,)).fetchone()
	for ogrenci_adi in ogrenci_adi_kontrol:
    		print("%s" % ogrenci_adi)
	#print (ogrenci_adi)
	harc_kontrol=("")
	dif_kontrol=("")
	mat_kontrol=("")
	if (durum[1]==1):
		harc_kontrol=("Ödenmiş")
	else:
		harc_kontrol=("Ödenmemiş")
	if (durum[2]==1):
		dif_kontrol=("Derse kayıtlı")
	else:
		dif_kontrol=("Derse kayıtlı değil")
	if (durum[3]==1):
		mat_kontrol=("Derse kayıtlı")
	else:
		mat_kontrol=("Derse kayıtlı değil")
	return render_template('mat201_canli.html' ,last_row=last_row[0], durum=durum, harc_kontrol=harc_kontrol, dif_kontrol=dif_kontrol, son_giris=son_giris[0], ogrenci_adi=ogrenci_adi)
@app.route('/mat102_canli')
def mat102_canli():
	db = sql.connect("ogrenciler.sqlite")
	cs= db.cursor()
	last_row = cs.execute('SELECT ogrenci_no FROM girisler ORDER by id DESC LIMIT 1').fetchone()
	son_giris = cs.execute('SELECT zaman FROM girisler ORDER by id DESC LIMIT 1').fetchone()
	#print (son_giris[0])
	#print (last_row[0])
	satirkontrol=last_row[0]
	#print (satirkontrol)
	durum = cs.execute('select * from kayitlar where ogrenci_no=?',(satirkontrol,)).fetchone()
	#print (durum)
	ogrenci_adi_kontrol = cs.execute('select ogrenci_adi from kayitlar where ogrenci_no=?',(satirkontrol,)).fetchone()
	for ogrenci_adi in ogrenci_adi_kontrol:
    		print("%s" % ogrenci_adi)
	#print (ogrenci_adi)
	harc_kontrol=("")
	dif_kontrol=("")
	mat_kontrol=("")
	if (durum[1]==1):
		harc_kontrol=("Ödenmiş")
	else:
		harc_kontrol=("Ödenmemiş")
	if (durum[2]==1):
		dif_kontrol=("Derse kayıtlı")
	else:
		dif_kontrol=("Derse kayıtlı değil")
	if (durum[3]==1):
		mat_kontrol=("Derse kayıtlı")
	else:
		mat_kontrol=("Derse kayıtlı değil")
	return render_template('mat102_canli.html' ,last_row=last_row[0], durum=durum, harc_kontrol=harc_kontrol, mat_kontrol=mat_kontrol, son_giris=son_giris[0], ogrenci_adi=ogrenci_adi)

def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/kayit')
def upload_files():
   return render_template('kayit.html')

	
@app.route('/basarili_kayit', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join('ogrenciler',f.filename))
		harc=request.form['harc']
		dif=request.form['dif']
		mat=request.form['mat']
		adi=request.form['adi']
		print (harc,dif,mat)
		db = sql.connect("ogrenciler.sqlite")
		cs= db.cursor()
		cs.execute("insert into kayitlar values (?, ?, ?, ?, ?, ?)",(f.filename[0:8],harc,dif,mat,"",adi))
		db.commit()	
		return render_template('basarili_kayit.html')


@app.route('/kayit_silme')
def kayit_silici():
   return render_template('kayit_silme.html')

@app.route('/basarili_silme', methods = ['GET', 'POST'])
def kayit_silme():
	if request.method == 'POST':
		silinecek=request.form['silinecek']
		print (silinecek)
		dosya_sil=silinecek+'.jpg'
		dosya_konum="ogrenciler"
		yol=os.path.join(dosya_konum,dosya_sil)
		os.remove(yol)
		print (dosya_sil)
		db = sql.connect("ogrenciler.sqlite")
		cs= db.cursor()
		cs.execute('DELETE FROM kayitlar WHERE ogrenci_no=?',(silinecek,))
		db.commit()
		return render_template('basarili_silme.html')





@app.route('/kayit_duzenle')
def kayit_duzenleyici():
	return render_template('kayit_duzenle.html')

@app.route('/kayit_duzenle2', methods = ['GET', 'POST'])
def kayit_duzenleyici2():
	if request.method == 'POST':
		db = sql.connect("ogrenciler.sqlite")
		cs= db.cursor()
		duzen_no=request.form['duzen_no']
		print (duzen_no)
		print (duzen_no[1])
		kayit_duzen = cs.execute('SELECT * FROM kayitlar WHERE ogrenci_no=?',(duzen_no,)).fetchall()
		print (kayit_duzen[0])
		return render_template('kayit_duzenle2.html', duzen_le=kayit_duzen[0],)		

@app.route('/basarili_duzenle', methods = ['GET', 'POST'])
def kayit_basarili():
	if request.method == 'POST':
		db = sql.connect("ogrenciler.sqlite")
		cs= db.cursor()
		duzen_no=request.form['duzen_no']
		harc=request.form['harc']
		dif=request.form['dif']
		mat=request.form['mat']
		adi=request.form['adi']
		print ("öğrenci adı::",adi)
		print ("harc::",harc)
		print ("dif::",dif)
		print ("mat::",mat)
		print ("asdasd",duzen_no)
		duzen_no_final=duzen_no[1:9]
		print (duzen_no_final)
		print (duzen_no_final)
		print (duzen_no_final)
		kayit_duzen = cs.execute('SELECT * FROM kayitlar WHERE ogrenci_no=?',(duzen_no_final,)).fetchone()
		cs.execute('UPDATE kayitlar SET harc=?, dif=?, mat=?, ogrenci_adi=? WHERE ogrenci_no=?',(harc,dif,mat,adi,duzen_no_final))
		db.commit()
		return render_template('basarili_duzenle.html')	

@app.route('/video')

def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
app.run(debug=False)
