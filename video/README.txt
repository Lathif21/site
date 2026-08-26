Videobestanden voor de site.

Aanwezig:
  ov-mortex.mp4 / ov-mortex.webm   webshop-hero, video-band en de CTA op index.html
      Montage uit het eigen beeldmateriaal in img/ — geen gefilmde opname.
      Vijf shots, verhaal pakket -> bouwen -> afwerken -> gestyled -> bewoond:
        ov-pallet, rz-3-2, rz-1-1, rz-1-2, rz-3-4
      Elk 3s met Ken Burns-zoom, 0,8s crossfades, fade naar zwart aan begin en
      eind zodat de loop rond is. 11,8s, 1600x900, 25fps, geen audio.
      Poster: img/ov-video.jpg (frame op 1,0s).

      KWALITEITSPLAFOND: vier van de vijf bronfoto's zijn maar 900px breed, dus
      een 16:9 uitsnede levert 900x506. Daarom 1600x900 (niet 1080p — dat voegt
      opschaling toe zonder detail), zoom tot maximaal 1.06 in plaats van 1.16,
      lanczos bij het opschalen en unsharp erna. Echte gefilmde beelden zijn de
      enige manier om hier verder te komen.
      Opnieuw genereren: zie hero.sh-recept onderaan.

      Vervang dit door echte videobeelden zodra die er zijn — de markup,
      posters en reduced-motion fallback blijven ongewijzigd.

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

Hero-montage opnieuw bouwen (ffmpeg):
  Per foto: scale=2560:1440 (cover-crop) -> zoompan d=75 s=1280x720 fps=25,
  daarna xfade duration=0.8 met offsets 2.2 / 4.4 / 6.6 / 8.8, en tot slot
  fade=in st=0 d=0.7 + fade=out st=11.1 d=0.7.
  mp4:  -c:v libx264 -profile:v high -preset slow -crf 20 -movflags +faststart
  webm: -c:v libvpx-vp9 -crf 24 -b:v 0 -row-mt 1 -deadline good -cpu-used 1

  Beide worden gemaakt uit ../video-masters/ov-mortex-master.mp4 (17,9MB,
  12,4Mbps). Gemeten tegen dat master: webm SSIM 0,9922 / PSNR 48,5dB en mp4
  SSIM 0,9932 / PSNR 48,8dB. Boven ~45dB is visueel verliesloos, dus de
  webversies zijn niet van het master te onderscheiden — op 1:1 gecontroleerd.
  Het master hoort NIET in video/: publish = "." zou 17,9MB meesturen.
