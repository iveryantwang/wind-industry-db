# -*- coding: utf-8 -*-
"""首页 3D 地球仪：把 02-客户与项目 的每个项目标成地球上的一个点。
纯 Canvas 实现，海岸线数据来自同目录 globe_land.json（Natural Earth 110m，公共领域），
不依赖任何 CDN。项目点按「国别」落在国家中心附近（同国多项目按螺旋散开），不是精确坐标。"""
import os, io, json, math

# 国别 -> (纬度, 经度, 散开系数)
COUNTRY_XY = {
    "中国": (35.0, 105.0, 5), "印度": (22.0, 79.0, 4), "越南": (15.5, 108.0, 1.3),
    "老挝": (19.0, 102.5, 1.2), "柬埔寨": (12.7, 105.0, 1.0), "菲律宾": (14.0, 121.5, 1.5),
    "泰国": (15.0, 101.0, 1.5), "日本": (36.0, 138.5, 1.8), "韩国": (36.3, 127.8, 1.2),
    "台湾": (23.7, 121.0, 0.9), "哈萨克斯坦": (48.0, 67.0, 5), "乌兹别克斯坦": (41.5, 64.0, 2),
    "土耳其": (39.0, 35.0, 2.5), "埃及": (26.5, 30.0, 2.5), "摩洛哥": (31.8, -7.0, 1.5),
    "南非": (-29.0, 24.0, 3), "赞比亚": (-14.5, 27.5, 1.5), "阿曼": (21.0, 56.0, 1.5),
    "英国": (54.0, -2.5, 1.7), "爱尔兰": (53.2, -8.0, 0.8), "德国": (51.0, 10.2, 1.5),
    "法国": (46.6, 2.5, 1.8), "意大利": (42.8, 12.5, 2.0), "荷兰": (52.2, 5.5, 0.8),
    "比利时": (50.6, 4.6, 0.5), "丹麦": (56.0, 9.5, 0.9), "瑞典": (62.0, 15.0, 2.5),
    "挪威": (61.0, 9.0, 2.2), "波兰": (52.0, 19.0, 1.5), "罗马尼亚": (45.8, 25.0, 1.5),
    "塞尔维亚": (44.0, 20.8, 0.8), "北马其顿": (41.6, 21.7, 0.4), "拉脱维亚": (56.9, 24.6, 0.6),
    "乌克兰": (49.0, 32.0, 2), "摩尔多瓦": (47.2, 28.5, 0.5), "欧洲（多国）": (50.0, 10.0, 3),
    "美国": (39.0, -98.0, 5), "加拿大": (56.0, -100.0, 5), "巴西": (-10.0, -52.0, 4),
    "智利": (-33.5, -70.7, 2), "澳大利亚": (-27.0, 134.0, 5), "新西兰": (-41.5, 173.0, 1.5),
    "印尼": (-2.0, 118.0, 3), "沙特": (24.0, 45.0, 3),
}
_HERE = os.path.dirname(os.path.abspath(__file__))


def build_globe_points(notes, slugify, flat, num_or_none):
    seen = {}
    pts = []
    for n in sorted((x for x in notes if x.get("type") == "project"),
                    key=lambda x: x["__basename__"]):
        c = flat(n.get("country"))
        if c not in COUNTRY_XY:
            continue
        lat, lon, spread = COUNTRY_XY[c]
        k = seen.get(c, 0); seen[c] = k + 1
        if k:
            r = 0.75 * spread * math.sqrt(k); a = k * 2.399963
            lat += r * math.sin(a); lon += r * math.cos(a) / max(0.35, math.cos(math.radians(lat)))
        pts.append({
            "n": flat(n.get("project")) or n["__basename__"], "c": c,
            "la": round(lat, 2), "lo": round(lon, 2),
            "mw": num_or_none(n.get("capacity_mw")) or 0,
            "o": flat(n.get("opportunity")), "oem": flat(n.get("oem")),
            "u": "02-%s/%s.html" % ("客户与项目", slugify(n["__basename__"])),
        })
    return pts


def load_land():
    with io.open(os.path.join(_HERE, "globe_land.json"), encoding="utf-8") as f:
        return f.read()


GLOBE_HTML = """<section class="globebox" id="globebox">
  <div class="globehead"><b>🌍 全球项目分布</b>
    <span class="gsub" id="gcount"></span>
    <span class="glegend"><i style="background:#e5484d"></i>高机会 <i style="background:#f5a524"></i>中 <i style="background:#4c8dd6"></i>低 <i style="background:#8b95a5"></i>已失单/其他</span>
    <span class="gbtns"><button type="button" id="gspin">⏸ 暂停旋转</button><button type="button" id="gzin">＋</button><button type="button" id="gzout">－</button><button type="button" id="greset">复位</button></span>
  </div>
  <div class="gstage"><canvas id="globe" aria-label="全球风电项目分布地球仪"></canvas><div class="gtip" id="gtip"></div></div>
  <div class="gfoot">拖动旋转 · 滚轮/按钮缩放 · 点圆点进项目详情 · 圆点大小≈装机容量 · 位置为国别级示意，非精确坐标</div>
</section>"""

