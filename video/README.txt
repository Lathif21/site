Videobestanden voor de site.

Aanwezig:
  ov-mortex.mp4 / ov-mortex.webm   video-CTA op index.html ("DIY Mortex Tafel")
      DUMMY. Nu nog dezelfde opname als tu-vid1; vervang door de echte
      Mortex-video. Poster is img/ov-video.jpg, dus het paneel ziet er
      ongewijzigd uit tot er op de knop gedrukt wordt.

  tu-vid1.mp4 / tu-vid1.webm       tutorials.html, "Een tutorial toevoegen"
      Bron: ../video-masters/tu-vid1-master.mov (3456x2144, 60fps, 2,5s, geen audio)
      Web:  1280x794, 30fps, H.264 High + VP9. Poster: img/tu-vid1.jpg (frame 0).

Nog toe te voegen:
  tu-vid2.mp4   ("tut 1")
      Zet het bestand hier neer en vul in build.py de size-tuple van tu-vid2 in
      ((breedte, hoogte)); de <source> voor webm en het width/height-attribuut
      worden dan mee gegenereerd. Zonder size blijft de TODO-placeholder staan.

Hercoderen (ffmpeg):
  ffmpeg -i master.mov -an -vf "scale=1280:-2,fps=30" \
         -c:v libx264 -profile:v high -pix_fmt yuv420p -preset slow -crf 23 \
         -movflags +faststart naam.mp4
  ffmpeg -i master.mov -an -vf "scale=1280:-2,fps=30" \
         -c:v libvpx-vp9 -crf 34 -b:v 0 -row-mt 1 naam.webm
  ffmpeg -i master.mov -vf "scale=1280:-2" -frames:v 1 -q:v 4 ../img/naam.jpg
