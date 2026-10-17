"""Troca o ícone embutido num .exe do Windows (recurso RT_ICON/RT_GROUP_ICON) sem ferramentas externas.
Cada imagem nova é gravada no lugar da antiga, que precisa ter tamanho igual ou maior."""
import struct, sys, io
from PIL import Image

def load(path):
    data=bytearray(open(path,'rb').read())
    pe=struct.unpack_from('<I',data,0x3c)[0]; nsec=struct.unpack_from('<H',data,pe+6)[0]; optsz=struct.unpack_from('<H',data,pe+20)[0]
    opt=pe+24; magic=struct.unpack_from('<H',data,opt)[0]; ddoff=opt+(112 if magic==0x20b else 96)
    rsrc_rva=struct.unpack_from('<I',data,ddoff+2*8)[0]
    secs=[struct.unpack_from('<8sIIII',data,opt+optsz+i*40) for i in range(nsec)]
    def r2o(rva):
        for n,vs,va,rs,ra in secs:
            if va<=rva<va+max(vs,rs): return rva-va+ra
        raise ValueError(hex(rva))
    base=r2o(rsrc_rva); entries={}
    def walk(off,path):
        _,_,_,_,nn,ni=struct.unpack_from('<IIHHHH',data,base+off)
        for k in range(nn+ni):
            idv,ptr=struct.unpack_from('<II',data,base+off+16+k*8)
            if ptr&0x80000000: walk(ptr&0x7fffffff,path+[idv])
            else:
                rva,size,_,_=struct.unpack_from('<IIII',data,base+ptr); entries[tuple(path+[idv])]=(base+ptr,r2o(rva),size)
    walk(0,[])
    return data,entries

def group_info(data,entries):
    key=[k for k in entries if k[0]==14][0]; de,off,size=entries[key]
    _,_,count=struct.unpack_from('<HHH',data,off); items=[]
    for i in range(count):
        w,h,cc,res,planes,bpp,nbytes,nid=struct.unpack_from('<BBBBHHIH',data,off+6+i*14)
        items.append(dict(w=w or 256,h=h or 256,bpp=bpp,bytes=nbytes,id=nid,rec=off+6+i*14))
    return items

def bmp_icon(img,size,bpp):
    im=img.convert('RGBA').resize((size,size),Image.LANCZOS)
    assert bpp==32
    px=im.load(); rows=[]
    for y in range(size-1,-1,-1):
        rows.append(b''.join(struct.pack('<BBBB',*(lambda p:(p[2],p[1],p[0],p[3]))(px[x,y])) for x in range(size)))
    xor=b''.join(rows); mask_row=((size+31)//32)*4; andm=b'\0'*mask_row*size
    hdr=struct.pack('<IiiHHIIiiII',40,size,size*2,1,32,0,len(xor)+len(andm),0,0,0,0)
    return hdr+xor+andm

def png_icon(img,size,limit):
    im=img.convert('RGBA').resize((size,size),Image.LANCZOS)
    for colors in (None,256,192,128,96,64,48,32):
        buf=io.BytesIO()
        if colors is None: im.save(buf,'PNG',optimize=True)
        else: im.quantize(colors=colors,method=Image.FASTOCTREE).save(buf,'PNG',optimize=True)
        if len(buf.getvalue())<=limit: return buf.getvalue(),colors
    raise SystemExit('PNG não coube no espaço do ícone original')

def main(exe,small_src,big_src,out):
    data,entries=load(exe); items=group_info(data,entries)
    small=Image.open(small_src); big=Image.open(big_src)
    for it in items:
        key=[k for k in entries if k[0]==3 and k[1]==it['id']][0]; de,off,size=entries[key]
        src=small if it['w']<=48 else big
        old=bytes(data[off:off+4])
        if old==b'\x89PNG': new,info=png_icon(src,it['w'],size)
        else:
            bpp=struct.unpack_from('<H',data,off+14)[0]
            new=bmp_icon(src,it['w'],bpp); info=f'bmp{bpp}'
            if len(new)>size: raise SystemExit(f'ícone {it["w"]} maior que o espaço')
        data[off:off+len(new)]=new; data[off+len(new):off+size]=b'\0'*(size-len(new))
        struct.pack_into('<I',data,de+4,len(new))          # tamanho no diretório de recursos
        struct.pack_into('<I',data,it['rec']+8,len(new))    # tamanho no grupo de ícones
        print(f"{it['w']}x{it['h']}: {info}, {len(new)} de {size} bytes")
    open(out,'wb').write(data)

if __name__=='__main__': main(*sys.argv[1:5])
