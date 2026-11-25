
#!/usr/bin/env python3
"""Tuesday 24 November 2026 — THE WORLD ON ONE PAGE. 38 stories, 13 panels, drawn in PIL only; deterministic."""
import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024; BG=(250,246,235); INK=(18,18,18); RED=(178,34,34); NAVY=(24,48,84); TEAL=(18,90,90); GOLD=(176,132,32); GREY=(110,110,105); LGREEN=(214,232,196); LBLUE=(205,224,238)
def F(sz,bold=False,serif=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if serif else ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    try: return ImageFont.truetype(p,sz)
    except Exception: return ImageFont.load_default()
def wrap(t,font,mw,d):
    words=t.split(); lines=[]; cur=""
    for w in words:
        s=(cur+" "+w).strip()
        if d.textlength(s,font=font)<=mw: cur=s
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def txt(d,x,y,s,font,fill=INK,align="left"):
    if align=="center": x-=d.textlength(s,font=font)//2
    if align=="right": x-=d.textlength(s,font=font)
    d.text((x,y),s,font=font,fill=fill); return d.textlength(s,font=font)
def para(d,x,y,s,font,mw,lh=13,fill=INK):
    for ln in wrap(s,font,mw,d): d.text((x,y),ln,font=font,fill=fill); y+=lh
    return y
def chip(d,x,y,s,fill):
    f=F(8,True); w=d.textlength(s,font=f)+10; d.rounded_rectangle([x,y,x+w,y+14],3,fill=fill); d.text((x+5,y+2),s,font=f,fill=(255,255,255)); return x+w+4
def scene(d,x,y,w,h,kind):
    d.rectangle([x,y,x+w,y+h],fill=LBLUE,outline=NAVY)
    if kind=="tower":
        d.rectangle([x,y,x+w,y+h],fill=(38,52,80)); d.rectangle([x+w*0.42,y+18,x+w*0.58,y+h],fill=(70,90,130)); d.polygon([(x+w*0.42,y+18),(x+w*0.5,y+2),(x+w*0.58,y+18)],fill=(200,170,60)); d.rectangle([x+w*0.42,y+38,x+w*0.58,y+44],fill=(255,220,120)); d.rectangle([x+w*0.15,y+h-22,x+w*0.35,y+h],fill=(60,70,95)); d.rectangle([x+w*0.65,y+h-30,x+w*0.85,y+h],fill=(60,70,95))
        for i in range(5): d.ellipse([x+w*0.62+i*9,y+22+i*3,x+w*0.66+i*9,y+26+i*3],fill=(255,120,40))
        d.ellipse([x+w*0.18,y+14,x+w*0.30,y+26],fill=(255,200,80))
    elif kind=="gate":
        d.rectangle([x,y,x+w,y+h],fill=(150,40,40)); d.rectangle([x+w*0.08,y+30,x+w*0.92,y+h],fill=(210,180,140)); d.rectangle([x+w*0.38,y+52,x+w*0.62,y+h],fill=(60,30,30)); d.rectangle([x+w*0.12,y+22,x+w*0.88,y+34],fill=(176,132,32)); d.rectangle([x+w*0.20,y+40,x+w*0.30,y+48],fill=(24,48,84)); d.rectangle([x+w*0.70,y+40,x+w*0.80,y+48],fill=(24,48,84)); d.text((x+w*0.30,y+58),"SERIOUS VIOLATIONS",font=F(9,True),fill=(255,255,255))
    elif kind=="court":
        d.rectangle([x,y,x+w,y+h],fill=(40,60,90)); d.polygon([(x+w*0.15,y+34),(x+w*0.5,y+8),(x+w*0.85,y+34)],fill=(220,220,210)); d.rectangle([x+w*0.20,y+34,x+w*0.80,y+40],fill=(220,220,210))
        for i in range(5): d.rectangle([x+w*0.20+i*w*0.13,y+40,x+w*0.28+i*w*0.13,y+h-8],fill=(220,220,210))
        d.text((x+w*0.30,y+h-26),"10 / 12",font=F(16,True),fill=(255,255,255))
    elif kind=="drones":
        d.rectangle([x,y,x+w,y+h],fill=(20,28,52)); d.ellipse([x+w*0.70,y+8,x+w*0.95,y+33],fill=(255,220,130))
        for i in range(4): d.ellipse([x+w*0.08+i*w*0.18,y+18+i*6,x+w*0.16+i*w*0.18,y+26+i*6],fill=(255,150,60))
        d.rectangle([x+w*0.10,y+h-26,x+w*0.90,y+h],fill=(40,45,70))
    elif kind=="trophy":
        d.rectangle([x,y,x+w,y+h],fill=(18,90,60)); d.ellipse([x+w*0.38,y+6,x+w*0.62,y+30],fill=(255,215,0)); d.rectangle([x+w*0.47,y+30,x+w*0.53,y+36],fill=(255,215,0)); d.rectangle([x+w*0.36,y+36,x+w*0.64,y+42],fill=(200,170,60)); d.text((x+8,y+h-12),"SENEGAL 1-0",font=F(9,True),fill=(255,255,255))
    elif kind=="ship":
        d.rectangle([x,y,x+w,y+h],fill=(30,70,110)); d.rectangle([x+w*0.10,y+h-16,x+w*0.90,y+h-2],fill=(180,60,40)); d.rectangle([x+w*0.18,y+18,x+w*0.82,y+h-16],fill=(220,220,210)); d.rectangle([x+w*0.42,y+6,x+w*0.50,y+18],fill=(220,220,210)); d.ellipse([x+w*0.78,y+8,x+w*0.92,y+20],fill=(255,150,50))
    elif kind=="chart":
        d.rectangle([x,y,x+w,y+h],fill=(245,245,235)); d.line([(x+8,y+h-14),(x+w-8,y+12)],fill=(18,120,60),width=4); d.line([(x+8,y+h-14),(x+w-8,y+h-14)],fill=INK,width=2); d.text((x+10,y+6),"50,018",font=F(15,True),fill=(18,120,60)); d.text((x+w*0.55,y+h-24),"+8.99%",font=F(11,True),fill=RED)
    elif kind=="data":
        d.rectangle([x,y,x+w,y+h],fill=(120,20,20)); d.rectangle([x+w*0.10,y+14,x+w*0.42,y+h-14],fill=(30,30,30)); d.rectangle([x+w*0.54,y+14,x+w*0.90,y+h-14],fill=(30,30,30)); d.text((x+w*0.14,y+20),"CODE RED",font=F(12,True),fill=(255,80,80)); d.text((x+w*0.58,y+20),"24 HRS",font=F(11,True),fill=(255,220,100))
    elif kind=="heli":
        d.rectangle([x,y,x+w,y+h],fill=(200,210,225)); d.ellipse([x+w*0.15,y+20,x+w*0.55,y+h-6],fill=(60,70,80)); d.rectangle([x+w*0.55,y+28,x+w*0.88,y+36],fill=(60,70,80)); d.line([(x+w*0.10,y+18),(x+w*0.85,y+18)],fill=INK,width=3); d.polygon([(x+w*0.05,y+h-4),(x+w*0.35,y+h-14),(x+w*0.65,y+h-14),(x+w*0.95,y+h-4)],fill=(90,100,110))
    elif kind=="market":
        d.rectangle([x,y,x+w,y+h],fill=(240,200,120)); d.rectangle([x+w*0.10,y+20,x+w*0.90,y+h-14],fill=(200,60,50)); d.text((x+w*0.18,y+8),"SUPERMARKET",font=F(11,True),fill=(255,255,255)); d.text((x+w*0.30,y+h-20),"25 HELD",font=F(13,True),fill=(255,255,255))
    elif kind=="desert":
        d.rectangle([x,y,x+w,y+h],fill=(230,200,140)); d.polygon([(x,y+h),(x+w*0.4,y+30),(x+w*0.8,y+h)],fill=(200,160,90)); d.polygon([(x+w*0.3,y+h),(x+w*0.7,y+45),(x+w,y+h)],fill=(180,140,70)); d.text((x+10,y+10),"60 KM",font=F(13,True),fill=(120,60,20))
    elif kind=="strike":
        d.rectangle([x,y,x+w,y+h],fill=(80,40,30)); d.ellipse([x+w*0.60,y+6,x+w*0.92,y+26],fill=(255,140,40)); d.rectangle([x+w*0.10,y+h-14,x+w*0.90,y+h-2],fill=(40,40,40)); d.text((x+10,y+h-22),"25 KILLED",font=F(12,True),fill=(255,255,255))
    else:
        d.rectangle([x,y,x+w,y+h],fill=(15,20,45)); d.polygon([(x+w*0.45,y+6),(x+w*0.52,y+26),(x+w*0.58,y+h-4),(x+w*0.42,y+h-4),(x+w*0.48,y+26)],fill=(230,230,230)); d.ellipse([x+w*0.68,y+10,x+w*0.92,y+30],fill=(200,200,220)); d.text((x+8,y+h-18),"TIANGONG",font=F(10,True),fill=(255,255,255))
CONT=[[( -168,66),(-140,70),(-120,72),(-95,80),(-80,73),(-65,60),(-55,52),(-60,45),(-75,35),(-80,25),(-90,20),(-97,16),(-105,20),(-115,28),(-125,40),(-125,49),(-145,60),(-168,66)],[(-80,10),(-70,12),(-60,8),(-50,0),(-40,-5),(-35,-10),(-40,-20),(-48,-28),(-58,-35),(-65,-45),(-70,-55),(-75,-40),(-80,-20),(-80,0),(-80,10)],[(-10,36),(-10,43),(-2,48),(0,51),(5,53),(8,57),(10,59),(18,56),(21,55),(23,59),(30,60),(30,70),(20,70),(10,70),(5,60),(-5,58),(-10,50),(-10,36)],[(-17,15),(-10,30),(0,36),(10,37),(20,32),(32,31),(35,28),(43,12),(51,11),(48,0),(40,-10),(35,-20),(30,-30),(20,-35),(15,-30),(12,-18),(13,-5),(9,4),(-8,5),(-17,15)],[(30,36),(35,36),(43,41),(50,46),(60,55),(70,70),(90,75),(110,75),(130,72),(160,70),(178,65),(160,60),(142,55),(140,40),(130,33),(122,30),(110,20),(105,10),(100,8),(95,15),(90,22),(80,15),(75,8),(70,20),(60,25),(50,29),(40,30),(30,36)],[(113,-22),(114,-30),(115,-35),(125,-32),(135,-35),(140,-38),(150,-37),(153,-27),(146,-19),(142,-11),(135,-12),(130,-13),(122,-14),(113,-22)]]
PINS=[(1,24.7,46.7),(2,31.2,121.5),(3,40.7,-74.0),(4,47.8,35.2),(5,14.7,-17.4),(6,26.5,56.5),(7,40.7,-74.0),(8,47.7,-122.1),(9,39.8,30.5),(10,10.4,-75.5),(11,12.8,45.0),(12,13.0,44.9),(13,39.7,98.5)]
OFF={3:(0,0),7:(16,-14),11:(0,0),12:(18,12),1:(0,0),2:(0,0)}
HERO=[("1 RIYADH · MIDDLE EAST","tower","Houthi drone hits Riyadh's tallest tower again, 11 hurt","A Houthi drone hit the PIF tower, Riyadh's tallest, for the second time in a week; 11 were hurt, including 2 Saudis, 2 Indians, 3 Nepalis and 4 Egyptians.",(178,34,34),"CONFIRMED","Saudi officials"),("2 SHANGHAI · ASIA","gate","China probes Shanghai party chief Chen Jining","Chen Jining, 62, the Shanghai party chief, is probed for serious violations, the fourth Politburo member to fall in a party investigation this year.",(24,48,84),"OFFICIAL","CCDI"),("3 NEW YORK · US / TECH","court","Huawei guilty on 10 of 12 counts","A US federal jury found Huawei guilty on 10 of 12 counts, including trade-secret theft and bank fraud, and cleared it of racketeering; sentencing is in Sep 2027.",(18,90,60),"CONFIRMED","US court")]
CARDS=[("4 ZAPORIZHZHIA · EUROPE","drones","Russian attacks kill 9 across Ukraine in a day","Russia killed 9 people in Ukraine in a day and wounded 81, launching 96 drones of which 73 were shot down or jammed.",(178,34,34),"REPORTED","Ukraine officials"),("5 DAKAR · AFRICA / SPORT","trophy","CAS hands Senegal back the AFCON title","CAS handed Senegal the Africa Cup title back after Morocco forfeited 3-0, turning the final into a 1-0 win for Senegal.",(18,90,60),"OFFICIAL","CAS"),("6 HORMUZ · MIDDLE EAST","ship","IRGC attacks container ship in Hormuz","The IRGC attacked a container ship in Hormuz at 18:58 UTC, disabling its navigation and closing waters north of Khasab, Oman.",(178,34,34),"REPORTED","UKMTO"),("7 NEW YORK · MARKETS","chart","Dow closes above 50,000 for the first time","The Dow closed at 50,018, its first close above 50,000, while Taiwan's Taiex jumped a record 8.99% and the Nasdaq fell 1.5%.",(18,90,60),"CONFIRMED","Market close"),("8 REDMOND · TECH","data","Microsoft declares 'Code Red' after historic outage","Microsoft declared Code Red after a 24-hour outage, the worst in Exchange Online history, aiming for global recovery within 1 hour.",(178,34,34),"REPORTED","Reuters"),("9 ESKISEHIR · EUROPE","heli","Turkish military helicopter crash kills 5","A Turkish military AS-532 helicopter crashed in Eskisehir, killing 5 people on board at 19:52 UTC.",(178,34,34),"REPORTED","Turkish officials"),("10 CARTAGENA · AMERICAS","market","Supermarket hostages: 25 held in Cartagena","Armed men held 25 hostages in a Cartagena supermarket, freeing 5 elderly women, while airport landings were suspended for about 45 minutes.",(178,34,34),"REPORTED","Colombia officials"),("11 ADEN · MIDDLE EAST","desert","Houthis advance within 60 km of Aden","Houthi forces advanced to within 60 km of Aden in Yemen, the closest push toward the port city in the current fighting.",(178,34,34),"REPORTED","Wires"),("12 LAHJ · MIDDLE EAST","strike","Saudi strikes kill 25, wound 6 in Yemen","Saudi strikes on a bus and truck in Wadi Maabaq, Lahj, killed or left missing 25 people and wounded 6 others.",(178,34,34),"REPORTED","Yemen officials"),("13 JIUQUAN · SPACE","rocket","China names first foreign astronaut for Tiangong","China named the Shenzhou-24 crew as Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali of Pakistan, the first foreign astronaut for Tiangong.",(24,48,84),"OFFICIAL","CMSA")]
ALSO=[("14 Ankara: Haftar visits Turkey for the first time.","REPORTED"),("15 London: UK sanctions Houthis and 4 officials.","OFFICIAL"),("16 Villavicencio: Car bomb injures 23 people.","REPORTED"),("17 Gaza: Israel kills Hamas internal security chief.","REPORTED"),("18 Baghdad: Iraq orders federal control of Kurdish oilfields.","OFFICIAL"),("19 Gaza: Meningitis epidemic alert, 272 cases in October.","OFFICIAL"),("20 DR Congo: Missing Cessna 208, rebels claim shootdown.","CLAIM"),("21 Hanoi: Hot-pot explosion kills at least 6 people.","REPORTED"),("22 Gulf of Finland: Ukraine hits Russian ship Sparta II.","REPORTED"),("23 Kuala Lumpur: Malaysia to return migrants to Myanmar.","OFFICIAL"),("24 Ulleungdo: S. Korea shelter order as Russian jets enter ADIZ.","OFFICIAL"),("25 Dhaka: Hasina plans return on 16 December.","REPORTED"),("26 The Hague: 14 nations endorse ICJ Myanmar ruling.","REPORTED"),("27 Jakarta: Indonesia nominates 2 VP candidates.","OFFICIAL"),("28 Beijing: China sentences official Ma to death for spying.","OFFICIAL"),("29 Brussels: NATO vows defence against space threat.","OFFICIAL"),("30 Mexico City: El Chapo Isidro arrested Fri 20 Nov.","REPORTED"),("31 San Salvador: Bukele names 3 soldiers killed in Haiti.","OFFICIAL"),("32 Ottawa: Pentagon rebukes Canada as only 41.9% of air fleet ready.","REPORTED"),("33 Washington: US adds Megaspeed to trade blacklist.","OFFICIAL"),("34 Kyiv: Zelensky urges Ukraine, Russia, US and Europe talks soon.","REPORTED"),("35 Ras Al Khaimah: UAE bus-truck crash kills 13 people.","REPORTED"),("36 London: England record 5,258 heat deaths in summer 2026.","OFFICIAL"),("37 Kourou: Ariane 6 lofts 36 Amazon satellites.","OFFICIAL"),("38 Cikande: Factory-fire toll rises to 26 people.","REPORTED")]
def main():
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im); d.rectangle([0,0,W,10],fill=RED)
    txt(d,16,16,"THE WORLD ON ONE PAGE",F(11,True),RED); txt(d,W-16,16,"38 STORIES · 6 REGIONS · 13 FIELDS",F(11,True),RED,align="right")
    txt(d,16,34,"Tuesday 24 November 2026",F(30,True,True)); d.line([(16,68),(W-16,68)],fill=INK,width=2)
    txt(d,16,74,"Riyadh tower hit again · Shanghai party chief probed · Huawei guilty on 10 of 12 counts.",F(12,False,True),RED)
    regs=[("Europe",9,RED),("Middle East",8,(200,120,30)),("Asia",8,TEAL),("Africa",2,(18,120,60)),("Americas",7,NAVY),("World/Space",4,(110,60,140))]; x=16
    for name,n,c in regs:
        w=150; d.rectangle([x,94,x+w,112],fill=c); txt(d,x+6,97,f"{name} {n}",F(10,True),(255,255,255)); x+=w+4
    txt(d,16,118,"THE DAY IN UTC",F(10,True),RED); utc="02:15 NATO space defence  ·  08:16 Hanoi blast  ·  10:42 Saudi strikes Yemen  ·  14:27 Riyadh tower hit  ·  16:51 Houthis 60 km from Aden  ·  18:58 Hormuz ship attack  ·  20:41 Huawei guilty."; para(d,16,132,utc,F(10),W-32,12)
    txt(d,16,158,"THE DAY IN NUMBERS",F(10,True),RED); nums=[("11","hurt, Riyadh"),("9","killed, Ukraine"),("50,018","Dow close"),("+8.99%","Taiex record"),("25","killed, Yemen"),("26","toll, Cikande"),("10/12","Huawei guilty"),("96","drones, Ukraine")]
    x=16
    for v,lab in nums:
        txt(d,x,172,v,F(16,True),RED); txt(d,x,190,lab,F(8),GREY); x+=122
    d.line([(16,208),(W-16,208)],fill=INK,width=1)
    hw=322; hx=16
    for i,(kick,kind,head,deck,col,cf,src) in enumerate(HERO):
        x=hx+i*(hw+8); scene(d,x,214,hw,92,kind); d.rectangle([x,306,x+hw,306],fill=RED); txt(d,x,312,kick,F(10,True),col); nx=chip(d,x,328,cf,col); txt(d,nx+2,330,f"({src})",F(8),GREY)
        y=para(d,x,346,head,F(13,True),hw,15); para(d,x,y+2,deck,F(10),hw,12)
    d.line([(16,470),(W-16,470)],fill=INK,width=1)
    cw=194
    for r in range(2):
        for c in range(5):
            i=r*5+c; kick,kind,head,deck,col,cf,src=CARDS[i]; x=16+c*(cw+6); y=478+r*138; scene(d,x,y,cw,46,kind); txt(d,x,y+50,kick,F(8,True),col); chip(d,x,y+63,cf,col); txt(d,x+62,y+65,f"({src})",F(7),GREY); yy=para(d,x,y+79,head,F(10,True),cw,12); para(d,x,yy+1,deck,F(8),cw,10)
    mx,my,mw,mh=16,760,370,158; d.rectangle([mx,my,mx+mw,my+mh],fill=(232,240,248),outline=NAVY); txt(d,mx+6,my+4,"WORLD MAP — PINS 1-13",F(9,True),NAVY)
    def XY(lon,lat): return mx+8+(lon+180)/360*(mw-16),my+18+(80-lat)/140*(mh-26)
    for poly in CONT:
        pts=[XY(lon,lat) for lon,lat in poly]; d.polygon(pts,fill=LGREEN,outline=(90,120,80))
    for n,lat,lon in PINS:
        px,py=XY(lon,lat); dx,dy=OFF.get(n,(0,0)); qx,qy=px+dx,py+dy
        if (dx,dy)!=(0,0): d.line([(px,py),(qx,qy)],fill=RED,width=1)
        d.ellipse([qx-8,qy-8,qx+8,qy+8],fill=RED,outline=(255,255,255)); d.text((qx-3,qy-6),str(n),font=F(8,True),fill=(255,255,255))
    lx=mx+mw+10; txt(d,lx,760,"ALSO ON TUESDAY 24 NOVEMBER — 25 MORE STORIES",F(10,True),RED)
    for j,(s,cf) in enumerate(ALSO):
        col=j//13; row=j%13; x=lx+col*300; y=778+row*11; cc={"CONFIRMED":(18,120,60),"OFFICIAL":(24,48,84),"REPORTED":(110,110,105),"CLAIM":(200,120,30)}[cf]; d.rectangle([x,y+1,x+7,y+8],fill=cc); d.text((x+10,y),s,font=F(8),fill=INK)
    txt(d,lx,924,"Legend: green CONFIRMED · blue OFFICIAL · grey REPORTED · orange CLAIM. Pins 3 and 7 share New York; pin 7 is offset.",F(7),GREY)
    d.rectangle([16,940,W-16,1006],fill=(178,34,34)); txt(d,24,946,"DATE CHECK",F(10,True),(255,255,255)); para(d,24,960,"Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC. LEFT OUT (not 24 Nov): Hormuz mine claims (23 Nov); Huang returns as Nvidia CEO (23 Nov); EU sanctions package (23 Nov); COP31 no deal (22 Nov); Merkury sinks (22 Nov); El Chapo Isidro arrested (Fri 20 Nov); Cikande fire starts (21 Nov). NOT YET: Shenzhou-24 launch (Wed 25 Nov 00:18 UTC); MPR picks VP (11 Dec); Huawei sentencing (Sep 2027); Hasina returns (16 Dec).",F(8),972,9,fill=(255,255,255))
    txt(d,16,1012,"Sources: dailysummaryof.com/world/2026-11-24 · Reuters · AP · UKMTO · CAS · CMSA · CCDI. Scenes are drawn illustrations, not photographs.",F(7),GREY)
    out=os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR","out"),"entry.png"); os.makedirs(os.path.dirname(out) or ".",exist_ok=True); im.save(out,optimize=True); print(out)
if __name__=="__main__": main()