GLOBE_CSS = """
.globebox{background:var(--panel);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);margin-bottom:18px;overflow:hidden}
.globehead{display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:10px 14px;border-bottom:1px solid var(--line2);font-size:13px}
.gsub{color:var(--ink3);font-size:12.5px}
.glegend{color:var(--ink2);font-size:12.5px;margin-left:auto}
.glegend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin:0 3px 0 10px;vertical-align:baseline}
.gbtns button{border:1px solid var(--line);background:var(--bg);color:var(--ink2);border-radius:6px;padding:3px 9px;font-size:12px;cursor:pointer;margin-left:4px}
.gbtns button:hover{border-color:var(--brand2);color:var(--brand2)}
.gstage{position:relative;height:min(62vh,520px);min-height:300px;background:radial-gradient(ellipse at 50% 40%,var(--line2),var(--panel))}
#globe{width:100%;height:100%;display:block;cursor:grab;touch-action:none}
#globe:active{cursor:grabbing}
.gtip{position:absolute;pointer-events:none;display:none;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-size:12.5px;box-shadow:var(--shadow);max-width:260px;z-index:3}
.gfoot{padding:6px 14px 9px;color:var(--ink3);font-size:12px}
"""

GLOBE_JS = r"""
(function(){
const PTS=__GPTS__, LAND=__GLAND__;
const cv=document.getElementById("globe"); if(!cv) return;
const ctx=cv.getContext("2d"), tip=document.getElementById("gtip");
const D=Math.PI/180, COL={"高":"#e5484d","中":"#f5a524","低":"#4c8dd6"};
let lon0=100, lat0=22, zoom=1, spin=true, W=0,H=0,R=0,dpr=1, vx=0, drag=null, hover=null, idle=0;
document.getElementById("gcount").textContent=PTS.length+" 个项目 · "+new Set(PTS.map(p=>p.c)).size+" 个国家/地区";
function css(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim();}
function size(){const r=cv.getBoundingClientRect();dpr=window.devicePixelRatio||1;W=r.width;H=r.height;
  cv.width=W*dpr;cv.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);R=Math.min(W,H)*0.46*zoom;}
function proj(la,lo){const p=la*D,l=(lo-lon0)*D,p0=lat0*D;
  const cc=Math.sin(p0)*Math.sin(p)+Math.cos(p0)*Math.cos(p)*Math.cos(l);
  return {x:W/2+R*Math.cos(p)*Math.sin(l), y:H/2-R*(Math.cos(p0)*Math.sin(p)-Math.sin(p0)*Math.cos(p)*Math.cos(l)), v:cc};}
function ring(r,fill){ctx.beginPath();let first=true;
  for(const c of r){const q=proj(c[1],c[0]);let x=q.x,y=q.y;
    if(q.v<0){const dx=x-W/2,dy=y-H/2,d=Math.hypot(dx,dy)||1;x=W/2+dx/d*R;y=H/2+dy/d*R;}
    if(first){ctx.moveTo(x,y);first=false}else ctx.lineTo(x,y);}
  ctx.closePath();if(fill)ctx.fill();}
function grat(){ctx.beginPath();
  for(let lo=-180;lo<180;lo+=30){let f=true;for(let la=-90;la<=90;la+=5){const q=proj(la,lo);
    if(q.v<0){f=true;continue}if(f){ctx.moveTo(q.x,q.y);f=false}else ctx.lineTo(q.x,q.y);}}
  for(let la=-60;la<=60;la+=30){let f=true;for(let lo=-180;lo<=180;lo+=5){const q=proj(la,lo);
    if(q.v<0){f=true;continue}if(f){ctx.moveTo(q.x,q.y);f=false}else ctx.lineTo(q.x,q.y);}}
  ctx.stroke();}
function draw(){
  ctx.clearRect(0,0,W,H);
  const g=ctx.createRadialGradient(W/2-R*.35,H/2-R*.4,R*.1,W/2,H/2,R);
  g.addColorStop(0,css("--coolbg")||"#eaf1f9");g.addColorStop(1,css("--line")||"#dfe5ee");
  ctx.fillStyle=g;ctx.beginPath();ctx.arc(W/2,H/2,R,0,7);ctx.fill();
  ctx.save();ctx.beginPath();ctx.arc(W/2,H/2,R,0,7);ctx.clip();
  ctx.strokeStyle=css("--line")||"#ccd";ctx.globalAlpha=.7;ctx.lineWidth=.6;grat();ctx.globalAlpha=1;
  ctx.fillStyle=css("--ink3")||"#8a97a9";ctx.globalAlpha=.55;for(const r of LAND)ring(r,true);ctx.globalAlpha=1;
  ctx.restore();
  ctx.strokeStyle=css("--brand2")||"#3d6ea5";ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(W/2,H/2,R,0,7);ctx.stroke();
  const vis=[];
  for(const p of PTS){const q=proj(p.la,p.lo);if(q.v>0.04){q.p=p;q.r=(3.2+Math.min(5,Math.sqrt(p.mw||0)/9))*Math.min(1.5,.75+zoom*.25);vis.push(q);}}
  vis.sort((a,b)=>a.v-b.v);
  for(const q of vis){const c=COL[q.p.o]||"#8b95a5",h=hover===q.p;
    ctx.globalAlpha=Math.min(1,q.v*2.5);
    ctx.fillStyle=c;ctx.globalAlpha*=.25;ctx.beginPath();ctx.arc(q.x,q.y,q.r+(h?7:3.5),0,7);ctx.fill();
    ctx.globalAlpha=Math.min(1,q.v*2.5);ctx.fillStyle=c;ctx.beginPath();ctx.arc(q.x,q.y,q.r,0,7);ctx.fill();
    ctx.strokeStyle="#fff";ctx.lineWidth=1;ctx.stroke();q.p._q=q;}
  ctx.globalAlpha=1;
}
function tick(){
  if(!drag){ if(Math.abs(vx)>.02){lon0-=vx;vx*=.94;} else if(spin&&!hover&&++idle>60)lon0+=.12; }
  draw();requestAnimationFrame(tick);}
function pick(x,y){let b=null,bd=1e9;for(const p of PTS){const q=p._q;if(!q||proj(p.la,p.lo).v<=.04)continue;
  const d=Math.hypot(q.x-x,q.y-y);if(d<q.r+6&&d<bd){bd=d;b=p}}return b;}
function pos(e){const r=cv.getBoundingClientRect();return [e.clientX-r.left,e.clientY-r.top];}
cv.addEventListener("pointerdown",e=>{cv.setPointerCapture(e.pointerId);const [x,y]=pos(e);drag={x,y,moved:0};vx=0;idle=0;});
cv.addEventListener("pointermove",e=>{const [x,y]=pos(e);
  if(drag){const dx=x-drag.x,dy=y-drag.y;drag.moved+=Math.abs(dx)+Math.abs(dy);
    const k=.4/zoom;lon0-=dx*k;lat0=Math.max(-80,Math.min(80,lat0+dy*k));vx=-dx*k*0+(-dx*k);drag.x=x;drag.y=y;idle=0;tip.style.display="none";return;}
  hover=pick(x,y);cv.style.cursor=hover?"pointer":"grab";
  if(hover){tip.style.display="block";tip.style.left=Math.min(x+14,W-200)+"px";tip.style.top=(y+14)+"px";
    tip.innerHTML="<b>"+hover.n.replace(/</g,"&lt;")+"</b><br>"+hover.c+" · "+(hover.mw?hover.mw+" MW":"容量未披露")+"<br>机会："+(hover.o||"—")+" · 整机："+(hover.oem||"未定");}
  else tip.style.display="none";});
cv.addEventListener("pointerup",e=>{if(drag&&drag.moved<5){const [x,y]=pos(e);const p=pick(x,y);if(p)location.href=p.u;}drag=null;});
cv.addEventListener("pointerleave",()=>{hover=null;tip.style.display="none";});
cv.addEventListener("wheel",e=>{e.preventDefault();setZ(zoom*(e.deltaY<0?1.12:.89));},{passive:false});
function setZ(z){zoom=Math.max(.7,Math.min(4,z));R=Math.min(W,H)*0.46*zoom;}
document.getElementById("gzin").onclick=()=>setZ(zoom*1.25);
document.getElementById("gzout").onclick=()=>setZ(zoom/1.25);
document.getElementById("greset").onclick=()=>{lon0=100;lat0=22;zoom=1;vx=0;size();};
const sb=document.getElementById("gspin");sb.onclick=()=>{spin=!spin;sb.textContent=spin?"⏸ 暂停旋转":"▶ 自动旋转";};
window.addEventListener("resize",size);size();requestAnimationFrame(tick);
})();
"""


def globe_js(points):
    return (GLOBE_JS.replace("__GPTS__", json.dumps(points, ensure_ascii=False, separators=(",", ":")))
                    .replace("__GLAND__", load_land()))
