# IT101
# Valentijn Bruggeman

# Uitleg
Ik heb een spel gemaakt met een Odroid N2+. Het doel van het spel is zoveel mogelijk punten halen in een gegeven tijdsbestek. Door middel van een 16x2 LCD scherm laat ik de gebruiker een mode kiezen (easy, medium of hard) en zijn score en tijd laten zien tijdens het spelen.

## Hoe het spel werkt
Door maximaal 60cm voor het spel te staan geeft de ultrasonic sensor een signaal naar de LCD scherm om een reeks berichten te laten zien om uiteindelijk de gebruiker te vragen om op een mode te selecteren door op een van de drie knoppen te drukken. Zodra een mode gekozen is draait de servo naar de juiste stand (easy, medium of hard) en gaat op de LCD scherm de tijd aftellen en toont die de huidige score. Als de tijd is afgelopen wordt je score nog een keer getoond en kan je kiezen om nog een keer te spelen. 

De data van de ultrasonic (tijd en afstand) en break beam snesor (tijd en score) wordt opgeslagen in een database en vervolgens weergegeven in een tabel op mijn website. Daarnaast is het ook mogelijk om via de website de servo aan te sturen.

# Benodigdheden
1. Odroid N2+
2. 1x Ultrasonic sensor
3. 1x LCD scherm
4. 3x Shorting switch knoppen (of iets wat daar op lijkt)
5. 1x Servo
6. 5x Break beam sensor (infrarood ontvanger en zender)

## Installatie
Ik heb Ubuntu gedownload op mijn odroid (zie support voor meer informatie) om als operating system te gebruiken. Verder heb ik de wiringpi library gebruikt samen met mysql, python3 en git om mijn project veilig te stellen op een alternatieve plek.

## Fotos
### De fysieke kast
![](../../images/spel_kast.png)
### Mijn aansluit schema
![](../../images/technische tekening.png)
Zoals te zien is heb ik in de technische tekening alleen een IR ontvanger getekend. In de daadwerkelijke aansluiting is er ook een zender die aangesloten is op de ground en 3.3V. Verder zijn niet alle IR ontvangers opgenomen in de technische tekening. Die zijn precies hetzelfde aangesloten als degene die wel opgenomen is in de technische tekening.
### Servo gedetaileerd
![](../../images/servo.png)
### Odroid plek in kast
![](../../images/odroidHoek.png)
### Knoppen, LCD en Ultrasonic sensor
![](../../images/knoppen_LCD.png)
### Break beam sensoren
![](../../images/breakBeam.png)

## Support
Voor meer informatie over de wiringpi library kan je hier terecht: http://wiringpi.com

Voor meer informatie over de Odroid N2+ kan je hier terecht: https://wiki.odroid.com/odroid-n2/odroid-n2

## Roadmap
Ik zou graag nog een break beam sensor toe willen voegen bij het grootste gat om accurater te meten. 
Daarnaast zou ik de website knoppen willen geven in plaats van dat je met een link naar de verschillende opties moet navigeren.

## Authors and acknowledgment
Met dank aan Jack Zwuup voor het helpen opzetten van een database en website!

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
