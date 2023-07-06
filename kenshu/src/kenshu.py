import docx as docx
import datetime
import sys
import os
import argparse



IMP=[]
IMP.append(("申請年月日",(0,3,0,1)))
IMP.append(("職氏名",(0,3,0,6)))
IMP.append(("研修内容",(0,4,3,0)))
IMP.append(("研修先",(0,5,3,0)))
IMP.append(("研修期間",(0,6,3,0)))

IMP.append(("渡航費",(0,19,0,2)))
IMP.append(("滞在費",(0,19,0,4)))
IMP.append(("国内連絡先",(0,19,0,6)))




def make_docx(basedocx,outdocx,formdata):
    if basedocx==outdocx:
        return
    doc = docx.Document(basedocx)
    for (key,(t,i,j,k)) in IMP:
        if key in formdata:
            doc.tables[t].cell(i,j).paragraphs[k].text=formdata[key]
            if key == "職氏名":
                doc.tables[t].cell(i,j).paragraphs[k].alignment=docx.enum.text.WD_ALIGN_PARAGRAPH.RIGHT 

    if "日程" in formdata:
        for l,ni in enumerate(formdata["日程"]):
            t=0
            i=8+l
            k=0
            if i > 13:
                print("Warn: Some Lines are not added.")
                continue
            for (key,j) in [("年月日",1),("出発地",4),("到着地",6),("宿泊及び滞在地",12),("宿泊数",14)]:
                if key in ni:
                    doc.tables[t].cell(i,j).paragraphs[k].text=ni[key]

        
    doc.save(outdocx)
    pass


def get_wareki_str(yyyy,mm,dd):
    return "令和{0}年{1}月{2}日".format(yyyy-2018,mm,dd)

def get_wareki_short_str(yyyy,mm,dd):
    return "R{0}.{1}.{2}".format(yyyy-2018,mm,dd)

def read_formdata_from_file(file):
    with open(file) as f:
        data={"":"","日程":[]}
        currenttag=""
        keys=["申請年月日","職","氏名","研修内容","研修先","渡航費", "滞在費","国内連絡先","mailto_name","mailto_address","filenameprefix"]
        tabelKeys=["出発地","到着地","宿泊及び滞在地","宿泊数"]
        
        for l in f:
            li=l.strip()
            if li.startswith("#"):
                continue
            if li.startswith("%"):
                continue
            if not li.startswith(":"):
                if currenttag=="日程":
                    data[currenttag][-1][subcurrenttag]=data[currenttag][-1][subcurrenttag]+li
                else:
                    data[currenttag]=data[currenttag]+li
            for k in keys:
                if li.startswith(":"+k+":"):
                    currenttag=k
                    data[currenttag]=li[len(k)+2:]
            if li.startswith(":年月日:"):
                currenttag="日程"
                data[currenttag].append({})
                subcurrenttag="年月日"
                data[currenttag][-1][subcurrenttag]=li[5:]
            for k in tabelKeys:
                if li.startswith(":"+k+":"):
                    currenttag="日程"
                    subcurrenttag=k
                    data[currenttag][-1][subcurrenttag]=li[len(k)+2:]

        formdata={}
        if "氏名" in data:
            formdata["氏名"]=data["氏名"]
            if "職" in data:
                formdata["職氏名"]="職・氏名  {0}・{1}".format(data["職"],data["氏名"])
        if "申請年月日" in data:
            d=[ int(di) for di in data["申請年月日"].split("/")]
            formdata["申請年月日"]=get_wareki_str(d[0],d[1],d[2])
            pass
        else:
            dt_now = datetime.datetime.now()
            formdata["申請年月日"]=get_wareki_str(dt_now.year,dt_now.month,dt_now.day)

        if data["日程"] != []:
            date=None
            firstdate=None
            formdata["日程"]=[]
            for i,ni in enumerate(data["日程"]):
                nni={}
                for k in ni.keys():
                    nni[k]=ni[k]
                if ni["年月日"] != "":
                    d=[ int(di) for di in ni["年月日"].split("/")]
                    nni["年月日"]=get_wareki_short_str(d[0],d[1],d[2])
                    dt=datetime.datetime(year=d[0], month=d[1], day=d[2])
                    nni["datetime"]=dt
                    if date==None:
                        date=dt
                        firstdate=dt
                    elif date != dt:
                        formdata["日程"][-1]["宿泊数"]="{0}".format((dt-date).days)
                        date=dt
                        
                formdata["日程"].append(nni)
            d0=get_wareki_str(firstdate.year,firstdate.month,firstdate.day)
            d1=get_wareki_str(date.year,date.month,date.day)
            d2=1+(date-firstdate).days
            formdata["研修期間"]="自 {0} 〜 至 {1} ({2}日間)".format(d0,d1,d2)
            formdata["day0"]=d0
            if firstdate.year==date.year:
                if firstdate.month==date.month:
                    if firstdate.day==date.day:
                        lastdate=""
                    else:
                        lastdate="-{2:02d}".format(date.year,date.month,date.day)
                        formdata["day1"]="{2:2d}日".format(date.year,date.month,date.day)
                else:
                    lastdate="-{1:02d}/{2:02d}".format(date.year,date.month,date.day)
                    formdata["day1"]="{1:2d}月{2:2d}日".format(date.year,date.month,date.day)
            else:
                lastdate="-{0:4d}/{1:02d}/{2:02d}".format(date.year,date.month,date.day)
                formdata["day1"]="{0:4d}年{1:2d}月{2:2d}日".format(date.year,date.month,date.day)
                    
            formdata["YYYY/MM/DD-"]="{0:4d}/{1:02d}/{2:02d}".format(firstdate.year,firstdate.month,firstdate.day)+lastdate
            formdata["YYYYMMDD"]="{0:4d}{1:02d}{2:02d}".format(firstdate.year,firstdate.month,firstdate.day)

        keys_justcopy=["研修内容","研修先","mailto_name","mailto_address","filenameprefix"]
        for k in keys_justcopy:
            if k in data:
                formdata[k]=data[k].replace("\\\\","\n")
        keys_justcopy_withkey=["渡航費", "滞在費","国内連絡先"]
        for k in keys_justcopy_withkey:
            if k in data:
                formdata[k]=k+": "+data[k].replace("\\\\","\n")
        return formdata

    return None


