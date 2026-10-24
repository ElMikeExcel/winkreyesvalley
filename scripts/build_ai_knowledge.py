"""Regenerate ai-knowledge.json from index.html + questions.html.
Reconstructed Oct 23, 2026 to reproduce the existing corpus format (id/title/text chunks)."""
import re, sys, json
from html.parser import HTMLParser
ENDBLOCK = set('p h1 h2 h3 h4 h6 li tr summary title ul ol table section article header footer main details figure figcaption blockquote dd dt pre'.split())
VOID=set('area base br col embed hr img input link meta source track wbr'.split())
MAX=6500
class X(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.lines=[]; s.cur=[]; s.skip=0; s.stack=[]; s.anchor=None; s.anchor_saved=None
        s.events=[]  # (line_index, kind, value)
    def flush(s, tag=None):
        t=' '.join(x for x in s.cur if x); t=re.sub(r'\s+',' ',t).strip()
        if t: s.lines.append(dict(text=t, tag=tag, anchor=s.cur_anchor, ingide=s.cur_inguide))
        s.cur=[]
    def in_id(s,i):
        return any(a.get('id')==i for t,a in s.stack)
    def in_guide(s):
        return any(t=='section' and a.get('id')=='guide' for t,a in s.stack)
    def handle_starttag(s,tag,a):
        a=dict(a)
        if tag in('script','style'): s.skip+=1; return
        if tag=='section' and 'qa-stub-sec' in (a.get('class') or ''): s.skip+=1; s.stubskip=True; return
        if tag in VOID: return
        s.stack.append((tag,a))
        if tag in('section','header') and a.get('id'):
            s.newanchor(a['id'])
        if tag=='details' and 'st-track' in (a.get('class') or '').split() and s.in_id('st-panel-mcmmo'):
            s.ladder_open=True; s.anchor_saved=s.anchor; s.pending_ladder=True
    def newanchor(s,i):
        s.flush('anchor'); s.anchor=i; s.events.append(len(s.lines))
    def handle_endtag(s,tag):
        if tag in('script','style'): s.skip-=1; return
        if tag=='section' and getattr(s,'stubskip',False) and s.skip==1: s.skip=0; s.stubskip=False; return
        if tag in ENDBLOCK: s.flush(tag)
        for i in range(len(s.stack)-1,-1,-1):
            if s.stack[i][0]==tag:
                closed=s.stack[i]; del s.stack[i:]; break
        else: closed=None
        if closed and closed[0]=='details' and 'st-track' in (closed[1].get('class') or '').split() and getattr(s,'ladder_open',False):
            s.ladder_open=False; s.newanchor(s.anchor_saved)
    def handle_comment(s,d):
        if '>' in d: s.handle_data(d.split('>',1)[1]+'-->')
    def handle_data(s,d):
        if s.skip: return
        if getattr(s,'pending_ladder',False):
            # ladder anchor named from the first span (st-title)
            t=d.strip()
            if t:
                s.pending_ladder=False
                s.newanchor('ladder-'+re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-'))
        parts=d.split('\n')
        for i,p in enumerate(parts):
            if i>0: s.flush('nl')
            p=re.sub(r'\s+',' ',p).strip()
            if p:
                if not s.cur: s.cur_anchor=s.anchor; s.cur_inguide=s.in_guide()
                s.cur.append(p)
def lines_of(src):
    x=X(); x.feed(src); x.flush('eof'); return x.lines
def chunk(lines):
    out=[]; cur=None; counters={}
    def start(aid,title,first,split=False):
        nonlocal cur
        if cur: out.append(cur)
        if split:
            counters[aid]=counters.get(aid,0)+1; cid=f"{aid}-{counters[aid]}"
        else: cid=aid
        cur=dict(id=cid,title=title,lines=[first],aid=aid)
    prev_anchor=object()
    for l in lines:
        t=l['text']; a=l['anchor'] or 'top'
        heading = l['tag'] in ('h2','h3','h4','title','summary')
        if cur is not None and a==prev_anchor and cur['lines'][-1]==t:
            continue
        if cur is None or a!=prev_anchor:
            start(a, t[:90], t); cur['hd']=heading
        elif heading and l['ingide'] and l['tag'] in ('h3','h4'):
            if len(cur['lines'])==1 and cur.get('hd'):
                cur.update(title=t, lines=[t])
            else:
                start(a, t, t)
            cur['hd']=True
            prev_anchor=a; continue
        elif len('\n'.join(cur['lines']))+1+len(t)>MAX:
            start(a, t[:90], t, split=True)
        else:
            cur['lines'].append(t)
        prev_anchor=a
    out.append(cur)
    return [dict(id=c['id'],title=c['title'],text='\n'.join(c['lines'])) for c in out]
def build(index_src, q_src):
    L=lines_of(index_src)
    Q=lines_of(q_src)
    # questions.html: skip its <title> line (not in corpus)
    Q=[l for l in Q if l['tag']!='title']
    return chunk(L+Q)
if __name__=='__main__':
    root=sys.argv[1] if len(sys.argv)>1 else '.'
    d=build(open(root+'/index.html').read(), open(root+'/questions.html').read())
    out=sys.argv[2] if len(sys.argv)>2 else root+'/ai-knowledge.json'
    open(out,'w').write(json.dumps(d,ensure_ascii=False,indent=1))
    print(len(d),'chunks')
