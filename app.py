from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys
from datetime import datetime



app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html')
 
    
@app.route('/display', methods = ['GET', 'POST'])
def parse():  
    if request.method == 'POST':
        f = request.files['file']        
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        f = open(app.config['UPLOAD_FOLDER']+filename,'r')
        matter=f.read()
        mat=matter.upper();
        fomt="%I:%M:%p"
        totaltime=0;
        index=mat.find("TIME LOG:");
        if index!=-1:
            mat=mat[index+len("TIME LOG:"):]
            index=mat.find('-')
            while (index!=-1):
                if mat[index+1]==' ':
                    mat=mat[:index-1] + "#" + mat[index+2:];
                elif mat[index-1]==' ':
                    mat=mat[:index-2] + "#" + mat[index+1:]
                else:
                    mat=mat[:index-1] + "#" + mat[index+1:];
                index = mat.find("#",index-2,index+2);
                st = mat.rfind(" ",0,index);
                st = mat[st+1:index];
                et = mat.find("M",index,index+15);
                et = mat[index+1:et+1];
                st = st[:len(st)-2] + ":" + st[len(st)-2:]
                et = et[:len(et)-2] + ":" + et[len(et)-2:]
                try:
                    st = datetime.strptime(st,fomt)
                    et = datetime.strptime(et,fomt)
                    totaltime = totaltime+(et-st).seconds/60
                except:
                    index = mat.find('-')
                    continue;
                index = mat.find('-')
        
        output = "Total time spent by the author is"+str(int((totaltime)/60))+"hours"+str(int((totaltime)%60))+"mins"
        return render_template('index.html',result=output)
    return render_template('index.html')
                    

if __name__ == '__main__':
    app.run(debug = True)