def mailtxt(formdata):
    r=""
    if "mailto_address" in formdata:
        r="To: "+formdata["mailto_address"]+"\n"
    r=r+"Subject: 研修"
    if "YYYY/MM/DD-" in formdata:
        r=r+" ("+formdata["YYYY/MM/DD-"]+")"
    r=r+"\n\n"
    if "mailto_name" in formdata:
        r=r+formdata["mailto_name"]+",\n\n"
    if "研修内容" in formdata:
        r=r+"以下の用務のため, "
    if "day0" in formdata:
        if "day1" in formdata:
            r=r+"\n"
            r=r+" "+formdata["day0"]+"から"+formdata["day1"]+"\n"
            r=r+"の日程で, "
        else:
            r=r+"\n"
            r=r+" "+formdata["day0"]+"\n"
            r=r+"に, "
    if "研修先" in formdata:
        r=r+"\n"
        r=r+" "+formdata["研修先"]+"\n"
        r=r+"へ, "
    if "研修内容" in formdata:
        r=r+"研修というかたちで行こうと考えています:\n"
        r=r+" "+formdata["研修内容"]
        r=r+"\n\n"
    else:
        r=r+"研修というかたちで行こうと考えています.\n"
    r=r+"ファイルを添付いたしますので, お手続きをお願いいたします.\n\n" 
    if "氏名" in formdata:
        r=r+"   "+formdata["氏名"]+"\n" 
    
    return r

def test():
    parser = argparse.ArgumentParser(description='研修用書類生成') 
    parser.add_argument('inputfile', help='研修の内容に関する入力ファイル')
    parser.add_argument('-od', '--output-docx', help='出力するdocxのファイル名.  デフォルトは出発日を使い, filenameprefix-YYYYMMDD.docx')
    parser.add_argument('-om', '--output-mail', help='出力するmailのファイル名. デフォルトは出発日を使い, filenameprefix-YYYYMMDD.txt')
    parser.add_argument('-O', '--output-base', help='出力ファイルを, OUTPUT_BASE.docx と OUTPUT_BASE.txt に指定.')
    parser.add_argument('-b', '--basefile', help='元となるdocx. デフォルトは, minimum.docx')   
    args = parser.parse_args()

    inputfile=args.inputfile
    fd=read_formdata_from_file(inputfile)

    if args.basefile:
        basedocx = args.basefile
    else:
        basedocx = os.path.join(os.path.dirname(__file__),"./minimum.docx")
        
    if args.output_docx:
        outputdocx=args.output_docx
    elif args.output_base:
            outputdocx=args.output_base+".docx"
    elif "YYYYMMDD" in fd:
        if "filenameprefix" in fd:
            outputdocx=fd["filenameprefix"]+"-"+fd["YYYYMMDD"]+".docx"
        else:
            outputdocx=fd["YYYYMMDD"]+".docx"
    else:
        outputdocx="test.docx"

    if basedocx==outputdocx:
        return

    make_docx(basedocx,outputdocx,fd)
        
    if args.output_mail:
        outputmail=args.output_mail
    elif args.output_base:
            outputmail=args.output_base+".txt"
    elif "YYYYMMDD" in fd:
        if "filenameprefix" in fd:
            outputmail=fd["filenameprefix"]+"-"+fd["YYYYMMDD"]+".txt"
        else:
            outputmail=fd["YYYYMMDD"]+".txt"
    else:
        outputmail="test.txt"

    if inputfile == outputmail:
        return            
    with open(outputmail,"w") as f:
        f.write(mailtxt(fd))





if __name__ == "__main__":
    test()


